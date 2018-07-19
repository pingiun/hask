from __future__ import division, print_function, absolute_import

import unittest

from hask import has_instance
from hask import Maybe, Just, Nothing
from hask import Read, Show, Eq, Functor, Applicative
from hask import Monad, Num, Foldable, Traversable
from hask import Typeclass, L

from hask import H, sig, __, t


te = TypeError
ve = ValueError


class TestMaybe(unittest.TestCase):

    def test_instances(self):
        self.assertTrue(has_instance(Maybe, Read))
        self.assertTrue(has_instance(Maybe, Show))
        self.assertTrue(has_instance(Maybe, Eq))
        self.assertTrue(has_instance(Maybe, Functor))
        self.assertTrue(has_instance(Maybe, Applicative))
        self.assertTrue(has_instance(Maybe, Monad))

        self.assertFalse(has_instance(Maybe, Typeclass))
        self.assertFalse(has_instance(Maybe, Num))
        self.assertFalse(has_instance(Maybe, Foldable))
        self.assertFalse(has_instance(Maybe, Traversable))

    def test_show(self):
        from hask.Prelude import show
        self.assertEqual("Just(3)", str(Just(3)))
        self.assertEqual("Just(3)", show(Just(3)))
        self.assertEqual("Just('a')", str(Just("a")))
        self.assertEqual("Just('a')", show(Just("a")))
        self.assertEqual("Just(Just(3))", str(Just(Just(3))))
        self.assertEqual("Just(Just(3))", show(Just(Just(3))))
        self.assertEqual("Nothing", str(Nothing))
        self.assertEqual("Nothing", show(Nothing))

    def test_eq(self):
        self.assertEqual(Nothing, Nothing)
        self.assertEqual(Just(3), Just(3))
        self.assertEqual(Just("3"), Just("3"))
        self.assertNotEqual(Just(1), Just(3))
        self.assertNotEqual(Just(3), Nothing)
        self.assertNotEqual(Nothing, Just(0))
        self.assertTrue(Just(1) == Just(1))
        self.assertFalse(Just(1) == Just(2))
        self.assertTrue(Nothing == Nothing or Nothing != Nothing)
        self.assertTrue(Just(1) == Just(1) or Just(1) != Just(1))
        self.assertFalse(Nothing == Nothing and Nothing != Nothing)
        self.assertFalse(Just(1) == Just(1) and Just(1) != Just(1))
        with self.assertRaises(te):
            Just(1) == Just("1")
        with self.assertRaises(te):
            Just(1) == Just(1.0)
        with self.assertRaises(te):
            Nothing == None  # noqa
        with self.assertRaises(te):
            Nothing == 1
        with self.assertRaises(te):
            Just(1) == 1

    def test_ord(self):
        self.assertTrue(Nothing < Just(0))
        self.assertTrue(Nothing < Just("a"))
        self.assertTrue(Nothing < Just(-float("inf")))
        self.assertTrue(Nothing <= Just(0))
        self.assertTrue(Nothing <= Just("a"))
        self.assertTrue(Nothing <= Just(-float("inf")))
        self.assertTrue(Nothing >= Nothing and Nothing <= Nothing)
        self.assertFalse(Nothing > Just(0))
        self.assertFalse(Nothing > Just("a"))
        self.assertFalse(Nothing > Just(-float("inf")))
        self.assertFalse(Nothing >= Just(0))
        self.assertFalse(Nothing >= Just("a"))
        self.assertFalse(Nothing >= Just(-float("inf")))
        self.assertFalse(Nothing > Nothing or Nothing < Nothing)

        self.assertTrue(Just(1) > Just(0))
        self.assertTrue(Just(Just(1)) > Just(Nothing))
        self.assertTrue(Just(Just(Nothing)) > Just(Nothing))
        self.assertTrue(Just(1) >= Just(0))
        self.assertTrue(Just(1) >= Just(1))
        self.assertTrue(Just(Just(1)) >= Just(Nothing))
        self.assertTrue(Just(Just(Nothing)) >= Just(Nothing))
        self.assertTrue(Just(Just(Nothing)) >= Just(Just(Nothing)))
        self.assertFalse(Just(0) > Just(1))
        self.assertFalse(Just(0) > Just(0))
        self.assertFalse(Just(Nothing) > Just(Just(1)))
        self.assertFalse(Just(Nothing) > Just(Just(Nothing)))
        self.assertFalse(Just(0) >= Just(1))
        self.assertFalse(Just(Nothing) >= Just(Just(1)))
        self.assertFalse(Just(Nothing) >= Just(Just(Nothing)))

        self.assertTrue(Just(0) < Just(1))
        self.assertTrue(Just(Nothing) < Just(Just(1)))
        self.assertTrue(Just(Nothing) < Just(Just(Nothing)))
        self.assertTrue(Just(0) <= Just(1))
        self.assertTrue(Just(Nothing) <= Just(Just(1)))
        self.assertTrue(Just(Nothing) <= Just(Just(Nothing)))
        self.assertFalse(Just(1) < Just(0))
        self.assertFalse(Just(1) < Just(1))
        self.assertFalse(Just(Just(1)) < Just(Nothing))
        self.assertFalse(Just(Just(Nothing)) < Just(Nothing))
        self.assertFalse(Just(1) <= Just(0))
        self.assertTrue(Just(1) <= Just(1))
        self.assertFalse(Just(Just(1)) <= Just(Nothing))
        self.assertFalse(Just(Just(Nothing)) <= Just(Nothing))
        self.assertTrue(Just(Just(Nothing)) <= Just(Just(Nothing)))

        with self.assertRaises(te):
            Just(1) > Just(1.0)
        with self.assertRaises(te):
            Just(1) >= Just(1.0)
        with self.assertRaises(te):
            Just(1) < Just(1.0)
        with self.assertRaises(te):
            Just(1) <= Just(1.0)
        with self.assertRaises(te):
            Just(1) > Just(Just(1))
        with self.assertRaises(te):
            Just(1) >= Just(Just(1))
        with self.assertRaises(te):
            Just(1) < Just(Just(1))
        with self.assertRaises(te):
            Just(1) <= Just(Just(1))

    def test_functor(self):
        from hask.Prelude import id, fmap
        plus1 = (lambda x: x + 1) ** (H/ int >> int)
        toStr = str ** (H/ int >> str)

        self.assertEqual(Just(Just(2)), fmap(Just, Just(2)))
        self.assertEqual(Just(3), plus1 * Just(2))
        self.assertEqual(Just("1"), toStr * Just(1))
        self.assertEqual(Just("3"), (toStr * plus1) * Just(2))

        # functor laws
        self.assertEqual(fmap(id, Just(4)), Just(4))
        self.assertEqual(fmap(id, Nothing), Nothing)
        self.assertEqual(id * Just(4), Just(4))
        self.assertEqual(id * Nothing, Nothing)
        self.assertEqual(fmap(toStr, fmap(plus1, Just(2))),
                         fmap(toStr * plus1, Just(2)))
        self.assertEqual((toStr * (plus1 * Just(2))),
                         (toStr * plus1) * Just(2))

    def test_monad(self):
        f = (lambda x: Just(str(x))) ** (H/ int >> t(Maybe, str))
        g = (lambda x: Just(x * 10)) ** (H/ int >> t(Maybe, int))
        self.assertEqual(Just("1"), Just(1) >> f)
        self.assertEqual(Just(10), Just(1) >> g)
        self.assertEqual(Just(1000), Just(1) >> g >> g >> g)

        @sig(H[(Num, "a")]/ "a" >> "a" >> t(Maybe, "a"))
        def safediv(x, y):
            return Just(x // y) if y != 0 else Nothing

        from hask.Prelude import flip
        s = flip(safediv)
        self.assertEqual(Just(3), Just(9) >> s(3))
        self.assertEqual(Just(1), Just(9) >> s(3) >> s(3))
        self.assertEqual(Nothing, Just(9) >> s(0) >> s(3))
        self.assertEqual(Nothing, Nothing >> s(3) >> s(3))

        # monad laws
        s_composed = (lambda x: s(3, x) >> s(3)) ** (H/ int >> t(Maybe, int))
        self.assertEqual(Just(2), Just(2) >> Just)
        self.assertEqual(Nothing, Nothing >> Just)
        self.assertEqual(Just(4) >> s(2), s(2, 4))
        self.assertEqual(Just(1), (Just(9) >> s(3)) >> s(3))
        self.assertEqual(Just(1), Just(9) >> s_composed)
        self.assertEqual(Nothing, (Nothing >> s(3)) >> s(3))
        self.assertEqual(Nothing, Nothing >> s_composed)

        from hask.Control.Monad import join, liftM
        self.assertEqual(join(Just(Just(1))), Just(1))
        self.assertEqual(join(Just(Nothing)), Nothing)
        self.assertEqual(liftM(__+1, Just(1)), Just(2))
        self.assertEqual(liftM(__+1, Nothing), Nothing)

    def test_functions(self):
        from hask.Data.Maybe import maybe, isJust, isNothing, fromJust
        from hask.Data.Maybe import listToMaybe, maybeToList, catMaybes
        from hask.Data.Maybe import mapMaybe

        self.assertTrue(isJust(Just(1)))
        self.assertTrue(isJust(Just(Nothing)))
        self.assertFalse(isJust(Nothing))
        self.assertFalse(isNothing(Just(1)))
        self.assertFalse(isNothing(Just(Nothing)))
        self.assertTrue(isNothing(Nothing))
        self.assertEqual(fromJust(Just("bird")), "bird")
        self.assertEqual(fromJust(Just(Nothing)), Nothing)
        with self.assertRaises(ve):
            fromJust(Nothing)

        self.assertEqual(2, maybe(0, (__+1), Just(1)))
        self.assertEqual(0, maybe(0, (__+1)) % Nothing)
        self.assertEqual(Nothing, listToMaybe(L[[]]))
        self.assertEqual(Just("a"), listToMaybe(L[["a"]]))
        self.assertEqual(Just("a"), listToMaybe(L["a", "b"]))
        self.assertEqual(Just(1), listToMaybe(L[1, ...]))
        self.assertEqual(L[[]], maybeToList(Nothing))
        self.assertEqual(L[[1]], maybeToList(Just(1)))
        self.assertEqual(L[[]], catMaybes(L[[]]))
        self.assertEqual(L[[]], catMaybes(L[Nothing, Nothing]))
        self.assertEqual(L[1, 2], catMaybes(L[Just(1), Just(2)]))
        self.assertEqual(L[1, 2], catMaybes(L[Just(1), Nothing, Just(2)]))

        from hask.Prelude import const
        self.assertEqual(L[[]], mapMaybe(const(Nothing), L[1, 2]))
        self.assertEqual(L[1, 2], mapMaybe(Just, L[1, 2]))
        self.assertEqual(L[[]], mapMaybe(Just, L[[]]))

        f = (lambda x: Just(x) if x > 3 else Nothing) \
            ** (H/ int >> t(Maybe, int))
        self.assertEqual(L[4, 5], mapMaybe(f, L[1, ..., 5]))
        self.assertEqual(L[[]], mapMaybe(f, L[1, ..., 3]))
