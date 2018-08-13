import unittest

from hask3 import Either, Left, Right, Read, Show, Eq, Functor, Applicative
from hask3 import Typeclass, Num, Foldable, Traversable, Monad
from hask3 import has_instance
from hask3 import __, H, sig, t
from hask3 import L


class TestEither(unittest.TestCase):

    def test_instances(self):
        self.assertTrue(has_instance(Either, Read))
        self.assertTrue(has_instance(Either, Show))
        self.assertTrue(has_instance(Either, Eq))
        self.assertTrue(has_instance(Either, Functor))
        self.assertTrue(has_instance(Either, Applicative))
        self.assertTrue(has_instance(Either, Monad))

        self.assertFalse(has_instance(Either, Typeclass))
        self.assertFalse(has_instance(Either, Num))
        self.assertFalse(has_instance(Either, Foldable))
        self.assertFalse(has_instance(Either, Traversable))

    def test_show(self):
        from hask3.Prelude import show
        self.assertEqual("Left(1)", str(Left(1)))
        self.assertEqual("Left('1')", str(Left("1")))
        self.assertEqual("Right(1)", str(Right(1)))
        self.assertEqual("Right('1')", str(Right("1")))
        self.assertEqual("Right(Left('1'))", str(Right(Left("1"))))
        self.assertEqual("Left(1)", show(Left(1)))
        self.assertEqual("Left('1')", show(Left("1")))
        self.assertEqual("Right(1)", show(Right(1)))
        self.assertEqual("Right('1')", show(Right("1")))
        self.assertEqual("Right(Left('1'))", show(Right(Left("1"))))

    def test_eq(self):
        self.assertTrue(Left(1) == Left(1))
        self.assertTrue(Right(1) == Right(1))
        self.assertFalse(Left(1) == Left(2))
        self.assertFalse(Right(1) == Right(2))
        self.assertFalse(Left(1) == Right(1))
        self.assertFalse(Left("a") == Right(1))
        self.assertFalse(Left(1) != Left(1))
        self.assertFalse(Right(1) != Right(1))
        self.assertTrue(Left(1) != Left(2))
        self.assertTrue(Right(1) != Right(2))
        self.assertTrue(Left(1) != Right(1))
        self.assertTrue(Left("a") != Right(1))

    def test_ord(self):
        self.assertTrue(Left(20) < Right(0))
        self.assertTrue(Left(20) < Right("a"))
        self.assertTrue(Left(2) < Left(3))
        self.assertTrue(Right(2) < Right(3))
        self.assertTrue(Left(20) <= Right(0))
        self.assertTrue(Left(20) <= Right("a"))
        self.assertTrue(Left(2) <= Left(3))
        self.assertTrue(Right(2) <= Right(3))
        self.assertFalse(Right(0) < Left(20))
        self.assertFalse(Right("a") < Left(20))
        self.assertFalse(Left(3) < Left(2))
        self.assertFalse(Right(3) < Right(2))
        self.assertFalse(Right(2) <= Left(20))
        self.assertFalse(Right("a") <= Left(20))
        self.assertFalse(Left(3) <= Left(2))
        self.assertFalse(Right(3) <= Right(2))

        self.assertTrue(Right(0) > Left(20))
        self.assertTrue(Right("a") > Left(20))
        self.assertTrue(Left(3) > Left(2))
        self.assertTrue(Right(3) > Right(2))
        self.assertTrue(Right(2) >= Left(20))
        self.assertTrue(Right("a") >= Left(20))
        self.assertTrue(Left(3) >= Left(2))
        self.assertTrue(Right(3) >= Right(2))
        self.assertFalse(Left(20) > Right(0))
        self.assertFalse(Left(20) > Right("a"))
        self.assertFalse(Left(2) > Left(3))
        self.assertFalse(Right(2) > Right(3))
        self.assertFalse(Left(20) >= Right(0))
        self.assertFalse(Left(20) >= Right("a"))
        self.assertFalse(Left(2) >= Left(3))
        self.assertFalse(Right(2) >= Right(3))

        self.assertFalse(Right(3) > Right(3))
        self.assertFalse(Left(3) > Left(3))
        self.assertFalse(Right(3) < Right(3))
        self.assertFalse(Left(3) < Left(3))
        self.assertTrue(Left(2.0) <= Left(2.0))
        self.assertTrue(Right(2) <= Right(2))
        self.assertTrue(Left(2.0) >= Left(2.0))
        self.assertTrue(Right(2) >= Right(2))

    def test_functor(self):
        from hask3.Prelude import id, fmap, const
        self.assertEqual(Left(7), fmap(__+1, Left(7)))
        self.assertEqual(Left("a"), fmap(__+1, Left("a")))
        self.assertEqual(Right(8), fmap(__+1, Right(7)))
        with self.assertRaises(TypeError):
            fmap(__+1, Right("a"))
        self.assertEqual(Right(Left(1)), fmap(const(Left(1)), Right("a")))
        self.assertEqual(Left("a"), fmap(const(Left(1)), Left("a")))

        f = (lambda x: x + "!") ** (H/ str >> str)
        g = (lambda x: x + "?") ** (H/ str >> str)
        self.assertEqual(Right("b?!"), (f * g) * Right("b"))
        self.assertEqual(Right("b?!"), f * g * Right("b"))
        self.assertEqual(Left("b"), (f * g) * Left("b"))
        self.assertEqual(Left("b"), f * g * Left("b"))

        # functor laws
        self.assertEqual(Left(7), fmap(id, Left(7)))
        self.assertEqual(Right(7), fmap(id, Right(7)))
        self.assertEqual(Right("a?!"), fmap(f * g, Right("a")))
        self.assertEqual(Left("a"), fmap(f * g, Left("a")))
        self.assertEqual(Right("a?!"), fmap(f, fmap(g, Right("a"))))
        self.assertEqual(Left("a"), fmap(f, fmap(g, Left("a"))))

    def test_monad(self):
        from hask3.Prelude import flip
        from hask3.Control.Monad import bind, join

        @sig(H/ int >> int >> t(Either, str, int))
        def sub_whole(x, y):
            return Right(x-y) if (x-y) >= 0 else Left("err")

        sub = flip(sub_whole)

        self.assertEqual(Right(2), Right(4) >> sub(2))
        self.assertEqual(Right(0), Right(4) >> sub(2) >> sub(2))
        self.assertEqual(Left("err"), Right(4) >> sub(10))
        self.assertEqual(Left("0"), Left("0") >> sub_whole(1))

        # monad laws
        sub_composed = (lambda x: sub_whole(4, x) >> sub(2)) ** \
                (H/ int >> t(Either, "a", int))
        self.assertEqual(Right(7), Right(7) >> Right)
        self.assertEqual(Left(7), Left(7) >> Right)
        self.assertEqual(Right(1), (Right(5) >> sub(1)) >> sub(3))
        self.assertEqual(Left("e"), (Left("e") >> sub(1)) >> sub(3))
        self.assertEqual(Left("err"), (Right(5) >> sub(10)) >> sub(3))
        self.assertEqual(Right(0), Right(2) >> sub_composed)
        self.assertEqual(Left("e"), Left("e") >> sub_composed)

        self.assertEqual(Right(2), bind(Right(4), sub(2)))

        self.assertEqual(join(Right(Right(1))), Right(1))
        self.assertEqual(join(Right(Left(1))), Left(1))

    def test_functions(self):
        from hask3.Data.Either import either
        from hask3.Data.Either import isRight
        from hask3.Data.Either import isLeft
        from hask3.Data.Either import lefts
        from hask3.Data.Either import rights
        from hask3.Data.Either import partitionEithers

        f = (lambda x: x + " world") ** (H/ str >> str)
        g = (lambda x: str(x * 10)) ** (H/ int >> str)

        self.assertEqual('20', either(f, g, Right(2)))
        self.assertEqual("hello world", either(f, g, Left("hello")))
        self.assertTrue(isLeft(Left(1)))
        self.assertTrue(isRight(Right("a")))
        self.assertFalse(isLeft(Right("a")))
        self.assertFalse(isRight(Left(1)))

        self.assertEqual(L[1, 3],
                rights(L[Right(1), Left(2), Right(3), Left(4)]))
        self.assertEqual(L[[]], rights(L[[]]))
        self.assertEqual(L[2, 4],
                lefts(L[Right(1), Left(2), Right(3), Left(4)]))
        self.assertEqual(L[[]], lefts(L[[]]))
        self.assertEqual((L[2, 4], L[1, 3]),
                partitionEithers(L[Right(1), Left(2), Right(3), Left(4)]))
        self.assertEqual((L[2, 4], L[[]]),
                partitionEithers(L[Left(2), Left(4)]))
        self.assertEqual((L[[]], L[1, 3]),
                partitionEithers(L[Right(1), Right(3)]))
        self.assertEqual((L[[]], L[[]]),
                partitionEithers(L[[]]))
