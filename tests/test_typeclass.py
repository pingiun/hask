import unittest
from hask import has_instance, deriving, data, d, instance
from hask.Prelude import Show, Eq, Ord


class TestTypeclass(unittest.TestCase):

    def test_typeclasses(self):
        A, B = data.A == d.B & deriving(Show, Eq)
        self.assertTrue(has_instance(A, Show))
        self.assertTrue(has_instance(A, Eq))
        self.assertFalse(has_instance(A, Ord))
        with self.assertRaises(TypeError):
            Ord[B]
        with self.assertRaises(TypeError):
            '''Notes:

            >>> a = data.A    # __new_tcon_enum__('A')
            >>> b = d.B    # __new_dcon_enum__('B')
            >>> d = d.B & deriving(Show, Ord) \
            ... # __new_dcon_deriving__('B', (), (Show, Ord))
            >>> adt = (a == d) \
            ... # build_ADT('A', (), [('B', ())], (Show, Ord))

            '''
            A, B = data.A == d.B & deriving(Show, Ord)

        class example(object):
            def __str__(self):
                return "example()"

        instance(Show, example).where(show=example.__str__)
        with self.assertRaises(TypeError):
            instance(1, example)
        with self.assertRaises(TypeError):
            instance(example, str)

        from hask.Prelude import show
        self.assertEqual("example()", show(example()))
