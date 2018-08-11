import unittest
from hask import H, t
from hask import __
from hask import L
from hask import Maybe, Just, Nothing
from hask import Either, Left, Right

# internals
from hask.lang.type_system import make_fn_type
from hask.lang.type_system import build_sig_arg
from hask.lang.type_system import build_sig
from hask.lang.type_system import typeof

from hask.lang.hindley_milner import Var
from hask.lang.hindley_milner import App
from hask.lang.hindley_milner import Lam
from hask.lang.hindley_milner import Let
from hask.lang.hindley_milner import TypeVariable
from hask.lang.hindley_milner import TypeOperator
from hask.lang.hindley_milner import Function
from hask.lang.hindley_milner import Tuple
from hask.lang.hindley_milner import unify

te = TypeError


class TestHindleyMilner(unittest.TestCase):
    """Test the internals of the Hindley-Milner type inference engine"""

    def inference(self, expr):
        """Type inference succeeded using our toy environment"""
        self.assertIsNotNone(expr.analyze(self.env))
        return

    def not_inference(self, expr):
        """Type inference failed using our toy environment"""
        with self.assertRaises(te):
            expr.analyze(self.env)
        return

    def unified(self, t1, t2):
        """Two types are able to be unified"""
        self.assertIsNone(unify(t1, t2))
        return

    def typecheck(self, expr, expr_type):
        """Typecheck succeeded using our toy environment"""
        self.assertIsNone(unify(expr.analyze(self.env), expr_type))
        return

    def not_typecheck(self, expr, expr_type):
        """Typecheck failed, but inference succeeded using our toy environment
        """
        self.inference(expr)
        with self.assertRaises(te):
            self.typecheck(expr, expr_type)
        return

    def setUp(self):
        """Create some basic types and polymorphic typevars, a toy environment,
           and some AST nodes
        """
        self.var1 = TypeVariable()
        self.var2 = TypeVariable()
        self.var3 = TypeVariable()
        self.var4 = TypeVariable()
        self.Pair = TypeOperator("*", (self.var1, self.var2))
        self.Bool = TypeOperator("bool", [])
        self.Integer = TypeOperator("int", [])
        self.NoneT = TypeOperator("None", [])

        # toy environment
        self.env = {"pair": Function(self.var1,
                                     Function(self.var2, self.Pair)),
                    "True": self.Bool,
                    "None": self.NoneT,
                    "id": Function(self.var4, self.var4),
                    "cond": Function(self.Bool, Function(self.var3,
                                     Function(self.var3, self.var3))),
                    "zero": Function(self.Integer, self.Bool),
                    "pred": Function(self.Integer, self.Integer),
                    "times": Function(self.Integer,
                                      Function(self.Integer, self.Integer)),
                    "4": self.Integer,
                    "1": self.Integer}

        # some expressions to play around with
        self.compose = Lam(
            "f",
            Lam("g",
                Lam("arg",
                    App(Var("g"), App(Var("f"), Var("arg")))))
        )
        self.pair = App(
            App(Var("pair"), App(Var("f"), Var("1"))),
            App(Var("f"), Var("True"))
        )

    def test_type_inference(self):
        """Basic type inference in our toy environment"""

        # (* True) ==> TypeError
        self.not_inference(App(Var("times"), Var("True")))

        # (* True) ==> TypeError (undefined symbol a)
        self.not_inference(App(Var("times"), Var("a")))

        # monomorphism restriction
        # \x -> ((x 4), (x True)) ==> TypeError
        self.not_inference(
            Lam("x",
                App(
                    App(Var("pair"),
                        App(Var("x"), Var("4"))),
                    App(Var("x"), Var("True")))))

        # \x -> ((f 4), (f True)) ==> TypeError (undefined symbol f)
        self.not_inference(
            App(
                App(Var("pair"), App(Var("f"), Var("4"))),
                App(Var("f"), Var("True"))))

        # \f -> (f f) ==> TypeError (recursive unification)
        self.not_inference(Lam("f", App(Var("f"), Var("f"))))

    def test_type_checking(self):
        """Basic type checking in our toy environment"""

        # 1 :: Integer
        self.typecheck(Var("1"), self.Integer)

        # 1 :: Bool ==> TypeError
        self.not_typecheck(Var("1"), self.Bool)

        # (\x -> x) :: (a -> a)
        v = TypeVariable()
        self.typecheck(
            Lam("n", Var("n")),
            Function(v, v))

        # type(id) == type(\x -> x)
        self.typecheck(
            Lam("n", Var("n")),
            self.env["id"])

        # (\x -> x) :: (a -> b)
        self.typecheck(
            Lam("n", Var("n")),
            Function(TypeVariable(), TypeVariable()))

        # (id 1) :: Integer
        self.typecheck(App(Var("id"), Var("1")), self.Integer)

        # (id 1) :: Bool ==> TypeError
        self.not_typecheck(App(Var("id"), Var("1")), self.Bool)

        # pred :: (Integer -> Integer)
        self.typecheck(Var("pred"), Function(self.Integer, self.Integer))

        # (pred 4) :: Integer
        self.typecheck(
            App(Var("pred"), Var("1")),
            self.Integer)

        # ((pair 1) 4) :: (a, b)
        self.typecheck(
            App(App(Var("pair"), Var("1")), Var("4")),
            TypeOperator("*", [TypeVariable(), TypeVariable()]))

        # (*) :: (Integer -> Integer -> Integer)
        self.typecheck(
            Var("times"),
            Function(self.Integer, Function(self.Integer, self.Integer)))

        # (* 4) :: (Integer -> Integer)
        self.typecheck(
            App(Var("times"), Var("4")),
            Function(self.Integer, self.Integer))

        # (* 4) :: (Bool -> Integer) ==> TypeError
        self.not_typecheck(
            App(Var("times"), Var("4")),
            Function(self.Bool, self.Integer))

        # (* 4) :: (Integer -> a) ==> TypeError
        self.not_typecheck(
            App(Var("times"), Var("4")),
            Function(self.Integer, TypeVariable))

        # ((* 1) 4) :: Integer
        self.typecheck(
            App(App(Var("times"), Var("1")), Var("4")),
            self.Integer)

        # ((* 1) 4) :: Bool ==> TypeError
        self.not_typecheck(
            App(App(Var("times"), Var("1")), Var("4")),
            self.Bool)

        # let g = (\f -> 5) in (g g) :: Integer
        self.typecheck(
            Let("g",
                Lam("f", Var("4")),
                App(Var("g"), Var("g"))),
            self.Integer)

        # (.) :: (a -> b) -> (b -> c) -> (a -> c)
        a, b, c = TypeVariable(), TypeVariable(), TypeVariable()
        self.typecheck(
            self.compose,
            Function(Function(a, b),
                     Function(Function(b, c), Function(a, c))))

        # composing `id` with `id` == `id`
        # ((. id) id) :: (a -> a)
        d = TypeVariable()
        self.typecheck(
            App(App(self.compose, Var("id")), Var("id")),
            Function(d, d))

        # composing `id` with `times 4`
        # ((. id) (* 2)) :: (int -> int)
        self.typecheck(
            App(App(self.compose, Var("id")),
                App(Var("times"), Var("4"))),
            Function(self.Integer, self.Integer))

        # composing `times 4` with `id`
        # ((. (* 2)) id) :: (int -> int)
        self.typecheck(
            App(App(self.compose,
                    App(Var("times"), Var("4"))), Var("id")),
            Function(self.Integer, self.Integer))

        # basic closure
        # ((\x -> (\y -> ((* x) y))) 1) :: (Integer -> Integer)
        self.typecheck(
            App(
                Lam("x",
                    Lam("y", App(App(Var("times"), Var("x")), Var("y")))),
                Var("1")),
            Function(self.Integer, self.Integer))

        # lambdas have lexical scope
        # (((\x -> (\x -> x)) True) None) :: NoneT
        self.typecheck(
            App(App(
                Lam("x", Lam("x", Var("x"))),
                Var("True")), Var("None")),
            self.NoneT)

        # basic let expression
        # let a = times in ((a 1) 4) :: Integer
        self.typecheck(
            Let("a", Var("times"), App(App(Var("a"), Var("1")), Var("4"))),
            self.Integer)

        # let has lexical scope
        # let a = 1 in (let a = None in a) :: NoneT
        self.typecheck(
            Let("a", Var("1"), Let("a", Var("None"), Var("a"))),
            self.NoneT)

        # let polymorphism
        # let f = (\x -> x) in ((f 4), (f True)) :: (Integer, Bool)
        self.typecheck(
            Let("f", Lam("x", Var("x")), self.pair),
            TypeOperator("*", [self.Integer, self.Bool]))

        # recursive let
        # (factorial 4) :: Integer
        self.typecheck(
            Let("factorial",  # letrec factorial =
                Lam("n",      # fn n =>
                    App(
                        App(   # cond (zero n) 1
                            App(Var("cond"),     # cond (zero n)
                                App(Var("zero"), Var("n"))),
                            Var("1")),
                        App(    # times n
                            App(Var("times"), Var("n")),
                            App(Var("factorial"),
                                App(Var("pred"), Var("n")))
                        )
                    )
                ),      # in  # noqa
                App(Var("factorial"), Var("4"))),
            self.Integer)

    def test_build_sig_item(self):
        """Test type signature building internals - make sure that types are
           translated in a reasonable way"""

        class example(object):
            pass

        # type variables
        self.assertTrue(isinstance(build_sig_arg("a", {}, {}), TypeVariable))
        self.assertTrue(isinstance(build_sig_arg("abc", {}, {}), TypeVariable))

        # builtin/non-ADT types
        self.unified(build_sig_arg(str, {}, {}), TypeOperator(str, []))
        self.unified(build_sig_arg(int, {}, {}), TypeOperator(int, []))
        self.unified(build_sig_arg(float, {}, {}), TypeOperator(float, []))
        self.unified(build_sig_arg(list, {}, {}), TypeOperator(list, []))
        self.unified(build_sig_arg(set, {}, {}), TypeOperator(set, []))
        self.unified(build_sig_arg(example, {}, {}), TypeOperator(example, []))

        # unit type (None)
        self.unified(build_sig_arg(None, {}, {}), TypeOperator(None, []))

        # tuple
        self.unified(
            build_sig_arg((int, int), {}, {}),
            Tuple([TypeOperator(int, []), TypeOperator(int, [])])
        )
        self.unified(
            build_sig_arg((None, (None, int)), {}, {}),
            Tuple([
                TypeOperator(None, []),
                Tuple([TypeOperator(None, []), TypeOperator(int, [])])
            ])
        )
        a = TypeVariable()
        self.unified(
            build_sig_arg(("a", "a", "a"), {}, {}),
            Tuple([a, a, a])
        )

        # list
        self.unified(typeof(L[[]]), build_sig_arg(["a"], {}, {}))
        self.unified(typeof(L[1, 1]), build_sig_arg([int], {}, {}))
        self.unified(typeof(L[[L[1, 1]]]), build_sig_arg([[int]], {}, {}))

        # adts
        self.unified(typeof(Nothing), build_sig_arg(t(Maybe, "a"), {}, {}))
        self.unified(typeof(Just(1)), build_sig_arg(t(Maybe, int), {}, {}))
        self.unified(
            typeof(Just(Just(Nothing))),
            build_sig_arg(t(Maybe, t(Maybe, t(Maybe, "a"))), {}, {}))
        self.unified(
            typeof(Right("error")),
            build_sig_arg(t(Either, str, "a"), {}, {}))
        self.unified(
            typeof(Left(2.0)),
            build_sig_arg(t(Either, "a", int), {}, {}))
        self.unified(
            typeof(Just(__+1)),
            build_sig_arg(t(Maybe, "a"), {}, {}))
        self.unified(
            typeof(Just(__+1)),
            build_sig_arg(t(Maybe, (H/ "a" >> "b")), {}, {}))

    def test_signature_build(self):
        """Make sure type signatures are built correctly"""
        # int -> int
        self.unified(
            make_fn_type(build_sig((H/ int >> int).sig)),
            Function(TypeOperator(int, []), TypeOperator(int, [])))

        # a -> a
        a = TypeVariable()
        self.unified(
            make_fn_type(build_sig((H/ "a" >> "a").sig)),
            Function(a, a))

        # a -> b
        a, b = TypeVariable(), TypeVariable()
        self.unified(
            make_fn_type(build_sig((H/ "a" >> "b").sig)),
            Function(a, b))

        # (int -> int) -> int -> int
        self.unified(
            make_fn_type(
                build_sig((H/ (H/ int >> int) >> int >> int).sig)
            ),
            Function(
                Function(TypeOperator(int, []), TypeOperator(int, [])),
                Function(TypeOperator(int, []), TypeOperator(int, []))
            )
        )

    def test_typecheck_builtins(self):
        """Make sure builtin types typecheck correctly"""

        # 1 :: int
        self.unified(typeof(1), TypeOperator(int, []))

        # "a" :: str
        self.unified(typeof("a"), TypeOperator(str, []))

        # Nothing :: Maybe a
        self.unified(
                typeof(Nothing),
                TypeOperator(Maybe, [TypeVariable()]))

        # Just(1) :: Maybe int
        self.unified(
                typeof(Just(1)),
                TypeOperator(Maybe, [TypeOperator(int, [])]))

        # Just(Just(Nothing)) :: Maybe (Maybe (Maybe a))
        self.unified(
            typeof(Just(Just(Nothing))),
            TypeOperator(
                Maybe,
                [TypeOperator(
                    Maybe,
                    [TypeOperator(Maybe, [TypeVariable()])])])
        )

        # Right("error") :: Either a str
        self.unified(
            typeof(Right("error")),
            TypeOperator(Either, [TypeVariable(),
                                  TypeOperator(str, [])]))

        # Left(2.0) :: Either float a
        self.unified(
            typeof(Left(2.0)),
            TypeOperator(Either,
                         [TypeOperator(float, []), TypeVariable()]))
