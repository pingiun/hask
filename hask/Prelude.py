# flake8: noqa
from __future__ import division, print_function, absolute_import

from hask.lang.syntax import sig
from hask.lang.syntax import H
from hask.lang.syntax import t

from hask.Data.Maybe import Maybe
from hask.Data.Maybe import Just
from hask.Data.Maybe import Nothing
from hask.Data.Maybe import in_maybe
from hask.Data.Maybe import maybe

from hask.Data.Either import Either
from hask.Data.Either import Left
from hask.Data.Either import Right
from hask.Data.Either import in_either
from hask.Data.Either import either

from hask.Data.Ord import Ordering
from hask.Data.Ord import LT
from hask.Data.Ord import EQ
from hask.Data.Ord import GT

from hask.Data.Tuple import fst
from hask.Data.Tuple import snd
from hask.Data.Tuple import curry
from hask.Data.Tuple import uncurry

from hask.lang.typeclasses import Read
from hask.lang.typeclasses import Show
from hask.lang.typeclasses import show

from hask.Data.Eq import Eq
from hask.Data.Ord import Ord
from hask.Data.Ord import max
from hask.Data.Ord import min
from hask.Data.Ord import compare

from hask.lang.lazylist import Enum
from hask.lang.lazylist import fromEnum
from hask.lang.lazylist import succ
from hask.lang.lazylist import pred
from hask.lang.lazylist import enumFromThen
from hask.lang.lazylist import enumFrom
from hask.lang.lazylist import enumFromThenTo
from hask.lang.lazylist import enumFromTo

from hask.lang.typeclasses import Bounded
from hask.Data.Functor import Functor
from hask.Data.Functor import fmap

from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad
from hask.Data.Foldable import Foldable
from hask.Data.Traversable import Traversable

from hask.Data.Num import Num
from hask.Data.Num import abs
from hask.Data.Num import negate
from hask.Data.Num import signum

from hask.Data.Num import Fractional
from hask.Data.Num import recip

from hask.Data.Num import Integral
from hask.Data.Num import toRatio

from hask.Data.Num import Ratio
from hask.Data.Num import R
from hask.Data.Num import Rational

from hask.Data.Num import Floating
from hask.Data.Num import exp
from hask.Data.Num import sqrt
from hask.Data.Num import log
from hask.Data.Num import pow
from hask.Data.Num import logBase
from hask.Data.Num import sin
from hask.Data.Num import tan
from hask.Data.Num import cos
from hask.Data.Num import asin
from hask.Data.Num import atan
from hask.Data.Num import acos
from hask.Data.Num import sinh
from hask.Data.Num import tanh
from hask.Data.Num import cosh
from hask.Data.Num import asinh
from hask.Data.Num import atanh
from hask.Data.Num import acosh

from hask.Data.Num import Real
from hask.Data.Num import toRational

from hask.Data.Num import RealFrac
from hask.Data.Num import properFraction
from hask.Data.Num import truncate
from hask.Data.Num import round
from hask.Data.Num import ceiling
from hask.Data.Num import floor

from hask.Data.Num import RealFloat
from hask.Data.Num import isNaN
from hask.Data.Num import isInfinite
from hask.Data.Num import isNegativeZero
from hask.Data.Num import atan2


@sig(H[(Num, "a")]/ "a" >> "a" >> "a")
def subtract(x, y):
    """``subtract :: Num a => a -> a -> a``

    The same as ``lambda x, y: y - x``.

    """
    return y - x


@sig(H[(Integral, "a")]/ "a" >> bool)
def even(x):
    """``even :: Integral a => a -> Bool``

    Returns True if the integral value is even, and False otherwise.

    """
    return x % 2 == 0


@sig(H[(Integral, "a")]/ "a" >> bool)
def odd(x):
    """``odd :: Integral a => a -> Bool``

    Returns True if the integral value is odd, and False otherwise.

    """
    return x % 2 == 1


@sig(H[(Integral, "a")]/ "a" >> "a" >> "a")
def gcd(x, y):
    """``gcd :: Integral a => a -> a -> a``

    The non-negative factor of both `x` and `y` of which every common factor
    of `x` and `y` is also a factor; for example ``gcd(4, 2) = 2``, ``gcd(-4,
    6) = 2``, ``gcd(0, 4) = 4``, and ``gcd(0, 0) = 0``.  (That is, the common
    divisor that is "greatest" in the divisibility pre-ordering.)

    """
    import fractions
    return fractions.gcd(x, y)


