from __future__ import division, print_function, absolute_import

from hask.lang.typeclasses import Show
from hask.lang.typeclasses import Read

from hask.lang.syntax import H
from hask.lang.syntax import sig
from hask.lang.syntax import t

from hask.lang.syntax import data
from hask.lang.syntax import d
from hask.lang.syntax import deriving
from hask.lang.syntax import instance

from hask.Data.Eq import Eq
from hask.Data.Ord import Ord
from hask.Data.Functor import Functor
from hask.Control.Applicative import Applicative
from hask.Control.Monad import Monad


# data Maybe a = Nothing | Just a deriving(Show, Eq, Ord)
Maybe, Nothing, Just =\
    data.Maybe("a") == d.Nothing | d.Just("a") & deriving(Read, Show, Eq, Ord)


def _fmap(f, x):
    from hask.lang.syntax import caseof, m, p
    return ~(caseof(x)
                | m(Just(m.a)) >> Just(f(p.a))
                | m(Nothing)   >> Nothing)


instance(Functor, Maybe).where(
    fmap = _fmap
)


instance(Applicative, Maybe).where(
    pure = Just
)


def _bind(x, f):
    from hask.lang.syntax import caseof, m, p
    return ~(caseof(x)
                | m(Just(m.a)) >> f(p.a)
                | m(Nothing)   >> Nothing)


instance(Monad, Maybe).where(
    bind = _bind
)


def in_maybe(fn):
    """Decorator for monadic error handling.

    If the decorated function raises an exception, return `Nothing`.
    Otherwise, take the result and wrap it in a `Just`.

    """
    from hask.lang.syntax import typify, t

    def closure_in_maybe(*args, **kwargs):
        try:
            return Just(fn(*args, **kwargs))
        except:    # noqa
            return Nothing

    return typify(fn, hkt=lambda x: t(Maybe, x))(closure_in_maybe)


@sig(H/ "b" >> (H/ "a" >> "b") >> t(Maybe, "a") >> "b")
def maybe(default, f, maybe_a):
    """``maybe :: b -> (a -> b) -> Maybe a -> b``

    Takes a `default` value, a function `f`, and a `Maybe` value.  If the
    `Maybe` value is `Nothing`, the function returns the default value.
    Otherwise, it applies the function to the value inside the `Just` and
    returns the result.

    """
    return default if maybe_a == Nothing else f(maybe_a[0])


@sig(H/ t(Maybe, "a") >> bool)
def isJust(a):
    '``isJust :: [Maybe a] -> bool``'
    return not isNothing(a)


@sig(H/ t(Maybe, "a")  >> bool)
def isNothing(a):
    '''``isNothing :: [Maybe a] -> bool``'''
    from hask.lang.syntax import caseof, m
    return ~(caseof(a)
                | m(Nothing)   >> True
                | m(Just(m.x)) >> False)


@sig(H/ t(Maybe, "a") >> "a")
def fromJust(x):
    '``fromJust :: [Maybe a] -> a``'
    if isJust(x):
        return x[0]
    else:
        raise ValueError("Cannot call fromJust on Nothing.")


@sig(H/ ["a"] >> t(Maybe, "a"))
def listToMaybe(a):
    '''``listToMaybe :: [a] -> [Maybe a]``'''
    from hask.lang.syntax import caseof, m, p
    return ~(caseof(a)
                | m(m.a ^ m.b) >> Just(p.a)
                | m(m.a)       >> Nothing)


@sig(H/ t(Maybe, "a") >> ["a"])
def maybeToList(a):
    """``maybeToList :: Maybe a -> [a]``

    Returns an empty list when given `Nothing` or a singleton list when not.

    """
    from hask.lang.syntax import caseof, m, p
    from hask.lang.lazylist import L
    return ~(caseof(a)
                | m(Nothing)   >> L[[]]
                | m(Just(m.x)) >> L[[p.x]])


@sig(H/ [t(Maybe, "a")] >> ["a"])
def catMaybes(a):
    """``catMaybes :: [Maybe a] -> [a]``

    Takes a list of `Maybes` and returns a list of all the `Just` values.

    """
    from hask.lang.lazylist import L
    return L[(fromJust(item) for item in a if isJust(item))]


@sig(H/ (H/ "a" >> t(Maybe, "b")) >> ["a"] >> ["b"])
def mapMaybe(f, la):
    """``mapMaybe :: (a -> Maybe b) -> [a] -> [b]``

    A version of `map` using a function with a `Maybe` result.  If it is
    ``Just b``, then `b` is included in the result list; otherwise, if it is
    ``Nothing``, no element is included.

    """
    from hask.lang.lazylist import L
    return L[(fromJust(b) for b in (f(a) for a in la) if isJust(b))]


del Read, Show
del H, sig, t
del data, d, instance, deriving
del Eq, Ord, Functor, Applicative, Monad
