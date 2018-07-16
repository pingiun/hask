import math
import sys
import unittest

from hask import H, sig, t, func, TypeSignatureError
from hask import p, m, caseof, IncompletePatternError
from hask import has_instance
from hask import guard, c, otherwise, NoGuardMatchException
from hask import __
from hask import data, d, deriving, instance
from hask import L
from hask import Ordering, LT, EQ, GT
from hask import Maybe, Just, Nothing, in_maybe
from hask import Either, Left, Right, in_either
from hask import Typeclass
from hask import Read, Show, Eq, Ord, Bounded, Num
from hask import Functor, Applicative, Monad
from hask import Foldable, Traversable

# internals
from hask.lang.type_system import make_fn_type
from hask.lang.type_system import build_sig_arg
from hask.lang.type_system import build_sig
from hask.lang.type_system import build_ADT
from hask.lang.type_system import typeof
from hask.lang.type_system import pattern_match
from hask.lang.type_system import PatternMatchBind

from hask.lang.hindley_milner import Var
from hask.lang.hindley_milner import App
from hask.lang.hindley_milner import Lam
from hask.lang.hindley_milner import Let
from hask.lang.hindley_milner import TypeVariable
from hask.lang.hindley_milner import TypeOperator
from hask.lang.hindley_milner import Function
from hask.lang.hindley_milner import Tuple
from hask.lang.hindley_milner import analyze
from hask.lang.hindley_milner import unify

from hask.lang.lazylist import List

te = TypeError
se = SyntaxError
ve = ValueError


class TestADTInternals_Enum(unittest.TestCase):

    def setUp(self):
        """
        Dummy type constructors and data constructors for an ADT with all
        enum data constructors
        """
        ds =  [("E1", []), ("E2", []), ("E3", [])]
        self.Type_Const, self.E1, self.E2, self.E3 =\
                build_ADT("Type_Const", [], ds, [])

    def test_adt(self):
        self.assertEqual(list(self.Type_Const.__constructors__),
                         [self.E1, self.E2, self.E3])
        self.assertTrue(isinstance(self.E1, self.Type_Const))
        self.assertTrue(isinstance(self.E2, self.Type_Const))
        self.assertTrue(isinstance(self.E3, self.Type_Const))

    def test_derive_eq_data(self):
        with self.assertRaises(te): self.E1 == self.E1
        with self.assertRaises(te): self.E1 != self.E1

        Eq.derive_instance(self.Type_Const)

        self.assertTrue(self.E1 == self.E1)
        self.assertTrue(self.E2 == self.E2)
        self.assertTrue(self.E3 == self.E3)

    def test_derive_show_data(self):
        self.assertNotEquals("E1", str(self.E1))

        Show.derive_instance(self.Type_Const)

        self.assertEqual("E1", str(self.E1))
        self.assertEqual("E2", str(self.E2))
        self.assertEqual("E3", str(self.E3))

    def test_derive_ord_data(self):
        with self.assertRaises(te): self.E1 > self.E1
        with self.assertRaises(te): self.E1 >= self.E1
        with self.assertRaises(te): self.E1 < self.E1
        with self.assertRaises(te): self.E1 <= self.E1

        Eq.derive_instance(self.Type_Const)
        Ord.derive_instance(self.Type_Const)

        self.assertTrue(self.E1 < self.E2)
        self.assertTrue(self.E1 <= self.E2)
        self.assertFalse(self.E1 > self.E2)
        self.assertFalse(self.E1 >= self.E2)

    def test_derive_bounded_data(self):
        Bounded.derive_instance(self.Type_Const)


class TestADTInternals_Builtin(unittest.TestCase):

    def setUp(self):
        """
        Dummy type constructors and data constructors for an ADT with all
        builtin (non-polymorphic) fields
        """
        ds =  [("M1", [int]), ("M2", [int, str]), ("M3", [int, int, int])]
        self.Type_Const, self.M1, self.M2, self.M3 =\
                build_ADT("Type_Const", [], ds, [])

    def test_adt(self):
        self.assertTrue(isinstance(self.M1(1), self.Type_Const))
        self.assertTrue(isinstance(self.M2(1, "abc"), self.Type_Const))
        self.assertTrue(isinstance(self.M2(1)("abc"), self.Type_Const))
        self.assertTrue(isinstance(self.M3(1, 2, 3), self.Type_Const))
        self.assertTrue(isinstance(self.M3(1)(2, 3), self.Type_Const))

        with self.assertRaises(te): self.M1(1.0)
        with self.assertRaises(te): self.M3(1, 2, "3")

    def test_derive_eq_data(self):
        with self.assertRaises(te): self.M1(1) == self.M1(1)
        with self.assertRaises(te): self.M1(1) != self.M1(1)

        Eq.derive_instance(self.Type_Const)

        self.assertTrue(self.M1(1) == self.M1(1))
        self.assertTrue(self.M2(1, "b") == self.M2(1, "b"))
        self.assertTrue(self.M3(1, 2, 3) == self.M3(1, 2, 3))
        self.assertFalse(self.M1(1) != self.M1(1))
        self.assertFalse(self.M2(1, "b") != self.M2(1, "b"))
        self.assertFalse(self.M3(1, 2, 3) != self.M3(1, 2, 3))
        self.assertFalse(self.M1(1) == self.M1(2))
        self.assertFalse(self.M2(1, "b") == self.M2(4, "b"))
        self.assertFalse(self.M2(1, "b") == self.M2(1, "a"))
        self.assertFalse(self.M3(1, 2, 3) == self.M3(1, 9, 3))

    def test_derive_show_data(self):
        self.assertNotEquals("M1(1)", str(self.M1(1)))

        Show.derive_instance(self.Type_Const)
        self.assertEqual("M1(1)", str(self.M1(1)))
        self.assertEqual("M2(1, \'a\')", str(self.M2(1, "a")))
        self.assertEqual("M3(1, 2, 3)", str(self.M3(1, 2, 3)))

    def test_derive_ord_data(self):
        with self.assertRaises(te): self.M1(1) > self.M1(1)
        with self.assertRaises(te): self.M1(1) >= self.M1(1)
        with self.assertRaises(te): self.M1(1) < self.M1(1)
        with self.assertRaises(te): self.M1(1) <= self.M1(1)

        Eq.derive_instance(self.Type_Const)
        Ord.derive_instance(self.Type_Const)

        self.assertTrue(self.M1(1) < self.M1(2))
        self.assertTrue(self.M1(1) <= self.M1(2))
        self.assertTrue(self.M1(2) <= self.M1(2))
        self.assertFalse(self.M1(3) < self.M1(2))
        self.assertFalse(self.M1(3) <= self.M1(2))
        self.assertTrue(self.M1(2) > self.M1(1))
        self.assertTrue(self.M1(2) >= self.M1(1))
        self.assertTrue(self.M1(2) >= self.M1(2))
        self.assertFalse(self.M1(1) > self.M1(2))
        self.assertFalse(self.M1(1) >= self.M1(2))

    def test_derive_bounded_data(self):
        with self.assertRaises(te):
            Bounded.derive_instance(self.Type_Const)


