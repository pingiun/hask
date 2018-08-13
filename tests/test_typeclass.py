import unittest
from hask3 import has_instance, deriving, data, d, instance
from hask3.Prelude import Show, Eq, Ord


class TestTypeclass(unittest.TestCase):

    def test_typeclasses(self):
        A, B = data.A == d.B & deriving(Show, Eq)
        self.assertTrue(has_instance(A, Show))
        self.assertTrue(has_instance(A, Eq))
        if has_instance(A, Ord):
            import ipdb; ipdb.set_trace()    # TODO: Remove this
            has_instance(A, Ord)
        self.assertFalse(has_instance(A, Ord))     # Failed here
        with self.assertRaises(TypeError):
            Ord[B]
        with self.assertRaises(TypeError):
            '''Notes:

            >>> x = data.X    # __new_tcon_enum__('X')
            >>> y = d.Y    # __new_dcon_enum__('Y')
            >>> z = d.Y & deriving(Show, Ord) \
            ... # __new_dcon_deriving__('Y', (), (Show, Ord))
            >>> adt = (x == z) \
            ... # build_ADT('X', (), [('Y', ())], (Show, Ord))

            '''
            try:
                X, Y = data.X == d.Y & deriving(Show, Ord)
                # Eq_Person
                import ipdb; ipdb.set_trace()    # TODO: Remove this
                has_instance(X, Eq)
            except TypeError:
                raise
            except Exception as error:
                import ipdb; ipdb.set_trace()    # TODO: Remove this
                print(error)


        class example(object):
            def __str__(self):
                return "example()"

        instance(Show, example).where(show=example.__str__)
        with self.assertRaises(TypeError):
            instance(1, example)
        with self.assertRaises(TypeError):
            instance(example, str)

        from hask3.Prelude import show
        self.assertEqual("example()", show(example()))