@sig(H[(Integral, "a")]/ "a" >> "a" >> "a")
def lcm(x, y):
    """``lcm :: Integral a => a -> a -> a``

    The smallest positive integer that both `x` and `y` divide.

    """
    g = gcd(x, y)
    return 0 if g == 0 else (x * y) // g


from hask.Data.Functor import Functor
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad


@sig(H[(Monad, "m")]/ t("m", "a") >> t("m", None))
def sequence(xs):
    """``sequence :: Monad m => [m a] -> m [a]``

    Evaluate each action in the sequence from left to right, and collect the
    results.

    """
    raise NotImplementedError()


@sig(H[(Monad, "m")]/ t("m", "a") >> t("m", None))
def sequence_(xs):
    """``sequence_ :: Monad m => [m a] -> m None``

    Evaluate each action in the sequence from left to right, and ignore the
    results.

    """
    raise NotImplementedError()


def mapM(f, xs):
    """``mapM :: Monad m => (a -> m b) -> [a] -> m [b]``

    Equivalent to ``sequence * map(f)``.

    """
    return sequence(fmap(f, xs))


def mapM_(f, xs):
    """``mapM_ :: Monad m => (a -> m b) -> [a] -> m ()``

    Equivalent to ``sequence_ * map(f)``.

    """
    return sequence_(fmap(f, xs))


@sig(H/ "a" >> "a")
def id(a):
    """``id :: a -> a``

    Identity function.

    """
    return a


@sig(H/ "a" >> "b" >> "a")
def const(a, b):
    """``const :: a -> b -> a``

    Constant function.

    """
    return a


@sig(H/ (H/ "a" >> "b" >> "c") >> "b" >> "a" >> "c")
def flip(f, b, a):
    """``flip :: (a -> b -> c) -> b -> a -> c``

    Takes its (first) two arguments in the reverse order of `f`.

    """
    return f(a, b)


@sig(H/ (H/ "a" >> bool) >> (H/ "a" >> "a") >> "a" >> "a")
def until(p, f, a):
    """``until :: (a -> Bool) -> (a -> a) -> a -> a``

    Yields the result of applying `f` until ``p(a)`` holds.

    """
    while not p(a):
        a = f(a)
    return a


@sig(H/ "a" >> "a" >> "a")
def asTypeOf(a, b):
    """``asTypeOf :: a -> a -> a``

    A type-restricted version of `const`:func:.  It is usually used as an
    infix operator, and its typing forces its first argument (which is usually
    overloaded) to have the same type as the second.

    """
    return a


@sig(H/ str >> "a")
def error(msg):
    """``error :: str -> a``

    Stops execution and displays an error message.

    """
    raise Exception(msg)


from hask.lang.syntax import undefined

from hask.Data.List import map
from hask.Data.List import filter
from hask.Data.List import head
from hask.Data.List import last
from hask.Data.List import tail
from hask.Data.List import init
from hask.Data.List import null
from hask.Data.List import reverse
from hask.Data.List import length

from hask.Data.List import foldl
from hask.Data.List import foldl1
from hask.Data.List import foldr
from hask.Data.List import foldr1

from hask.Data.List import and_
from hask.Data.List import or_
from hask.Data.List import any
from hask.Data.List import all
from hask.Data.List import sum
from hask.Data.List import product
from hask.Data.List import concat
from hask.Data.List import concatMap
from hask.Data.List import maximum
from hask.Data.List import minimum

from hask.Data.List import scanl
from hask.Data.List import scanl1
from hask.Data.List import scanr
from hask.Data.List import scanr1

from hask.Data.List import iterate
from hask.Data.List import repeat
from hask.Data.List import replicate
from hask.Data.List import cycle

from hask.Data.List import take
from hask.Data.List import drop
from hask.Data.List import splitAt
from hask.Data.List import takeWhile
from hask.Data.List import dropWhile
from hask.Data.List import span
from hask.Data.List import break_

from hask.Data.List import elem
from hask.Data.List import notElem
from hask.Data.List import lookup

from hask.Data.List import zip
from hask.Data.List import zip3
from hask.Data.List import zipWith
from hask.Data.List import zipWith3
from hask.Data.List import unzip
from hask.Data.List import unzip3

from hask.Data.List import lines
from hask.Data.List import words
from hask.Data.List import unlines
from hask.Data.List import unwords