class TestADTInternals_Poly(unittest.TestCase):
    def setUp(self):
        """
        Dummy type constructors and data constructors for an ADT with
        polymorphic fields
        """
        ds =  [("M1", ["a"]), ("M2", ["a", "b"]), ("M3", ["a", "c", "c"])]
        self.Type_Const, self.M1, self.M2, self.M3 =\
                build_ADT("Type_Const", ["a", "b", "c"], ds, [])

    def test_adt(self):
        self.assertTrue(isinstance(self.M1(1), self.Type_Const))
        self.assertTrue(isinstance(self.M2(1, "abc"), self.Type_Const))
        self.assertTrue(isinstance(self.M2(1)("abc"), self.Type_Const))
        self.assertTrue(isinstance(self.M3(1, 2, 3), self.Type_Const))
        self.assertTrue(isinstance(self.M3(1)(2, 3), self.Type_Const))
        with self.assertRaises(te): self.M3(1, "a", 2)

    def test_derive_eq_data(self):
        with self.assertRaises(te): self.M1(1) == self.M1(1)
        with self.assertRaises(te): self.M1(1) == self.M2(1, "b")
        with self.assertRaises(te): self.M1(1) != self.M1(1)
        with self.assertRaises(te): self.M1(1) != self.M2(1, "b")

        Eq.derive_instance(self.Type_Const)

        self.assertEqual(self.M1(1), self.M1(1))
        self.assertEqual(self.M2(1, "a"), self.M2(1, "a"))
        self.assertNotEqual(self.M1("a"), self.M1("b"))
        self.assertNotEqual(self.M1("a"), self.M2("a", "b"))
        self.assertEqual(self.M3(1, "b", "b"), self.M3(1, "b", "b"))
        with self.assertRaises(te): self.M1(1) == self.M1("a")
        with self.assertRaises(te): self.M3(1, 2, 2) == self.M3(1, "a", "b")

    def test_derive_show_data(self):
        self.assertNotEqual("M1(1)", str(self.M1(1)))
        self.assertNotEqual("M2(1, 2)", str(self.M2(1, 2)))

        Show.derive_instance(self.Type_Const)

        self.assertEqual("M1(1)", str(self.M1(1)))
        self.assertEqual("M2(1, 2)", str(self.M2(1, 2)))

    def test_derive_ord_data(self):
        with self.assertRaises(te): self.M1(1) > self.M1(1)
        with self.assertRaises(te): self.M1(1) < self.M2(1, "b")
        with self.assertRaises(te): self.M1(1) >= self.M1(1)
        with self.assertRaises(te): self.M1(1) <= self.M2(1, "b")

        Eq.derive_instance(self.Type_Const)
        Ord.derive_instance(self.Type_Const)

        self.assertTrue(self.M1(1) < self.M2(100, "a"))
        self.assertTrue(self.M1(1) <= self.M2(100, "a"))
        self.assertFalse(self.M1(1) > self.M2(100, "a"))
        self.assertFalse(self.M1(1) >= self.M2(100, "a"))
        self.assertTrue(self.M3(1, "a", "b") < self.M3(1, "a", "c"))
        self.assertTrue(self.M3(1, "a", "b") <= self.M3(1, "a", "c"))
        self.assertFalse(self.M1(1) > self.M2(100, "a"))
        self.assertFalse(self.M1(1) >= self.M2(100, "a"))
        with self.assertRaises(te): self.M1(1) > self.M1("a")
        with self.assertRaises(te): self.M3(1, 2, 2) > self.M3(1, "a", "b")


