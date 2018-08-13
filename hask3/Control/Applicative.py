from hask3.lang import List
from hask3.lang import instance
from hask3.Data.Functor import Functor


class Applicative(Functor):
    """
    A functor with application, providing operations to embed pure expressions
    (pure), and sequence computations and combine their results (ap).

    Dependencies:

    - `~hask3.Data.Functor.Functor`:class:

    Attributes:

    - ``pure``

    Minimal complete definition:

    - ``pure``

    """
    @classmethod
    def make_instance(self, cls, pure):
        from hask3.lang import build_instance
        build_instance(Applicative, cls, {"pure": pure})


def _pure(x):
    from hask3.lang import L
    return L[[x]]


instance(Applicative, List).where(
    pure = _pure
)


del instance, List, Functor, _pure
