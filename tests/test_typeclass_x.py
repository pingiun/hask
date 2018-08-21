'''Manu's example on "xhg2" (prices).'''

import unittest

from hask3.lang.syntax import t, instance, data, d, deriving, H
from hask3.lang.syntax import m, p, caseof
from hask3.lang.type_system import Typeclass, build_instance
from hask3.Data.Eq import Eq
from hask3.Data.Maybe import Maybe, Nothing, Just
from hask3.lang.typeclasses import Show


class Composite(Typeclass):
    '''A composite with payload of type `a`, children of type `b`, wrapped in
    container of type `f`.

    Attributes:

    - ``children :: a -> f b``

    '''
    @classmethod
    def make_instance(cls, instance, children):
        children = children ** (H/ 'a' >> t('f', 'b'))
        build_instance(cls, instance,
                       {'children': lambda self: children(self)})


Tree, Leaf, Node = data.Tree('a') == (
    d.Leaf | d.Node('a', [t(data.Tree, 'a')]) &
    deriving(Show, Eq)
)


def tree_children(t):
    return ~(caseof(t)
             | m(Leaf) >> Nothing
             | m(Node(m.p, m.xs)) >> Just(p.xs))


class TestTypeclassX(unittest.TestCase):
    def test_typeclasses_x(self):
        # Instantiate using defined higher-kinded type
        instance(Composite, t(t(Tree, 'a'), Maybe, [t(Tree, 'a')])).where(
            children=tree_children
        )

        # String representation for higher-kinded type.
        self.assertEqual(str(t(t(Tree, 'a'), Maybe, [t(Tree, 'a')])),
                         '((Tree a) Maybe [(Tree a)])')
