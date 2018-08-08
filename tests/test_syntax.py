import unittest

from hask import __
from hask import TypeSignatureError
from hask import NoGuardMatchException
from hask import IncompletePatternError
from hask import caseof, guard, otherwise
from hask import H, c, m, t, sig, p
from hask import Just, Nothing, Maybe, Either
from hask import GT, EQ, LT, Ordering, Eq, L


te = TypeError
ve = ValueError


class TestSyntax(unittest.TestCase):

    def test_syntax(self):
        from hask.lang.syntax import Syntax
        s = Syntax()
        s.invalid_syntax_message = "err"
        with self.assertRaises(SyntaxError):
            len(s)
        with self.assertRaises(SyntaxError):
            s[0]
        with self.assertRaises(SyntaxError):
            s[1]
        with self.assertRaises(SyntaxError):
            del s["foo"]
        with self.assertRaises(SyntaxError):
            iter(s)
        with self.assertRaises(SyntaxError):
            reversed(s)
        with self.assertRaises(SyntaxError):
            1 in s
        with self.assertRaises(SyntaxError):
            1 not in s
        with self.assertRaises(SyntaxError):
            s("f")
        with self.assertRaises(SyntaxError):
            with s:
                pass
        with self.assertRaises(SyntaxError):
            s > 0
        with self.assertRaises(SyntaxError):
            s < 0
        with self.assertRaises(SyntaxError):
            s >= 0
        with self.assertRaises(SyntaxError):
            s <= 0
        with self.assertRaises(SyntaxError):
            s == 0
        with self.assertRaises(SyntaxError):
            s != 0
        with self.assertRaises(SyntaxError):
            abs(s)
        with self.assertRaises(SyntaxError):
            ~s
        with self.assertRaises(SyntaxError):
            +s
        with self.assertRaises(SyntaxError):
            -s
        with self.assertRaises(SyntaxError):
            s + 1
        with self.assertRaises(SyntaxError):
            s - 1
        with self.assertRaises(SyntaxError):
            s * 1
        with self.assertRaises(SyntaxError):
            s ** 1
        with self.assertRaises(SyntaxError):
            s / 1
        with self.assertRaises(SyntaxError):
            s % 1
        with self.assertRaises(SyntaxError):
            divmod(s, 1)
        with self.assertRaises(SyntaxError):
            s << 1
        with self.assertRaises(SyntaxError):
            s >> 1
        with self.assertRaises(SyntaxError):
            s & 1
        with self.assertRaises(SyntaxError):
            s | 1
        with self.assertRaises(SyntaxError):
            s ^ 1
        with self.assertRaises(SyntaxError):
            1 + s
        with self.assertRaises(SyntaxError):
            1 - s
        with self.assertRaises(SyntaxError):
            1 * s
        with self.assertRaises(SyntaxError):
            1 ** s
        with self.assertRaises(SyntaxError):
            1 / s
        with self.assertRaises(SyntaxError):
            1 % s
        with self.assertRaises(SyntaxError):
            1 << s
        with self.assertRaises(SyntaxError):
            1 >> s
        with self.assertRaises(SyntaxError):
            1 & s
        with self.assertRaises(SyntaxError):
            1 | s
        with self.assertRaises(SyntaxError):
            1 ^ s
        with self.assertRaises(SyntaxError):
            s += 1
        with self.assertRaises(SyntaxError):
            s -= 1
        with self.assertRaises(SyntaxError):
            s *= 1
        with self.assertRaises(SyntaxError):
            s **= 1
        with self.assertRaises(SyntaxError):
            s /= 1
        with self.assertRaises(SyntaxError):
            s %= 1
        with self.assertRaises(SyntaxError):
            s <<= 1
        with self.assertRaises(SyntaxError):
            s >>= 1
        with self.assertRaises(SyntaxError):
            s &= 1
        with self.assertRaises(SyntaxError):
            s |= 1
        with self.assertRaises(SyntaxError):
            s ^= 1

    def test_section(self):
        """Operator sections (e.g. `(1+__)` )"""

        # basic sections
        self.assertEqual(4, (__ + 1)(3))
        self.assertEqual(4, (1 + __)(3))
        self.assertEqual(3, (__ - 5)(8))
        self.assertEqual(3, (8 - __)(5))
        self.assertEqual(8, (__ * 2)(4))
        self.assertEqual(8, (2 * __)(4))
        self.assertEqual(1, (__ % 4)(5))
        self.assertEqual(1, (5 % __)(4))

        self.assertTrue((__ < 4)(3))
        self.assertTrue((5 < __)(9))
        self.assertTrue((__ > 4)(5))
        self.assertTrue((5 > __)(4))
        self.assertTrue((__ == 4)(4))
        self.assertTrue((5 == __)(5))
        self.assertTrue((__ != 4)(3))
        self.assertTrue((5 != __)(8))
        self.assertTrue((__ >= 4)(5))
        self.assertTrue((5 >= __)(5))
        self.assertTrue((__ <= 4)(4))
        self.assertTrue((5 <= __)(8))
        self.assertFalse((__ < 4)(4))
        self.assertFalse((5 < __)(2))
        self.assertFalse((__ > 4)(3))
        self.assertFalse((5 > __)(5))
        self.assertFalse((__ == 4)(9))
        self.assertFalse((5 == __)(8))
        self.assertFalse((__ != 4)(4))
        self.assertFalse((5 != __)(5))
        self.assertFalse((__ >= 4)(1))
        self.assertFalse((5 >= __)(6))
        self.assertFalse((__ <= 4)(6))
        self.assertFalse((5 <= __)(4))

        # double sections
        self.assertEqual(3, (__+__)(1, 2))
        self.assertEqual(1, (__-__)(2, 1))
        self.assertEqual(4, (__*__)(1, 4))
        self.assertEqual(3, (__/__)(12, 4))
        self.assertEqual(3, (__+__)(1)(2))
        self.assertEqual(1, (__-__)(2)(1))
        self.assertEqual(4, (__*__)(1)(4))
        self.assertEqual(3, (__/__)(12)(4))

        # sections composed with `fmap`
        self.assertEqual(12, ((__*4) * (__+2) * (1+__))(0))
        self.assertEqual(2, (__+1) * (__/2) * (2-__) % 0)
        self.assertEqual(4, (__ + 1) * (__ * 3) % 1)

    def test_guard(self):
        me = NoGuardMatchException

        self.assertTrue(~(guard(1)
            | c(lambda x: x == 1) >> True
            | otherwise           >> False))
        self.assertFalse(~(guard(2)
            | c(lambda y: y == 1) >> True
            | otherwise           >> False))
        self.assertFalse(~(guard(2)
            | otherwise >> False))
        self.assertFalse(~(guard(2)
            | otherwise           >> False
            | c(lambda x: x == 2) >> True))
        self.assertEqual("foo", ~(guard(1)
            | c(lambda x: x > 1)  >> "bar"
            | c(lambda x: x < 1)  >> "baz"
            | c(lambda x: x == 1) >> "foo"
            | otherwise           >> "Err"))

        with self.assertRaises(ve):
            ~(guard(2) | c(1) >> 1)
        with self.assertRaises(me):
            ~(guard(1) | c(lambda x: x == 2) >> 1)

        # syntax checks
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) + c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) - c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) * c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) / c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) % c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) ** c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) << c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) & c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) ^ c(lambda _: 1)

        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) >> c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) >> 2 >> 2
        with self.assertRaises(SyntaxError):
            c(lambda x: x > 1) | c(lambda x: x < 1)
        with self.assertRaises(SyntaxError):
            otherwise >> c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            otherwise | c(lambda x: x < 1)
        with self.assertRaises(SyntaxError):
            otherwise >> c(lambda _: 1)
        with self.assertRaises(SyntaxError):
            otherwise | c(lambda x: x < 1)
        with self.assertRaises(SyntaxError):
            ~(guard(2) | c(lambda x: x == 2) >> 1 | c(lambda y: y == 2))
        with self.assertRaises(SyntaxError):
            c(lambda x: x == 10) >> "1" >> "2"
        with self.assertRaises(SyntaxError):
            "1" >> c(lambda x: x == 10)
        with self.assertRaises(SyntaxError):
            guard(1) | c(lambda x: x > 1)
        with self.assertRaises(SyntaxError):
            guard(1) | (lambda x: x > 1)
        with self.assertRaises(SyntaxError):
            ~guard(1) | (lambda x: x > 1)
        with self.assertRaises(SyntaxError):
            ~guard(1)
        with self.assertRaises(SyntaxError):
            otherwise >> "1" >> "2"
        with self.assertRaises(SyntaxError):
            "1" >> otherwise

    def test_caseof(self):
        # literal matching
        self.assertEqual(1,
                ~(caseof("a")
                    | m("a") >> 1))
        self.assertEqual(1,
                ~(caseof(2.0)
                    | m(2.0) >> ~(caseof("a")
                                    | m("b") >> 3
                                    | m("a") >> 1)
                    | m(2.0) >> 2))
        self.assertEqual("x",
                ~(caseof(Just("x"))
                    | m(Nothing)   >> False
                    | m(Just("x")) >> "x"))
        self.assertEqual(1,
                ~(caseof([1, 2])
                    | m((1, 2)) >> 2
                    | m([1, 2]) >> 1))
        self.assertEqual(True,
                ~(caseof(GT)
                    | m(LT) >> False
                    | m(EQ) >> False
                    | m(GT) >> True))
        self.assertEqual(2,
                ~(caseof((1, 2, 3))
                    | m((1, 2))    >> 1
                    | m((1, 2, 3)) >> 2))

        with self.assertRaises(IncompletePatternError):
            ~(caseof(1) | m(2) >> 2)

        # matches with wildcard
        self.assertEqual(1,
                ~(caseof(1)
                    | m(m._) >> 1
                    | m(1) >> 2))
        self.assertEqual(True,
                ~(caseof(GT)
                    | m(LT) >> False
                    | m(EQ) >> False
                    | m(m._) >> True))
        self.assertEqual(False,
                ~(caseof(GT)
                    | m(LT) >> False
                    | m(m._)  >> False
                    | m(GT) >> True))
        self.assertEqual(2,
                ~(caseof((1, 2, 3))
                    | m((2, 1, 3)) >> 1
                    | m((1, m._, 3)) >> 2
                    | m((1, 2, 3)) >> 3))

        # variable bind
        self.assertEqual(("b", "a"),
                ~(caseof(("a", "b"))
                    | m((m.x, m.y)) >> (p.y, p.x)
                    | m(m._)          >> None))
        self.assertEqual(1,
                ~(caseof(Just(1))
                    | m(Just(m.x)) >> p.x
                    | m(Nothing)   >> 0))
        self.assertEqual(Just(0),
                ~(caseof(Nothing)
                    | m(Just(m.x)) >> Just(p.x + 1)
                    | m(Nothing)   >> Just(0)))
        self.assertEqual(1,
                ~(caseof(2)
                    | m((m.a, m.a)) >> p.a
                    | m(2)          >> 1))
        self.assertEqual(1,
                ~(caseof(Just(10))
                    | m(Just(m.a)) >> ~(caseof(1)
                                            | m(m.a) >> p.a
                                            | m(m._) >> False)
                    | m(Nothing)   >> 11))

        # cons matches
        self.assertEqual([3],
                ~(caseof([1, 2, 3])
                    | m(1 ^ (2 ^ m.x)) >> p.x
                    | m(m.x)           >> False))
        self.assertEqual([3, 2, 1],
                ~(caseof([3, 2, 1])
                    | m(m.a ^ (2 ^ m.c)) >> [p.a, 2, p.c[0]]
                    | m(m.x)             >> False))
        self.assertEqual([3, 2, [1, 0]],
                ~(caseof([3, 2, 1, 0])
                    | m(m.a ^ (m.b ^ m.c)) >> [p.a, p.b, p.c]
                    | m(m.x)               >> False))
        self.assertEqual(L[3, 2, 1],
                ~(caseof(L[3, 2, 1, 0])
                    | m(m.a ^ (m.b ^ m.c)) >> L[p.a, p.b, p.c[0]]
                    | m(m.x)               >> False))
        self.assertEqual(1,
                ~(caseof(L[1, ...])
                    | m(m.a ^ m.b) >> p.a
                    | m(m.a)       >> False))
        self.assertTrue(~(caseof(L[[]])
                            | m(m.a ^ m.b) >> False
                            | m(m.a)       >> True))

        with self.assertRaises(SyntaxError):
            ~(caseof((1, 2))
                | m((m.a, m.a)) >> p.a
                | m(1)          >> 1)
        with self.assertRaises(SyntaxError):
            ~(caseof([1, 2, 3, 4])
                | m(m.a ^ m.b ^ m.c) >> True
                | m(m.x)             >> False)
        with self.assertRaises(SyntaxError):
            ~(caseof(L[1, 2, 2])
                | m(m.a ^ 1) >> False
                | m(m.a)     >> True)

    def test_type_sig(self):
        tse = TypeSignatureError
        x = lambda x: x
        with self.assertRaises(tse):
            x ** (H/ int >> 1)
        with self.assertRaises(tse):
            x ** (H/ int >> [int, int])
        with self.assertRaises(tse):
            x ** (H/ int >> [])
        with self.assertRaises(tse):
            x ** (H/ int >> "AAA")

        with self.assertRaises(te):
            t(Maybe, "a", "b")
        with self.assertRaises(te):
            t(Either, "a")
        with self.assertRaises(te):
            t(Ordering, "a")

        with self.assertRaises(SyntaxError):
            sig(sig(H/ int >> int))
        with self.assertRaises(SyntaxError):
            sig(H)

        with self.assertRaises(SyntaxError):
            H[Eq, "a", "b"]
        with self.assertRaises(SyntaxError):
            H[(Eq, Eq)]
        with self.assertRaises(SyntaxError):
            H[("a", Eq)]
        with self.assertRaises(SyntaxError):
            H[("a", "a")]
        with self.assertRaises(SyntaxError):
            H[(Eq, "a", "b")]
        with self.assertRaises(SyntaxError):
            H[(Eq, 1)]
        with self.assertRaises(SyntaxError):
            H[(Maybe, 1)]
        with self.assertRaises(SyntaxError):
            sig(H/ "a")(1)
