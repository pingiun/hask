import unittest

from hask import Eq
from hask import H, sig, func
from hask import L
from hask import Just, Nothing
from hask import Left, Right

# internals
from hask.lang.type_system import pattern_match
from hask.lang.type_system import PatternMatchBind

te = TypeError
se = SyntaxError
ve = ValueError


class TestTypeSystem(unittest.TestCase):

    def test_TypedFunc_builtin(self):
        """TypedFunc with builtin types"""

        f = (lambda x: x + 2) ** (H/ int >> int)
        g = (lambda x: x - 5) ** (H/ int >> int)
        h = (lambda x: x * 2) ** (H/ int >> int)
        i = (lambda x: str(x)) ** (H/ int >> str)
        j = (lambda x: x[0]) ** (H/ list >> float)

        # basic type checking
        self.assertEqual(2, f(g(5)))
        self.assertEqual(2, (f * g)(5))
        self.assertEqual(2, f * g % 5)
        self.assertEqual(8, f * f * f % 2)
        self.assertEqual(f(h(g(5))), (f * h * g)(5))
        self.assertEqual((i * h * f)(9), "22")
        self.assertEqual(1., j % [1., 2.])
        with self.assertRaises(te):
            f(4.0)
        with self.assertRaises(te):
            f("4")
        with self.assertRaises(te):
            f(1, 2)

    def test_TypedFunc_var(self):
        @sig(H/ "a" >> "b" >> "a" >> "b")
        def superconst(a, b, c):
            return b

        self.assertEqual(1, superconst([], 1, [1, 2]))
        self.assertEqual(None, superconst([], None, [1, 2]))
        with self.assertRaises(te):
            superconst(1, "a", 1.)

    def test_TypedFunc_tuple(self):
        @sig(H/ (int, "a", str) >> str)
        def pprint(tup):
            return str(tup[0]) + tup[2]

        self.assertEqual("1a", pprint((1, 9., "a")))
        self.assertEqual("1a", pprint((1, object(), "a")))
        with self.assertRaises(te):
            pprint((1, 2, 3))
        with self.assertRaises(te):
            pprint(("1", 2, "3"))
        with self.assertRaises(te):
            pprint((1, 2, 3, 4))
        with self.assertRaises(te):
            pprint((1, 2))

        @sig(H/ ("a", "b") >> ("b", "a"))
        def swap(tup):
            return (tup[1], tup[0])

        self.assertEqual(swap((1, 2)), (2, 1))
        self.assertEqual(swap((1.0, 2)), (2, 1.))
        with self.assertRaises(te):
            swap((1, 2, 3))

    def test_TypedFunc_list(self):
        @sig(H/ [int] >> int)
        def sum1(l):
            return sum(l)

        self.assertEqual(sum1 % L[1, 2, 3], 6)
        with self.assertRaises(te):
            sum1 % L[1., 2., 3.]

        @sig(H/ [["a"]] >> ["a"])
        def flatten(xss):
            return L[(x for xs in xss for x in xs)]

        self.assertEqual(flatten(L[L["a", "b"], L["c", "d"]]),
                         L["a", "b", "c", "d"])
        with self.assertRaises(te):
            flatten(L["a", "b"])

    def test_TypedFunc_None(self):
        @sig(H/ None >> None)
        def n_to_n(n):
            return

        self.assertIsNone(None, n_to_n % None)
        self.assertIsNone(None, n_to_n * n_to_n % None)
        with self.assertRaises(te):
            n_to_n(1)

    def test_TypedFunc_func(self):
        """PyFunc signature type"""

        @sig(H/ func >> func)
        def id_wrap(f):
            return lambda x: f(x)

        lam_test = lambda x: x + "!"

        def f_test(x):
            return x ** 2

        class example(object):
            def meth_test(self, x):
                return (x, x)

            @staticmethod
            def stat_test(x):
                return [x]

        self.assertEqual(id_wrap(lam_test)("woot"), "woot!")
        self.assertEqual(id_wrap(f_test)(2), 4)
        self.assertEqual(id_wrap(example().meth_test)(2), (2, 2))
        self.assertEqual(id_wrap(example.stat_test)(2), [2])

        self.assertEqual((id_wrap * id_wrap % (lambda x: x+1))(9), 10)
        with self.assertRaises(te):
            id_wrap(1)

        @sig(H/ func >> func >> int >> int)
        def composei(f, g, x):
            return f(g(x))

        self.assertEqual(composei(lambda x: x + 2)(lambda x: x * 3)(6), 20)

    def test_TypedFunc_class(self):
        @sig(H[(Eq, "a")]/ "a" >> "a")
        def eq_id(a):
            return a

        self.assertEqual(1, eq_id(1))

    def test_match(self):
        match_only = lambda v, p: pattern_match(v, p)[0]
        pb = PatternMatchBind

        # literal matches
        self.assertTrue(match_only(1, 1))
        self.assertTrue(match_only((1, "a"), (1, "a")))
        self.assertTrue(match_only(Nothing, Nothing))
        self.assertTrue(match_only(Just(1), Just(1)))
        self.assertFalse(match_only(2, 1))
        self.assertFalse(match_only(("a", 1), (1, "a")))
        self.assertFalse(match_only(("a", "b"), ["a", "b"]))
        self.assertFalse(match_only(Nothing, Just(Nothing)))
        self.assertFalse(match_only(Just(2), Just(1)))
        self.assertFalse(match_only(Right(2), Just(2)))
        self.assertFalse(match_only(Right(2), Left(2)))

        # matches with wildcard (i.e, discarded variable bind)
        self.assertTrue(match_only(1, pb("_")))
        self.assertTrue(match_only(Nothing, pb("_")))
        self.assertTrue(match_only(Just("whatever"), Just(pb("_"))))
        self.assertTrue(match_only(Right(Just(5)), Right(Just(pb("_")))))
        self.assertTrue(match_only(("a", "b", "c"), ("a", pb("_"), "c")))
        self.assertFalse(match_only(("a", "b", "c"), ("1", pb("_"), "c")))
        self.assertFalse(match_only(("a", "b", "d"), ("a", pb("_"), "c")))

        # matches with variable binding
        self.assertEqual((True, {"a": 1}), pattern_match(1, pb("a")))
        self.assertEqual((True, {"a": 1, "b": 2}),
                         pattern_match((1, 2), (pb("a"), pb("b"))))
        self.assertEqual((True, {"a": 8}),
                         pattern_match(Just(8), Just(pb("a"))))
        self.assertEqual((True, {"a": "a"}),
                         pattern_match(Right(Just("a")), Right(Just(pb("a")))))
        self.assertEqual((False, {"a": 1}),
                         pattern_match((2, 1), (3, pb("a"))))
        self.assertEqual(
            (True, {"a": 1, "b": 2, "_": "a"}),
            pattern_match((1, "a", 2), (pb("a"), pb("_"), pb("b")))
        )

        with self.assertRaises(se):
            pattern_match((1, 2), (pb("c"), pb("a")), {"c": 1})
        with self.assertRaises(se):
            pattern_match((1, 2), (pb("c"), pb("a")), {"a": 1})
