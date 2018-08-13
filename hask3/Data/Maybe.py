from hask3.lang.typeclasses import Show
from hask3.lang.typeclasses import Read

from hask3.lang.syntax import H
from hask3.lang.syntax import sig
from hask3.lang.syntax import t

from hask3.lang.syntax import data
from hask3.lang.syntax import d
from hask3.lang.syntax import deriving
from hask3.lang.syntax import instance

from hask3.Data.Eq import Eq
from hask3.Data.Ord import Ord
from hask3.Data.Functor import Functor
from hask3.Control.Applicative import Applicative
from hask3.Control.Monad import Monad


# data Maybe a = Nothing | Just a deriving(Show, Eq, Ord)
Maybe, Nothing, Just = (
    data.Maybe("a") == d.Nothing | d.Just("a") & deriving(Read, Show, Eq, Ord)
)


def _fmap(f, x):
    from hask3.lang.syntax import caseof, m, p
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
    from hask3.lang.syntax import caseof, m, p
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
    from hask3.lang.syntax import typify, t

    def closure_in_maybe(*args, **kwargs):
        try:
            return Just(fn(*args, **kwargs))
        except:    # noqa
            return Nothing

    return typify(fn, hkt=lambda x: t(Maybe, x))(closure_in_maybe)


@sig(H/ "b" >> (H/ "a" >> "b") >> t(Maybe, "a") >> "b")
def maybe(default, f, maybe_a):
    """Apply `f` to `maybe_a` (if possible) or return `default`.

    Take a `default` value, a function, and a Maybe value.  If the Maybe value
    is Nothing, return the default value.  Otherwise, apply the function to
    the value inside the Just and return the result.

    Type signature: ``maybe :: b -> (a -> b) -> Maybe a -> b``.

    """
    return default if maybe_a == Nothing else f(maybe_a[0])


@sig(H/ t(Maybe, "a") >> bool)
def isJust(a):
    '''Return True iff its argument is of the form ``Just(_)``.

    Type signature: ``isJust :: [Maybe a] -> bool``

    '''
    return not isNothing(a)


@sig(H/ t(Maybe, "a")  >> bool)
def isNothing(a):
    '''Return True iff its argument is of the form ``Nothing``.

    Type signature: ``isNothing :: [Maybe a] -> bool``.

    '''
    from hask3.lang.syntax import caseof, m
    return ~(caseof(a)
                | m(Nothing)   >> True
                | m(Just(m.x)) >> False)


@sig(H/ t(Maybe, "a") >> "a")
def fromJust(x):
    '''Extract the value from a ``Just(x)``.

    If `x` is not of the form ``Just(_)``, raise a ValueError.

    Type signature: ``fromJust :: [Maybe a] -> a``.

    '''
    if isJust(x):
        return x[0]
    else:
        raise ValueError("Cannot call fromJust on Nothing.")


@sig(H/ 'a' >> t(Maybe, 'a') >> 'a')
def fromMaybe(default, x):
    '''Return the value wrapped or the default.

    If the Maybe is Nothing, return the default value; otherwise, return the
    value contained in the Maybe.

    Type signature:: ``fromMaybe :: a -> Maybe a -> a``.

    '''
    from hask3.lang.syntax import caseof, m, p
    return ~(caseof(x)
        | m(Nothing) >> default
        | m(Just(m.x)) >> p.x
    )


@sig(H/ ["a"] >> t(Maybe, "a"))
def listToMaybe(ls):
    '''Wrap the head of the list with the Maybe functor.

    If the list is empty, return Nothing; otherwise return ``Just(head(ls))``.

    Type signature: ``listToMaybe :: [a] -> [Maybe a]``.

    '''
    from hask3.lang.syntax import caseof, m, p
    return ~(caseof(ls)
                | m(m.a ^ m.b) >> Just(p.a)
                | m(m.a)       >> Nothing)


@sig(H/ t(Maybe, "a") >> ["a"])
def maybeToList(a):
    """Return a list from a Maybe value.

    When given Nothing, return the empty list.  When given ``Just(x)`` return
    the list ``[x]``.

    Type signature: ``maybeToList :: Maybe a -> [a]``.

    """
    from hask3.lang.syntax import caseof, m, p
    from hask3.lang.lazylist import L
    return ~(caseof(a)
                | m(Nothing)   >> L[[]]
                | m(Just(m.x)) >> L[[p.x]])


@sig(H/ [t(Maybe, "a")] >> ["a"])
def catMaybes(maybes):
    """Extract all non-Nothing values.

    Type signature: ``catMaybes :: [Maybe a] -> [a]``.

    """
    from hask3.lang.lazylist import L
    return L[(fromJust(item) for item in maybes if isJust(item))]


@sig(H/ (H/ "a" >> t(Maybe, "b")) >> ["a"] >> ["b"])
def mapMaybe(f, la):
    """Apply `f` to all non-Nothing values.

    `mapMaybe`:func: is a version of map which can throw out elements.  In
    particular, the functional argument returns something of type ``Maybe b``.
    If this is Nothing, no element is added on to the result list.  If it is
    Just b, then b is included in the result list.

    Type signature: ``mapMaybe :: (a -> Maybe b) -> [a] -> [b]``

    """
    from hask3.lang.lazylist import L
    return L[(fromJust(b) for b in (f(a) for a in la) if isJust(b))]


del Read, Show
del H, sig, t
del data, d, instance, deriving
del Eq, Ord, Functor, Applicative, Monad
