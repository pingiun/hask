from __future__ import division, print_function, absolute_import

from hask.lang import List
from hask.lang import instance
from hask.Data.Functor import Functor


class Applicative(Functor):
    """
    A functor with application, providing operations to embed pure expressions
    (pure), and sequence computations and combine their results (ap).

    Dependencies:

    - `~hask.Data.Functor.Functor`:class:

    Attributes:

    - ``pure``

    Minimal complete definition:

    - ``pure``

    """
    @classmethod
    def make_instance(self, cls, pure):
        from hask.lang import build_instance
        build_instance(Applicative, cls, {"pure": pure})


def _pure(x):
    from hask.lang import L
    return L[[x]]


instance(Applicative, List).where(
    pure = _pure
)


del instance, List, Functor, _pure