class TestADTSyntax(unittest.TestCase):

    def test_data(self):
        # these are not syntactically valid
        with self.assertRaises(se): data.n
        with self.assertRaises(se): data.n("a")
        with self.assertRaises(se): data.N("!")
        with self.assertRaises(se): data.N("A")
        with self.assertRaises(se): data.N("a", "a")
        with self.assertRaises(se): data.N(1, "b")
        with self.assertRaises(se): data.N("a")("b")
        with self.assertRaises(se): data.N()
        with self.assertRaises(se): data.N == d
        with self.assertRaises(se): data.N == 1

        # these should all work fine
        self.assertIsNotNone(data.N)
        self.assertIsNotNone(data.N1)
        self.assertIsNotNone(data.N("a"))
        self.assertIsNotNone(data.N("azzz"))
        self.assertIsNotNone(data.N("a", "b"))

    def test_d(self):
        # these are not syntactically valid
        with self.assertRaises(se): d.a
        with self.assertRaises(se): d.A | deriving(Eq)
        with self.assertRaises(se): d.A | d
        with self.assertRaises(se): d.A | d.B | d
        with self.assertRaises(se): d.A | "a"
        with self.assertRaises(te): deriving("a")
        with self.assertRaises(se): deriving(Eq, Show) | d.B
        with self.assertRaises(se): deriving(Eq, Show) & d.B
        with self.assertRaises(se): d.A("a", "b") & deriving
        with self.assertRaises(se): d.A("a", "b") & Show
        with self.assertRaises(te): deriving(1, 2)

        # these should all work fine
        self.assertIsNotNone(d.A)
        self.assertIsNotNone(d.A("a"))
        self.assertIsNotNone(d.A("a", "b", "c"))
        self.assertIsNotNone(d.A("a") | d.B("b"))
        self.assertIsNotNone(d.A("a") | d.B)
        self.assertIsNotNone(d.B | d.A("a"))
        self.assertIsNotNone(d.B | d.A)
        self.assertIsNotNone(d.A("a") | d.B("b") | d.C("a"))
        self.assertIsNotNone(d.A("a", "b") & deriving(Eq, Show))
        self.assertIsNotNone(d.A("a") | d.B("b") & deriving(Eq, Show))

    def test_adts(self):
        """Assorted ADT tests that don't fit anywhere else"""
        T, M1, M2, M3 =\
        data.T("a", "b") == d.M1("a") | d.M2("b") | d.M3 & deriving(Eq)

        self.assertEqual(M1(20), M1(20))
        self.assertEqual(M2(20), M2(20))
        self.assertNotEqual(M1(20), M1(21))
        self.assertNotEqual(M2(20), M2(21))
        self.assertNotEqual(M1(2), M2(2))
        self.assertNotEqual(M1(2), M2("a"))
        self.assertNotEqual(M1(2), M3)
        self.assertEqual(M3, M3)
        self.assertFalse(M3 != M3)
        with self.assertRaises(te): M1("a") == M1(3.0)

        A, B, C =\
        data.A == d.B(str, str) | d.C(str) & deriving(Show, Eq)
        self.assertTrue(has_instance(A, Show))
        self.assertTrue(has_instance(A, Eq))
        self.assertEqual("B('a', 'b')", str(B("a", "b")))
        self.assertEqual("C('a')", str(C("a")))
        self.assertEqual(B("a", "b"), B("a", "b"))
        self.assertEqual(C("a"), C("a"))
        self.assertNotEqual(B("a", "b"), B("a", "c"))
        self.assertNotEqual(C("b"), C("c"))
        self.assertNotEqual(C("b"), B("b", "c"))
        with self.assertRaises(te): M1("a") == C("a")

        # make sure everything works with only 1 constructor
        A, B =\
        data.A == d.B(str, str) & deriving(Show, Eq)
        self.assertTrue(has_instance(A, Show))
        self.assertTrue(has_instance(A, Eq))
        self.assertEqual("B('a', 'b')", str(B("a", "b")))
        self.assertEqual(B("a", "b"), B("a", "b"))
        self.assertNotEqual(B("a", "b"), B("a", "c"))

        # make sure everything works with a bunch of constructors
        X, X1, X2, X3, X4, X5, X6 =\
        data.X == d.X1 | d.X2 | d.X3 | d.X4 | d.X5 | d.X6 & deriving(Eq, Ord)
        self.assertTrue(X1 != X2 and X2 != X3 and X3 != X4 and X4 != X5 and \
                X4 != X5 and X5 != X6)
        self.assertTrue(X1 < X2 < X3 < X4 < X5 < X6)
        with self.assertRaises(te): X1 < A("a", "a")
        with self.assertRaises(te): data.X == d.A | d.B & deriving(Show, 1)


class TestBuiltins(unittest.TestCase):

    def test_show(self):
        from hask.Prelude import show
        self.assertEqual('1', show(1))
        self.assertEqual("'a'", show("a"))
        self.assertEqual("[1, 2]", show([1, 2]))
        self.assertEqual("{'a': 1}", show({"a": 1}))

    def test_enum(self):
        from hask.Prelude import fromEnum, succ, pred
        self.assertEqual(1, fromEnum(1))
        self.assertEqual("b", succ("a"))
        self.assertEqual("a", pred("b"))
        self.assertEqual(2, succ(1))
        self.assertEqual(1, pred(2))
        self.assertEqual(0, pred(pred(2)))
        self.assertEqual(-1, pred(pred(pred(2))))
        self.assertEqual(4, succ(succ(succ(1))))

    def test_numerics(self):
        self.assertTrue(has_instance(int, Num))
        self.assertTrue(has_instance(long, Num))
        self.assertTrue(has_instance(float, Num))
        self.assertTrue(has_instance(complex, Num))


