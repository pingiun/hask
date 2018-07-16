import unittest
from hask import has_instance, deriving, data, d, instance
from hask.Prelude import Show, Eq, Ord

te = TypeError


class TestTypeclass(unittest.TestCase):

    def test_typeclasses(self):
        A, B =\
                data.A == d.B & deriving(Show, Eq)
        self.assertTrue(has_instance(A, Show))
        self.assertTrue(has_instance(A, Eq))
        self.assertFalse(has_instance(A, Ord))
        with self.assertRaises(te):
            Ord[B]
        with self.assertRaises(te):
            A, B = data.A == d.B & deriving(Show, Ord)

        class example(object):
            def __str__(self):
                return "example()"

        instance(Show, example).where(show=example.__str__)
        with self.assertRaises(te):
            instance(1, example)
        with self.assertRaises(te):
            instance(example, str)

        from hask.Prelude import show
        self.assertEqual("example()", show(example()))
