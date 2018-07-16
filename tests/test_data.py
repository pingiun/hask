import unittest
import math

from hask import L
from hask import sig, H
from hask import LT, GT

te = TypeError


class TestDataString(unittest.TestCase):

    def test_string(self):
        from hask.Data.String import lines, words, unlines, unwords
        self.assertEqual(lines("a\nb \n\nc"), L[["a", "b ", "", "c"]])
        self.assertEqual(lines(""), L[[]])
        self.assertEqual(unlines(L[["a", "b ", "", "c"]]), "a\nb \n\nc")
        self.assertEqual(unlines(L[[]]), "")
        self.assertEqual(words(" 1 2  4"), L[["", "1", "2", "", "4"]])
        self.assertEqual(words(""), L[[]])
        self.assertEqual(unwords(L[["", "1", "2", "", "4"]]), " 1 2  4")
        self.assertEqual(unwords(L[[]]), "")


class TestDataChar(unittest.TestCase):

    def test_char(self):
        from hask.Data.Char import ord, chr

        self.assertEqual("a", chr(97))
        with self.assertRaises(te):
            ord(97)
        with self.assertRaises(te):
            chr("a")
        with self.assertRaises(te):
            chr * chr
        for i in range(256):
            self.assertEqual(i, ord * chr % i)


class TestDataNum(unittest.TestCase):

    def test_Num(self):
        from hask.Data.Num import negate, signum, abs
        self.assertEqual(negate(5), -5)
        self.assertEqual(negate(-5), 5)
        self.assertEqual(signum(5), 1)
        self.assertEqual(signum(-5), -1)
        self.assertEqual(signum(0), 0)
        self.assertEqual(abs(5), 5)
        self.assertEqual(abs(-5), 5)

    def test_RealFloat(self):
        from hask.Data.Num import isNaN, isInfinite, isNegativeZero, atan2
        self.assertTrue(isNaN(float("nan")) and not isNaN(1.0))
        self.assertTrue(isInfinite(float("-inf")) and not isInfinite(1.0))
        self.assertTrue(isNegativeZero(-0.0) and not isNegativeZero(0.0))
        self.assertEqual(round(atan2(0.0, 0.0), 5), round(0.0, 5))
        self.assertEqual(round(atan2(0.0, -0.0), 5), round(math.pi, 5))


class TestDataTuple(unittest.TestCase):

    def test_tuple(self):
        from hask.Data.Tuple import fst, snd, curry, uncurry, swap

        self.assertEqual(1, fst((1, 2)))
        self.assertEqual(("a", "b"), fst((("a", "b"), ("c", "d"))))
        self.assertEqual("a", fst(fst((("a", "b"), ("c", "d")))))

        self.assertEqual(2, snd((1, 2)))
        self.assertEqual(("c", "d"), snd((("a", "b"), ("c", "d"))))
        self.assertEqual("b", snd * fst % (("a", "b"), ("c", "d")))
        self.assertEqual("c", fst * snd % (("a", "b"), ("c", "d")))

        self.assertEqual(swap(swap((1, 2))), (1, 2))
        self.assertEqual(swap((1, "a")), ("a", 1))

        @sig(H/ (str, str) >> str)
        def uncurried_fn(tup):
            return tup[0] + tup[1]

        @sig(H/ list >> list >> list)
        def curried_fn(x, y):
            return x + y

        self.assertEqual(uncurry(curried_fn, ([1, 2], [3, 4])), [1, 2, 3, 4])
        self.assertEqual(curry(uncurried_fn, "a", "b"), "ab")
        self.assertEqual(uncurry(curry(uncurried_fn), ("a", "b")), "ab")
        self.assertEqual(curry(uncurry(curried_fn), ["a"], ["b"]), ["a", "b"])


class TestDataOrd(unittest.TestCase):

    def test_ord(self):
        from hask.Data.Ord import max, min, compare, comparing
        self.assertEqual(max(1, 2), 2)
        self.assertEqual(min(1, 2), 1)
        self.assertEqual(compare(1)(2), LT)

        from hask.Data.Tuple import fst, snd
        self.assertEqual(comparing(fst, (1, 2), (3, 0)), LT)
        self.assertEqual(comparing(snd, (1, 2), (3, 0)), GT)


class TestDataRatio(unittest.TestCase):

    def test_ratio(self):
        from hask.Data.Ratio import R, numerator, denominator
        self.assertEqual(1, numerator % R(1, 2))
        self.assertEqual(2, denominator % R(1, 2))
