import unittest

from hask3 import Show, Eq, Ord, Functor, Monad, Applicative
from hask3 import Foldable, Typeclass, Num
from hask3 import L, H, sig
from hask3 import has_instance

from hask3.lang.lazylist import List


try:
    xrange
except NameError:
    xrange = range


class TestList(unittest.TestCase):

    def test_instances(self):
        self.assertTrue(has_instance(List, Show))
        self.assertTrue(has_instance(List, Eq))
        self.assertTrue(has_instance(List, Ord))
        self.assertTrue(has_instance(List, Functor))
        self.assertTrue(has_instance(List, Applicative))
        self.assertTrue(has_instance(List, Monad))
        self.assertTrue(has_instance(List, Foldable))
        # self.assertTrue(has_instance(List, Traversable))

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
        with self.assertRaises(TypeError):
            L["a", "b"] == L[1, 2]

        # with infinite lists
        self.assertNotEqual(L[1, ...], L[0, ...])
        self.assertNotEqual(L[1, 3, ...], L[1, 4, ...])
        self.assertNotEqual(L[1, 4], L[1, 4, ...])
        with self.assertRaises(TypeError):
            L["a", "b"] == L[1, ...]

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

        with self.assertRaises(TypeError):
            L[1, 2] > L[1.0, 2.0]
        with self.assertRaises(TypeError):
            L[1, 2] > L[1.0, 2.0, ...]
        with self.assertRaises(TypeError):
            L[1, 2] < L[1.0, 2.0]
        with self.assertRaises(TypeError):
            L[1, 2] < L[1.0, 2.0, ...]
        with self.assertRaises(TypeError):
            L[1, 2] >= L[1.0, 2.0]
        with self.assertRaises(TypeError):
            L[1, 2] >= L[1.0, 2.0, ...]
        with self.assertRaises(TypeError):
            L[1, 2] <= L[1.0, 2.0]
        with self.assertRaises(TypeError):
            L[1, 2] <= L[1.0, 2.0, ...]

    def test_show(self):
        from hask3.Prelude import show
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
        with self.assertRaises(TypeError):
            "a" ^ L[2, 4]
        with self.assertRaises(TypeError):
            True ^ L[2, 4]
        with self.assertRaises(TypeError):
            "a" ^ L[(i for i in range(20))]
        with self.assertRaises(TypeError):
            L[1, "a"]

    def test_extend(self):
        self.assertEqual(L[1, 2, 3, 4], L[[1, 2]] + L[[3, 4]])
        self.assertEqual(L[1, 2, 3, 4, 5], L[1, 2] + L[3, 4] + L[[5]])
        self.assertEqual(L[1, 2, 3, 4, 5], L[1, 2] + L[[]] + L[3, 4, 5])
        self.assertEqual(L[1, ..., 10], (L[1, ...] + L[0, ...])[:10])
        with self.assertRaises(TypeError):
            L[1.0, 2.0] + L[3, 4]
        with self.assertRaises(TypeError):
            L[1.0, 2.0] + [3, 4]
        with self.assertRaises(TypeError):
            L[(i for i in "abc")] + L[1, 2]

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
        with self.assertRaises(ie):
            L[((0, 1, 2))][3]
        with self.assertRaises(ie):
            L[((0, 1, 2))][-4]
        with self.assertRaises(ie):
            L[((i for i in range(3)))][3]
        with self.assertRaises(ie):
            L[((i for i in range(3)))][-4]

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
        self.assertEqual(L[2, 3], L[1, ...][1:][:2])
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

        with self.assertRaises(SyntaxError):
            L[1, 2, 3, ...]
        with self.assertRaises(SyntaxError):
            L[..., 2]
        with self.assertRaises(SyntaxError):
            L[1, ..., 10, 11]

    def test_contains(self):
        self.assertTrue(1 in L[2, 3, 1])
        self.assertFalse(1 not in L[2, 3, 1])
        self.assertTrue(4 not in L[2, 3, 1])
        self.assertFalse(4 in L[2, 3, 1])
        self.assertTrue(55 in L[1, ...])
        self.assertFalse(4 in L[1, 3, ..., 19])
        self.assertTrue(4 not in L[1, 3, ..., 19])

        with self.assertRaises(TypeError):
            "b" in L[1, ...]
        self.assertEqual(1, L["a", "b", "a"].count("b"))
        self.assertEqual(2, L["a", "b", "a"].count("a"))
        self.assertEqual(0, L["a", "b", "a"].count("d"))
        with self.assertRaises(TypeError):
            L["a", "b", "c"].count(1)
        self.assertEqual(1, L["a", "b", "a"].index("b"))
        self.assertEqual(0, L["a", "b", "a"].index("a"))
        with self.assertRaises(ValueError):
            L["a", "b", "c"].index("d")
        with self.assertRaises(TypeError):
            L["a", "b", "c"].index(1)

    def test_functor(self):
        from hask3.Prelude import id, map, fmap  # noqa: F401
        f = (lambda x: x ** 2 - 1) ** (H/ int >> int)
        g = (lambda y: y // 4 + 9) ** (H/ int >> int)

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
        # Now this is a list with `None` as member
        self.assertEqual(1, len(L[None]))
        self.assertEqual(1, len(L[None, ]))
        self.assertEqual(3, len(L[1, 2, 3]))
        self.assertEqual(20, len(L[0, ..., 19]))