class TestList(unittest.TestCase):

    def test_instances(self):
        self.assertTrue(has_instance(List, Show))
        self.assertTrue(has_instance(List, Eq))
        self.assertTrue(has_instance(List, Ord))
        self.assertTrue(has_instance(List, Functor))
        self.assertTrue(has_instance(List, Applicative))
        self.assertTrue(has_instance(List, Monad))
        self.assertTrue(has_instance(List, Foldable))
        #self.assertTrue(has_instance(List, Traversable))

        self.assertFalse(has_instance(List, Typeclass))
        self.assertFalse(has_instance(List, Num))

    def test_eq(self):
        self.assertEqual(L[[]], L[[]])
        self.assertEqual(L[[1, 2]], L[[1, 2]])
        self.assertEqual(L[1, 2], L[1, 2])
        self.assertEqual(L[1, 2], L[[1, 2]])
        self.assertEqual(L[range(10)], L[range(10)])
        self.assertEqual(L[range(5)], L[0, 1, 2, 3, 4])
        self.assertEqual(L[range(10)], L[xrange(10)])
        self.assertEqual(L[xrange(10)], L[xrange(10)])
        self.assertEqual(L[xrange(5)], L[0, 1, 2, 3, 4])
        self.assertEqual(L[(i for i in range(5))], L[(i for i in range(5))])
        self.assertEqual(L[(i for i in range(5))], L[0, 1, 2, 3, 4])
        self.assertEqual(L[(i for i in [])], L[[]])
        self.assertEqual(L[1, ..., 20], L[1, ..., 20])
        self.assertEqual(L[1, 4, ..., 20], L[1, 4, ..., 20])
        self.assertNotEqual(L[1, 2], L[[]])
        self.assertNotEqual(L[1, 2], L[[1]])
        self.assertNotEqual(L[1, 2], L[1, 2, 3])
        self.assertNotEqual(L[1, 2], L[2, 2])
        with self.assertRaises(te): L["a", "b"] == L[1, 2]

        # with infinite lists
        self.assertNotEqual(L[1, ...], L[0,...])
        self.assertNotEqual(L[1, 3, ...], L[1, 4, ...])
        self.assertNotEqual(L[1, 4], L[1, 4, ...])
        with self.assertRaises(te): L["a", "b"] == L[1, ...]

    def test_ord(self):
        self.assertTrue(L[[]] < L[2, 1])
        self.assertTrue(L[1, 2] < L[2, 1])
        self.assertTrue(L[1, 2] < L[2, 1, 3])
        self.assertTrue(L[1, 2] < L[2, ...])
        self.assertFalse(L[2, 1] < L[[]])
        self.assertFalse(L[2, 1] < L[1, 2])
        self.assertFalse(L[2, 1] < L[1, 1, 1])
        self.assertFalse(L[2, 1] < L[1, ...])
        self.assertTrue(L[[]] <= L[2, 1])
        self.assertTrue(L[1, 2] <= L[2, 1])
        self.assertTrue(L[1, 2] <= L[2, 1, 3])
        self.assertTrue(L[1, 2] <= L[2, ...])
        self.assertFalse(L[2, 1] <= L[[]])
        self.assertFalse(L[2, 1] <= L[1, 2])
        self.assertFalse(L[2, 1] <= L[1, 1, 1])
        self.assertFalse(L[2, 1] <= L[1, ...])

        self.assertFalse(L[[]] > L[2, 1])
        self.assertFalse(L[1, 2] > L[2, 1])
        self.assertFalse(L[1, 2] > L[2, 1, 3])
        self.assertFalse(L[1, 2] > L[2, ...])
        self.assertTrue(L[2, 1] > L[[]])
        self.assertTrue(L[2, 1] > L[1, 2])
        self.assertTrue(L[2, 1] > L[1, 1, 1])
        self.assertTrue(L[2, 1] > L[1, ...])
        self.assertFalse(L[[]] >= L[2, 1])
        self.assertFalse(L[1, 2] >= L[2, 1])
        self.assertFalse(L[1, 2] >= L[2, 1, 3])
        self.assertFalse(L[1, 2] >= L[2, ...])
        self.assertTrue(L[2, 1] >= L[[]])
        self.assertTrue(L[2, 1] >= L[1, 2])
        self.assertTrue(L[2, 1] >= L[1, 1, 1])
        self.assertTrue(L[2, 1] >= L[1, ...])

        self.assertFalse(L[1, 2] < L[1, 2])
        self.assertFalse(L[1, 2] > L[1, 2])
        self.assertTrue(L[1, 2] <= L[1, 2])
        self.assertTrue(L[1, 2] <= L[1, 2])

        self.assertTrue(L[1, 2] + L[3, ...] > L[1, 2, 3] + L[2, ...])
        self.assertTrue(L[1, 2] + L[3, ...] >= L[1, 2, 3] + L[2, ...])
        self.assertTrue(L[1, 2, 3] + L[1, ...] < L[1, 2] + L[3, ...])
        self.assertTrue(L[1, 2, 3] + L[1, ...] <= L[1, 2] + L[3, ...])
        self.assertFalse(L[1, 2] + L[3, ...] < L[1, 2, 3] + L[2, ...])
        self.assertFalse(L[1, 2] + L[3, ...] <= L[1, 2, 3] + L[2, ...])
        self.assertFalse(L[1, 2, 3] + L[1, ...] > L[1, 2] + L[3, ...])
        self.assertFalse(L[1, 2, 3] + L[1, ...] >= L[1, 2] + L[3, ...])

        self.assertTrue(L[1, 2, 3] + L[4, ...] > L[1, 2])
        self.assertTrue(L[1, 2, 3] + L[4, ...] >= L[1, 2])
        self.assertTrue(L[1, 2] < L[1, 2, 3] + L[4, ...])
        self.assertTrue(L[1, 2] <= L[1, 2, 3] + L[4, ...])
        self.assertFalse(L[1, 2] > L[1, 2, 3] + L[4, ...])
        self.assertFalse(L[1, 2] >= L[1, 2, 3] + L[4, ...])
        self.assertFalse(L[1, 2, 3] + L[4, ...] < L[1, 2])
        self.assertFalse(L[1, 2, 3] + L[4, ...] <= L[1, 2])

        with self.assertRaises(te): L[1, 2] > L[1.0, 2.0]
        with self.assertRaises(te): L[1, 2] > L[1.0, 2.0, ...]
        with self.assertRaises(te): L[1, 2] < L[1.0, 2.0]
        with self.assertRaises(te): L[1, 2] < L[1.0, 2.0, ...]
        with self.assertRaises(te): L[1, 2] >= L[1.0, 2.0]
        with self.assertRaises(te): L[1, 2] >= L[1.0, 2.0, ...]
        with self.assertRaises(te): L[1, 2] <= L[1.0, 2.0]
        with self.assertRaises(te): L[1, 2] <= L[1.0, 2.0, ...]

    def test_show(self):
        from hask.Prelude import show
        self.assertEqual("L[[]]", show(L[[]]))
        self.assertEqual("L[[2.0]]", show(L[[2.0]]))
        self.assertEqual("L['a', 'a']", show(L[['a', 'a']]))
        self.assertEqual("L[['a']]", show(L[['a']]))
        self.assertEqual("L[1, 2]", show(L[1, 2]))
        self.assertEqual("L[1, 2]", show(L[[1, 2]]))
        self.assertEqual("L[1, 2, 3]", show(L[1, 2, 3]))
        self.assertEqual("L[1, 2, 3]", show(L[1, 2, 3][:]))

    def test_cons(self):
        self.assertEqual(L[[1]], 1 ^ L[[]])
        self.assertEqual(L[1, 2, 3], 1 ^ (2 ^ L[[3]]))
        self.assertEqual(L[0, 1, 2], (0 ^ L[1, ...])[:3])
        self.assertEqual(L[True, False, True], True ^ (False ^ L[[True]]))
        with self.assertRaises(te): "a" ^ L[2, 4]
        with self.assertRaises(te): True ^ L[2, 4]
        with self.assertRaises(te): "a" ^ L[(i for i in range(20))]
        with self.assertRaises(te): L[1, "a"]

    def test_extend(self):
        self.assertEqual(L[1, 2, 3, 4], L[[1, 2]] + L[[3, 4]])
        self.assertEqual(L[1, 2, 3, 4, 5], L[1, 2] + L[3, 4] + L[[5]])
        self.assertEqual(L[1, 2, 3, 4, 5], L[1, 2] + L[[]] + L[3, 4, 5])
        self.assertEqual(L[1, ..., 10], (L[1, ...] + L[0, ...])[:10])
        with self.assertRaises(te): L[1.0, 2.0] + L[3, 4]
        with self.assertRaises(te): L[1.0, 2.0] + [3, 4]
        with self.assertRaises(te): L[(i for i in "abc")] + L[1, 2]

    def test_indexing(self):
        ie = IndexError

        # regular indexing
        self.assertEqual(3, L[range(10)][3])
        self.assertEqual(3, L[range(4)][-1])
        self.assertEqual(3, L[(i for i in range(10))][3])
        self.assertEqual(3, L[(i for i in range(4))][-1])
        self.assertEqual(2, L[[0, 1, 2, 3]][2])
        self.assertEqual(2, L[[0, 1, 2, 3]][-2])
        self.assertEqual(1, L[(0, 1, 2, 3)][1])
        self.assertEqual(1, L[(0, 1, 2, 3)][-3])
        with self.assertRaises(ie): L[((0, 1, 2))][3]
        with self.assertRaises(ie): L[((0, 1, 2))][-4]
        with self.assertRaises(ie): L[((i for i in range(3)))][3]
        with self.assertRaises(ie): L[((i for i in range(3)))][-4]

        # slice indexing
        self.assertEqual(L[1, 2, 3], L[1, 2, 3, 4][:3])
        self.assertEqual(L[1, 2, 3], L[1, 2, 3][:3])
        self.assertEqual(L[1, 2, 3], L[1, 2, 3][:4])
        self.assertEqual(L[[]], L[1, 2, 3][:-4])
        self.assertEqual(L[2, 3], L[1, 2, 3, 4][1:3])
        self.assertEqual(L[2, 3, 4], L[1, 2, 3, 4][1:4])
        self.assertEqual(L[[2]], L[1, 2, 3][1:-1])
        self.assertEqual(L[[]], L[1, 2, 3][1:-4])
        self.assertEqual(L[2, 3, 4], L[1, 2, 3, 4][1:])
        self.assertEqual(L[[]], L[1, 2, 3, 4][4:])
        self.assertEqual(L[[]], L[1, 2, 3, 4][9:])
        self.assertEqual(L[3, 2, 1], L[1, 2, 3][::-1])
        self.assertEqual(L[2, 1], L[1, 2, 3][1::-1])
        self.assertEqual(L[[]], L[1, 2, 3][:4:-1])
        self.assertEqual(L[[3]], L[1, 2, 3][:1:-1])

    def test_list_comp(self):
        # numeric lists
        self.assertEqual(10, len(L[0, ...][:10]))
        self.assertEqual(L[0, ...][:10], L[range(10)])
        self.assertEqual(L[-10, ...][:10], L[range(-10, 0)])
        self.assertEqual(11, len(L[-5, ..., 5]))
        self.assertEqual(L[-5, ..., 5], L[range(-5, 6)])
        self.assertEqual(L[-5, -4, ..., 5], L[range(-5, 6)])
        self.assertEqual(L[-5, -3, ..., 5], L[range(-5, 6, 2)])
        self.assertEqual(L[1, 3, 5, 7], L[1, 3, ...][:4])
        self.assertEqual(L[3, 5, 7], L[1, 3, ...][1:4])
        self.assertEqual(L[5, 7], L[1, 3, ...][2:4])
        self.assertEqual(L[[]], L[1, 3, ...][4:4])
        self.assertEqual(L[[]], L[1, 3, ...][5:4])
        self.assertEqual(L[1, 3, 5, 7], L[1, 3, ..., 7])
        self.assertEqual(L[1, 3, 5, 7], L[1, 3, ..., 8])
        self.assertEqual(L[2, 3], L[1,...][1:][:2])
        self.assertEqual(L[2, 7, ..., 4], L[[2]])
        self.assertEqual(L[[2]], L[2, 3, ..., 2])
        self.assertEqual(L[2, 3], L[2, 3, ..., 3])

        # decreasing lists
        self.assertEqual(L[5, 4, ...][:10], L[range(5, -5, -1)])
        self.assertEqual(L[5, 3, ...][:10], L[range(5, -15, -2)])
        self.assertEqual(L[5, ..., 1], L[5, 4, 3, 2, 1])
        self.assertEqual(L[5, 3, ..., -5], L[5, 3, 1, -1, -3, -5])
        self.assertEqual(L[[]], L[2, 3, ..., 1])
        self.assertEqual(L[[]], L[2, 2, ..., 1])

        # character lists
        self.assertEqual(10, len(L["a", ...][:10]))
        self.assertEqual("abcdefghij", "".join(L["a", ...][:10]))
        self.assertEqual(11, len(L["a", ..., "k"]))

        with self.assertRaises(se): L[1, 2, 3, ...]
        with self.assertRaises(se): L[..., 2]
        with self.assertRaises(se): L[1, ..., 10, 11]

    def test_contains(self):
        self.assertTrue(1 in L[2, 3, 1])
        self.assertFalse(1 not in L[2, 3, 1])
        self.assertTrue(4 not in L[2, 3, 1])
        self.assertFalse(4 in L[2, 3, 1])
        self.assertTrue(55 in L[1,...])
        self.assertFalse(4 in L[1, 3, ..., 19])
        self.assertTrue(4 not in L[1, 3, ..., 19])

        with self.assertRaises(te): "b" in L[1, ...]
        self.assertEqual(1, L["a", "b", "a"].count("b"))
        self.assertEqual(2, L["a", "b", "a"].count("a"))
        self.assertEqual(0, L["a", "b", "a"].count("d"))
        with self.assertRaises(te): L["a", "b", "c"].count(1)
        self.assertEqual(1, L["a", "b", "a"].index("b"))
        self.assertEqual(0, L["a", "b", "a"].index("a"))
        with self.assertRaises(ve): L["a", "b", "c"].index("d")
        with self.assertRaises(te): L["a", "b", "c"].index(1)

    def test_functor(self):
        from hask.Prelude import id, map, fmap
        f = (lambda x: x ** 2 - 1) ** (H/ int >> int)
        g = (lambda y: y / 4 + 9) ** (H/ int >> int)

        self.assertEqual(L[0, 3, 8, 15], fmap(f, L[1, ..., 4]))
        self.assertEqual(L[0, 3, 8, 15], fmap(f, L[1, ...])[:4])
        self.assertEqual(L[0, 3, 8, 15], f * L[1, ..., 4])
        self.assertEqual(L[0, 3, 8, 15], (f * L[1, ...])[:4])

        # functor laws
        self.assertEqual(L[range(10)], fmap(id, L[range(10)]))
        self.assertEqual(L[range(10)], fmap(id, L[0, ...][:10]))
        self.assertEqual(fmap(f * g, L[range(20)]),
                         fmap(f, fmap(g, L[range(20)])))
        self.assertEqual(fmap(f * g, L[7, ...])[:20],
                         fmap(f, fmap(g, L[7, ...]))[:20])

    def test_monad(self):
        @sig(H/ "a" >> ["a"])
        def double(x):
            return L[x, x]

        self.assertEqual(L[[]], L[[]] >> double)
        self.assertEqual(L[1, 1], L[[1]] >> double)
        self.assertEqual(L[1, 1, 2, 2], L[1, 2] >> double)
        self.assertEqual(L[1, 1, 1, 1, 2, 2, 2, 2],
                         L[1, 2] >> double >> double)

        @sig(H/ "a" >> ["a"])
        def single(x):
            return L[[x]]

        composed_double = (lambda x: double(x) >> double) ** (H/ "a" >> ["a"])

        # monad laws
        self.assertEqual(L[[]], L[[]] >> single)
        self.assertEqual(L[[1]], L[[1]] >> single)
        self.assertEqual(L[1, ..., 20], L[1, ..., 20] >> single)
        self.assertEqual(L[1, 1, 1, 1, 2, 2, 2, 2],
                         (L[1, 2] >> double) >> double)
        self.assertEqual(L[1, 1, 1, 1, 2, 2, 2, 2],
                         L[1, 2] >> (composed_double))

    def test_len(self):
        self.assertEqual(0, len(L[[]]))
        self.assertEqual(0, len(L[None]))
        self.assertEqual(1, len(L[None,]))
        self.assertEqual(3, len(L[1, 2, 3]))
        self.assertEqual(20, len(L[0, ..., 19]))


