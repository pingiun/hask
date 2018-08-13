# flake8: noqa
import fractions

from hask3.lang.syntax import sig
from hask3.lang.syntax import H
from hask3.lang.syntax import t

from hask3.Data.Maybe import Maybe
from hask3.Data.Maybe import Just
from hask3.Data.Maybe import Nothing
from hask3.Data.Maybe import in_maybe
from hask3.Data.Maybe import maybe

from hask3.Data.Either import Either
from hask3.Data.Either import Left
from hask3.Data.Either import Right
from hask3.Data.Either import in_either
from hask3.Data.Either import either

from hask3.Data.Ord import Ordering
from hask3.Data.Ord import LT
from hask3.Data.Ord import EQ
from hask3.Data.Ord import GT

from hask3.Data.Tuple import fst
from hask3.Data.Tuple import snd
from hask3.Data.Tuple import curry
from hask3.Data.Tuple import uncurry

from hask3.lang.typeclasses import Read
from hask3.lang.typeclasses import Show
from hask3.lang.typeclasses import show

from hask3.Data.Eq import Eq
from hask3.Data.Ord import Ord
from hask3.Data.Ord import max
from hask3.Data.Ord import min
from hask3.Data.Ord import compare

from hask3.lang.lazylist import Enum
from hask3.lang.lazylist import fromEnum
from hask3.lang.lazylist import succ
from hask3.lang.lazylist import pred
from hask3.lang.lazylist import enumFromThen
from hask3.lang.lazylist import enumFrom
from hask3.lang.lazylist import enumFromThenTo
from hask3.lang.lazylist import enumFromTo

from hask3.lang.typeclasses import Bounded
from hask3.Data.Functor import Functor
from hask3.Data.Functor import fmap

from hask3.Control.Applicative import Applicative
from hask3.Control.Monad import Monad
from hask3.Data.Foldable import Foldable
from hask3.Data.Traversable import Traversable

from hask3.Data.Num import Num
from hask3.Data.Num import abs
from hask3.Data.Num import negate
from hask3.Data.Num import signum

from hask3.Data.Num import Fractional
from hask3.Data.Num import recip

from hask3.Data.Num import Integral
from hask3.Data.Num import toRatio

from hask3.Data.Num import Ratio
from hask3.Data.Num import R
from hask3.Data.Num import Rational

from hask3.Data.Num import Floating
from hask3.Data.Num import exp
from hask3.Data.Num import sqrt
from hask3.Data.Num import log
from hask3.Data.Num import pow
from hask3.Data.Num import logBase
from hask3.Data.Num import sin
from hask3.Data.Num import tan
from hask3.Data.Num import cos
from hask3.Data.Num import asin
from hask3.Data.Num import atan
from hask3.Data.Num import acos
from hask3.Data.Num import sinh
from hask3.Data.Num import tanh
from hask3.Data.Num import cosh
from hask3.Data.Num import asinh
from hask3.Data.Num import atanh
from hask3.Data.Num import acosh

from hask3.Data.Num import Real
from hask3.Data.Num import toRational

from hask3.Data.Num import RealFrac
from hask3.Data.Num import properFraction
from hask3.Data.Num import truncate
from hask3.Data.Num import round
from hask3.Data.Num import ceiling
from hask3.Data.Num import floor

from hask3.Data.Num import RealFloat
from hask3.Data.Num import isNaN
from hask3.Data.Num import isInfinite
from hask3.Data.Num import isNegativeZero
from hask3.Data.Num import atan2


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
    return fractions.gcd(x, y)


@sig(H[(Integral, "a")]/ "a" >> "a" >> "a")
def lcm(x, y):
    """``lcm :: Integral a => a -> a -> a``

    The smallest positive integer that both `x` and `y` divide.

    """
    g = gcd(x, y)
    return 0 if g == 0 else (x * y) // g


from hask3.Data.Functor import Functor
from hask3.Control.Applicative import Applicative
from hask3.Control.Monad import Monad


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


from hask3.lang.syntax import undefined

from hask3.Data.List import map
from hask3.Data.List import filter
from hask3.Data.List import head
from hask3.Data.List import last
from hask3.Data.List import tail
from hask3.Data.List import init
from hask3.Data.List import null
from hask3.Data.List import reverse
from hask3.Data.List import length

from hask3.Data.List import foldl
from hask3.Data.List import foldl1
from hask3.Data.List import foldr
from hask3.Data.List import foldr1

from hask3.Data.List import and_
from hask3.Data.List import or_
from hask3.Data.List import any
from hask3.Data.List import all
from hask3.Data.List import sum
from hask3.Data.List import product
from hask3.Data.List import concat
from hask3.Data.List import concatMap
from hask3.Data.List import maximum
from hask3.Data.List import minimum

from hask3.Data.List import scanl
from hask3.Data.List import scanl1
from hask3.Data.List import scanr
from hask3.Data.List import scanr1

from hask3.Data.List import iterate
from hask3.Data.List import repeat
from hask3.Data.List import replicate
from hask3.Data.List import cycle

from hask3.Data.List import take
from hask3.Data.List import drop
from hask3.Data.List import splitAt
from hask3.Data.List import takeWhile
from hask3.Data.List import dropWhile
from hask3.Data.List import span
from hask3.Data.List import break_

from hask3.Data.List import elem
from hask3.Data.List import notElem
from hask3.Data.List import lookup

from hask3.Data.List import zip
from hask3.Data.List import zip3
from hask3.Data.List import zipWith
from hask3.Data.List import zipWith3
from hask3.Data.List import unzip
from hask3.Data.List import unzip3

from hask3.Data.List import lines
from hask3.Data.List import words
from hask3.Data.List import unlines
from hask3.Data.List import unwords
