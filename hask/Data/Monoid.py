from __future__ import division, print_function, absolute_import

from hask.lang.syntax import H
from hask.lang.syntax import sig

from hask.lang.type_system import Typeclass


class Monoid(Typeclass):
    """Types with an associative binary operation that has an identity.

    Attributes:

    - ``mempty``
    - ``mappend``
    - ``mconcat``

    Minimal complete definition:

    - ``mempty``
    - ``mappend``
    - ``mconcat``

    """
    @classmethod
    def make_instance(typeclass, cls, mempty, mappend, mconcat):
        from hask.lang.type_system import build_instance
        attrs = {"mempty": mempty, "mappend": mappend, "mconcat": mconcat}
        build_instance(Monoid, cls, attrs)


@sig(H[(Monoid, "m")]/ "m" >> "m" >> "m")
def mappend(x, y):
    """``mappend :: a -> a -> a``

    An associative operation.

    """
    return Monoid[x].mappend(x, y)


@sig(H[(Monoid, "m")]/ ["m"] >> "m")
def mconcat(m):
    """``mconcat :: [a] -> a``

    Fold a list using the monoid.

    """
    raise NotImplementedError


del Typeclass
del H, sig