class Test_README_Examples(unittest.TestCase):
    """Make sure the README examples are all working"""

    def test_list(self):
        self.assertEqual([1, 2, 3], list(L[1, 2, 3]))
        my_list = ["a", "b", "c"]
        self.assertEqual(L["a", "b", "c"], L[my_list])
        self.assertEqual(L[(x**2 for x in range(1, 11))],
            L[1, 4, 9, 16, 25, 36, 49, 64, 81, 100])

        self.assertEqual(L[1, 2, 3], 1 ^ L[2, 3])
        self.assertEqual("goodnight" ^ ("sweet" ^ ("prince" ^ L[[]])),
            L["goodnight", "sweet", "prince"])
        with self.assertRaises(te): "a" ^ L[1.0, 10.3]
        self.assertEqual(L[1, 2] + L[3, 4], L[1, 2, 3, 4])

        from hask.Data.List import take
        self.assertEqual(take(5, L["a", "b", ...]),
                         L['a', 'b', 'c', 'd', 'e'])

        self.assertEqual(L[1,...][5:10],
                         L[6, 7, 8, 9, 10])

        from hask.Data.List import map
        from hask.Data.Char import chr
        letters = map(chr, L[97, ...])
        self.assertEqual(letters[:9],
                          L['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'])

        self.assertTrue(55 in L[1, 3, ...])

    def test_ADT(self):
        FooBar, Foo, Bar =\
        data.FooBar("a", "b") == d.Foo("a", "b", str) | d.Bar
        self.assertIsNotNone(Foo(1, 2, "s"))

    def test_sig(self):
        @sig(H/ "a" >> "b" >> "a")
        def const(x, y):
            return x
        self.assertEqual(const(1, 2), 1)

        def const(x, y):
            return x
        const = const ** (H/ "a" >> "b" >> "a")
        self.assertEqual(const(1, 2), 1)

        f = (lambda x, y: x + y) ** (H/ int >> int >> int)
        self.assertEqual(5, f(2, 3))
        with self.assertRaises(te): f(9, 1.0)

        g = (lambda a, b, c: a / (b + c)) ** (H/ int >> int >> int >> int)
        self.assertEqual(g(10, 2, 3), 2)
        part_g = g(12)
        self.assertEqual(part_g(2, 2), 3)
        self.assertEqual(g(20, 1)(4), 4)
        self.assertEqual(Just * Just * Just * Just % 77, Just(Just(Just(Just(77)))))

        # add two ints together
        @sig(H/ int >> int >> int)
        def add(x, y):
            return x + y

        # reverse order of arguments to a function
        @sig(H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
        def flip(f, b, a):
            return f(a, b)

        # map a Python (untyped) function over a Python (untyped) set
        @sig(H/ func >> set >> set)
        def set_map(fn, lst):
            return set((fn(x) for x in lst))

        # map a typed function over a List
        @sig(H/ (H/ "a" >> "b") >> ["a"] >> ["b"])
        def map(f, xs):
            return L[(f(x) for x in xs)]

        # type signature with an Eq constraint
        @sig(H[(Eq, "a")]/ "a" >> ["a"] >> bool)
        def not_in(y, xs):
            return not any((x == y for x in xs))

        # type signature with a type constructor (Maybe) that has type arguments
        @sig(H/ int >> int >> t(Maybe, int))
        def safe_div(x, y):
            return Nothing if y == 0 else Just(x/y)

        # type signature for a function that returns nothing
        @sig(H/ int >> None)
        def launch_missiles(num_missiles):
            return

        Ratio, R =\
                data.Ratio("a") == d.R("a", "a") & deriving(Eq)

        Rational = t(Ratio, int)


        @sig(H/ Rational >> Rational >> Rational)
        def addRational(rat1, rat2):
            pass

        from hask.Prelude import flip
        h = (lambda x, y: x / y) ** (H/ float >> float >> float)
        self.assertEqual(h(3.0) * h(6.0) * flip(h, 2.0) % 36.0, 9.0)

    def test_match(self):
        @sig(H/ int >> int)
        def fib(x):
            return ~(caseof(x)
                        | m(0)   >> 1
                        | m(1)   >> 1
                        | m(m.n) >> fib(p.n - 2) + fib(p.n - 1)
                    )

        self.assertEqual(1, fib(0))
        self.assertEqual(1, fib(1))
        self.assertEqual(13, fib(6))

        def default_to_zero(x):
            return ~(caseof(x)
                        | m(Just(m.x)) >> p.x
                        | m(Nothing)   >> 0)

        self.assertEqual(default_to_zero(Just(27)), 27)
        self.assertEqual(default_to_zero(Nothing), 0)
        self.assertEqual(Just(20.0)[0], 20.0)
        self.assertEqual(Left("words words words words")[0], "words words words words")
        with self.assertRaises(IndexError): Nothing[0]

    def test_typeclasses(self):
        from hask.Prelude import fmap
        M, N, J = data.M("a") == d.N | d.J("a") & deriving(Show, Eq, Ord)

        def maybe_fmap(fn, maybe_value):
            return ~(caseof(maybe_value)
                        | m(N)      >> N
                        | m(J(m.x)) >> J(fn(p.x))
                    )

        instance(Functor, M).where(
            fmap = maybe_fmap
        )

        times2 = (lambda x: x * 2) ** (H/ int >> int)
        toFloat = float ** (H/ int >> float)

        self.assertEqual(fmap(toFloat, J(10)), J(10.0))
        self.assertEqual(fmap(toFloat, fmap(times2, J(25))), J(50.0))
        self.assertEqual((toFloat * times2) * J(25), J(50.0))
        self.assertEqual((toFloat * times2) * N, N)

        instance(Applicative, M).where(
            pure = J
        )

        instance(Monad, M).where(
            bind = lambda x, f: ~(caseof(x)
                                    | m(J(m.a)) >> f(p.a)
                                    | m(N)   >> N)
        )

        @sig(H/ int >> int >> t(M, int))
        def safe_div(x, y):
            return N if y == 0 else J(x/y)

        from hask.Prelude import flip
        divBy = flip(safe_div)
        self.assertEqual(J(9) >> divBy(3), J(3))

        self.assertEqual(Just(12) >> divBy(2) >> divBy(2) >> divBy(3), J(1))
        self.assertEqual(J(12) >> divBy(0) >> divBy(6), N)

        from hask.Data.List import replicate
        self.assertEqual(L[1, 2] >> replicate(2) >> replicate(2),
                L[1, 1, 1, 1, 2, 2, 2, 2])

        class Person(object):
            def __init__(self, name, age):
                self.name = name
                self.age = age

        instance(Eq, Person).where(
            eq = lambda p1, p2: p1.name == p2.name and p1.age == p2.age
        )

        self.assertFalse(Person("Philip Wadler", 59) == Person("Simon Peyton Jones", 57))

    def test_sections(self):
        f = (__ - 20) * (2 ** __) * (__ + 3)
        self.assertEqual(8172, f(10))
        self.assertEqual("Hello world", (__+__)('Hello ', 'world'))
        self.assertEqual(1024, (__**__)(2)(10))

    def test_guard(self):
        porridge_tempurature = 80
        self.assertEqual(
                ~(guard(porridge_tempurature)
                    | c(__ < 20)  >> "Porridge is too cold!"
                    | c(__ < 90)  >> "Porridge is just right!"
                    | c(__ < 150) >> "Porridge is too hot!"
                    | otherwise   >> "Porridge has gone thermonuclear"
                ),
                'Porridge is just right!')

        def examine_password_security(password):
            analysis = ~(guard(password)
                | c(lambda x: len(x) > 20) >> "Wow, that's one secure password"
                | c(lambda x: len(x) < 5)  >> "You made Bruce Schneier cry"
                | c(__ == "12345")         >> "Same combination as my luggage!"
                | otherwise                >> "Hope it's not `password`"
            )
            return analysis

        nuclear_launch_code = "12345"
        self.assertEqual(
                examine_password_security(nuclear_launch_code),
                'Same combination as my luggage!')

    def test_decorators(self):
        def eat_cheese(cheese):
            if cheese <= 0:
                raise ValueError("Out of cheese error")
            return cheese - 1

        maybe_eat = in_maybe(eat_cheese)
        self.assertEqual(maybe_eat(1), Just(0))
        self.assertEqual(maybe_eat(0), Nothing)
        self.assertEqual(Just(6), Just(7) >> maybe_eat)
        self.assertEqual(Just(7),
                         Just(10) >> maybe_eat >> maybe_eat >> maybe_eat)
        self.assertEqual(Nothing,
                         Just(1) >> maybe_eat >> maybe_eat >> maybe_eat)

        either_eat = in_either(eat_cheese)
        self.assertEqual(either_eat(10), Right(9))
        self.assertTrue(isinstance(either_eat(0)[0], ValueError))

    def test_examples(self):
        @sig(H/ int >> int >> t(Maybe, int))
        def safe_div(x, y):
            return Nothing if y == 0 else Just(x/y)

        from hask.Data.Maybe import mapMaybe
        self.assertEqual(mapMaybe(safe_div(12)) % L[0, 1, 3, 0, 6],
                         L[12, 4, 2])

        from hask.Data.List import isInfixOf
        self.assertTrue(isInfixOf(L[2, 8], L[1, 4, 6, 2, 8, 3, 7]))

        from hask.Control.Monad import join
        self.assertEqual(join(Just(Just(1))), Just(1))

        from hask.Prelude import flip
        from hask.Data.Tuple import snd
        from hask.Python.builtins import divmod, hex

        hexMod = hex * snd * flip(divmod, 16)
        self.assertEqual(hexMod(24), '0x8')


if __name__ == '__main__':
    unittest.main()
