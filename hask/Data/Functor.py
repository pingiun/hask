from __future__ import division, print_function, absolute_import

from hask.lang.type_system import TypedFunc
from hask.lang.type_system import Typeclass

from hask.lang.lazylist import List

from hask.lang import H
from hask.lang import sig
from hask.lang import t
from hask.lang import instance


class Functor(Typeclass):
    """
    The Functor class is used for types that can be mapped over. Instances of
    Functor should satisfy the following laws::

        fmap(id)  ==  id
        fmap(f * g)  ==  fmap(f * (fmap g))

    Attributes:

    - ``fmap``
    - ``__rmul__``

    Minimal complete definition:

    - ``fmap``

    """
    @classmethod
    def make_instance(typeclass, cls, fmap):
        from hask.lang.type_system import is_builtin
        from hask.lang.type_system import build_instance
        from hask.lang import H, t
        fmap = fmap ** (
            H[(Functor, "f")]/ (H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
        if not is_builtin(cls):
            cls.__rmul__ = lambda x, f: fmap(f, x)
        build_instance(Functor, cls, {"fmap": fmap})


@sig(H[(Functor, "f")]/ (H/ "a" >> "b") >> t("f", "a") >> t("f", "b"))
def fmap(f, x):
    return Functor[x].fmap(f, x)


def _fmap(fn, lst):
    from xoutil.future.itertools import map as imap
    from hask.lang.lazylist import L
    return L[imap(fn, iter(lst))]


instance(Functor, List).where(
    fmap = _fmap
)

instance(Functor, TypedFunc).where(
    fmap = TypedFunc.__mul__
)


del _fmap
del instance, t, sig, H
del List, Typeclass, TypedFunc
