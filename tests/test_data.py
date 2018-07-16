import unittest
import math

from hask import __
from hask import L
from hask import sig, H, t
from hask import LT, GT

from hask import Nothing, Just, Maybe

te = TypeError
ve = ValueError


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


class TestDataList(unittest.TestCase):

    def test_basic_functions(self):
        from hask.Data.List import head, last, tail, init, uncons, null, length

        self.assertEqual(4, head(L[4, 2]))
        self.assertEqual(1, head(L[1, ...]))
        with self.assertRaises(IndexError):
            head(L[[]])

        self.assertEqual(1, last(L[[1]]))
        self.assertEqual(4, last(L[1, 5, 3, 6, 4]))
        with self.assertRaises(IndexError):
            last(L[[]])

        self.assertEqual(L[[]], tail(L[[1]]))
        self.assertEqual(L[2, 3], tail(L[1, 2, 3]))
        with self.assertRaises(IndexError):
            tail(L[[]])

        self.assertEqual(L[[]], init(L[[1]]))
        self.assertEqual(L[1, 2], init(L[1, 2, 3]))
        with self.assertRaises(IndexError):
            init(L[[]])

        self.assertEqual(Nothing, uncons(L[[]]))
        self.assertEqual(Just % (1, L[[]]), uncons(L[[1]]))
        self.assertEqual(Just % (1, L[2, 3]), uncons(L[1, 2, 3]))

        self.assertTrue(null(L[[]]))
        self.assertFalse(null(L[[1]]))
        self.assertFalse(null(L[1, ...]))

        self.assertEqual(20, length(L[0, ..., 19]))
        self.assertEqual(0, length(L[[]]))

    def test_list_transformations(self):
        from hask.Data.List import map, reverse, intersperse, intercalate  # noqa: F401
        from hask.Data.List import transpose, subsequences, permutations  # noqa: F401

        self.assertEqual(L[1, 2, 1], intersperse(2, L[1, 1]))
        self.assertEqual(L[[]], intersperse(2, L[[]]))

        self.assertEqual(L[[L[[]]]], subsequences(L[[]]))
        self.assertEqual(L[L[[]], L[[1]], L[[2]], L[1, 2]],
                         subsequences(L[1, 2]))

        self.assertEqual(L[L[1, 2], L[2, 1]], permutations(L[1, 2]))
        self.assertEqual(L[[]], permutations(L[[]]))

    def test_reducing_lists(self):
        from hask.Data.List import foldl, foldl_, foldr, foldr1, concat  # noqa: F401
        from hask.Data.List import concatMap, and_, or_, any, all, sum, product  # noqa: F401
        from hask.Data.List import maximum, minimum

        from hask.Data.List import repeat, take

        self.assertEqual(L[1, ..., 6], concat(L[L[1, 2, 3], L[4, 5, 6]]))
        self.assertEqual(L[[]], concat(L[[]]))
        self.assertEqual(L[1, 1, 1, 1], take(4) * concat * repeat % L[[1]])

        self.assertTrue(or_(L[True, True]))
        self.assertTrue(or_(L[True, False]))
        self.assertFalse(or_(L[[]]))
        self.assertTrue(or_(repeat(True)))

        self.assertTrue(and_(L[True, True]))
        self.assertFalse(and_(L[True, False]))
        self.assertTrue(and_(L[[]]))
        self.assertFalse(and_(repeat(False)))

        self.assertTrue(any(__>5, L[0, ..., 6]))
        self.assertFalse(any(__>6, L[0, ..., 6]))
        self.assertFalse(any(__>6, L[[]]))
        self.assertTrue(any(__>0, L[0, ...]))

        self.assertTrue(all(__>6, L[7, ..., 15]))
        self.assertFalse(all(__>6, L[0, ..., 5]))
        self.assertTrue(all(__>6, L[[]]))
        self.assertFalse(all(__<0, L[0, ...]))

        self.assertEqual(55, sum(L[1, ..., 10]))
        self.assertEqual(0, sum(L[[]]))

        self.assertEqual(3628800, product(L[1, ..., 10]))
        self.assertEqual(1, product(L[[]]))

        self.assertEqual(10, maximum(L[0, ..., 10]))
        with self.assertRaises(ve):
            maximum(L[[]])

        self.assertEqual(0, minimum(L[0, ..., 10]))
        with self.assertRaises(ve):
            minimum(L[[]])

    def test_building_lists(self):
        from hask.Data.List import scanl, scanl1, scanr, scanr1, mapAccumL  # noqa: F401
        from hask.Data.List import mapAccumR, iterate, repeat, replicate, cycle  # noqa: F401
        from hask.Data.List import unfoldr

        plus_one = (lambda x: x + 1) ** (H/ int >> int)
        self.assertEquals(iterate(plus_one, 0)[:10], L[range(10)])
        self.assertEquals(iterate(__+1, 0)[:10], L[range(10)])

        uf = (lambda x: Nothing if x > 5 else Just((x+1, x+1))) ** \
                (H/ int >> t(Maybe, (int, int)))
        self.assertEquals(L[[]], unfoldr(uf, 6))
        self.assertEquals(L[1, ..., 6], unfoldr(uf, 0))

    def test_sublists(self):
        from hask.Data.List import take, drop, splitAt, takeWhile, dropWhile  # noqa: F401
        from hask.Data.List import dropWhileEnd, span, break_, stripPrefix  # noqa: F401
        from hask.Data.List import group, inits, tails, isPrefixOf, isSuffixOf  # noqa: F401
        from hask.Data.List import isInfixOf, isSubsequenceOf  # noqa: F401

        self.assertEqual(L[1, 2], take(2, L[1, 2, 3]))
        self.assertEqual(L[1, 2, 3], take(3, L[1, 2, 3]))
        self.assertEqual(L[1, 2, 3], take(3, L[1, ...]))
        self.assertEqual(L[[]], take(0, L[1, ...]))

        self.assertEqual(L[2, 3], drop(1, L[1, 2, 3]))
        self.assertEqual(L[[]], drop(3, L[1, 2, 3]))
        self.assertEqual(L[1, 2, 3], drop(0, L[1, 2, 3]))
        self.assertEqual(4, drop(3, L[1, ...])[0])

        self.assertEqual((L[1, 2, 3], L[4, 5]), splitAt(3, L[1, ..., 5]))
        self.assertEqual((L[[]], L[[]]), splitAt(0, L[[]]))
        self.assertEqual((L[[]], L[1, 2]), splitAt(0, L[1, 2]))
        self.assertEqual((L[[]], L[[]]), splitAt(10, L[[]]))
        self.assertEqual((L[1, 2], L[[]]), splitAt(10, L[1, 2]))
        self.assertEqual(L[1, ..., 10], splitAt(10, L[1, ...])[0])

        self.assertEqual(L[1, ..., 4], takeWhile(__<5, L[1, ...]))
        self.assertEqual(L[[]], takeWhile(__>5, L[1, ...]))
        self.assertEqual(L[[]], takeWhile(__|True, L[[]]))

        self.assertEqual(L[L[[]], L[[1]], L[1, 2], L[1, 2, 3]],
                         inits(L[1, 2, 3]))
        self.assertEqual(L[[L[[]]]], inits(L[[]]))

        self.assertEqual(L[L[1, 2, 3], L[2, 3], L[[3]], L[[]]],
                         tails(L[1, 2, 3]))
        self.assertEqual(L[[L[[]]]], tails(L[[]]))

        self.assertTrue(isPrefixOf(L["a", "b"], L["a", "b", "c"]))
        self.assertTrue(isPrefixOf(L["a", "b"], L["a", ...]))
        self.assertFalse(isPrefixOf(L["a", "b"], L["d", "a", "b", "c"]))

        self.assertTrue(isSuffixOf(L["b", "c"], L["a", "b", "c"]))
        self.assertFalse(isSuffixOf(L["a", "b"], L["d", "a", "b", "c"]))

        self.assertTrue(isInfixOf(L[1, 2], L[2, 3, 1, 2, 4]))
        self.assertTrue(isInfixOf(L[1, 2], L[1, ...]))
        self.assertFalse(isInfixOf(L[8, 1], L[2, 3, 1, 2, 4]))
        self.assertFalse(isInfixOf(L[1, 2], L[2, 3, 1, 4]))

    def test_searching_lists(self):
        from hask.Data.List import elem, notElem, lookup, find, filter  # noqa: F401
        from hask.Data.List import partition  # noqa: F401

        self.assertTrue(elem(1, L[1, ...]))
        self.assertFalse(elem(2, L[1, 3, 4, 5]))
        self.assertFalse(notElem(1, L[1, ...]))
        self.assertTrue(notElem(2, L[1, 3, 4, 5]))

    def test_indexing_lists(self):
        from hask.Data.List import elemIndex, elemIndices, findIndex  # noqa: F401
        from hask.Data.List import findIndicies  # noqa: F401

    def test_zipping_lists(self):
        from hask.Data.List import zip, zip3, zip4, zip5, zip6, zip7, zipWith  # noqa: F401
        from hask.Data.List import zipWith3, zipWith4, zipWith5, zipWith6  # noqa: F401
        from hask.Data.List import zipWith7, unzip, unzip3, unzip4, unzip5  # noqa: F401
        from hask.Data.List import unzip6  # noqa: F401

        self.assertEqual(L[(1, "a"), (2, "b")], zip(L[1, 2], L["a", "b"]))
        self.assertEqual(L[(1, "a"), (2, "b")], zip(L[1, 2, 3], L["a", "b"]))
        self.assertEqual(L[(1, "a"), (2, "b")], zip(L[1, 2], L["a", "b", "c"]))
        self.assertEqual(L[[]], zip(L[[]], L[[]]))

        self.assertEqual(L[1, 1, 1], zipWith(__-__, L[1, 2, 3], L[0, 1, 2]))
        self.assertEqual(L[1, 1, 1], zipWith(__-__, L[1, 2, 3, 4], L[0, 1, 2]))
        self.assertEqual(L[1, 1, 1], zipWith(__-__, L[1, 2, 3], L[0, 1, 2, 3]))
        self.assertEqual(L[[]], zipWith(__-__, L[[]], L[[]]))

        self.assertEqual((L["a", "b"], L[2, 4]), unzip(L[("a", 2), ("b", 4)]))
        self.assertEqual((L[[]], L[[]]), unzip(L[[]]))

    def test_set_operations(self):
        from hask.Data.List import nub, delete, diff, union, intersect  # noqa: F401

        self.assertEqual(L[[]], nub(L[[]]))
        self.assertEqual(L[[1]], nub(L[[1]]))
        self.assertEqual(L[[1]], nub(L[[1, 1]]))

    def test_ordered_lists(self):
        from hask.Data.List import sort, sortOn, insert  # noqa: F401

        self.assertEqual(L[[]], sort(L[[]]))
        self.assertEqual(L[1, 2, 3], sort(L[1, 2, 3]))
        self.assertEqual(L[1, 2, 3], sort(L[2, 3, 1]))
        self.assertEqual(L[1, 1, 2, 3], sort(L[2, 1, 3, 1]))

    def test_generalized_functions(self):
        from hask.Data.List import nubBy, deleteBy, deleteFirstBy, unionBy  # noqa: F401
        from hask.Data.List import intersectBy, groupBy, sortBy, insertBy  # noqa: F401
        from hask.Data.List import maximumBy, minimumBy, genericLength  # noqa: F401
        from hask.Data.List import genericTake, genericDrop, genericSplitAt  # noqa: F401
        from hask.Data.List import genericIndex, genericReplicate  # noqa: F401
