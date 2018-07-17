from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)

from ..lang import build_instance
from ..lang import List, L
from ..lang import instance
from ..Data.Functor import Functor


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
        build_instance(Applicative, cls, {"pure": pure})


instance(Applicative, List).where(
    pure = lambda x: L[[x]]
)
