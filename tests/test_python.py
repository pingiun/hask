import unittest

from hask3 import __

te = TypeError


class TestPython(unittest.TestCase):

    def test_builtins(self):
        from hask3.Python.builtins import callable, cmp, delattr, divmod
        from hask3.Python.builtins import getattr, hasattr, hash  # noqa: F401
        from hask3.Python.builtins import hex, isinstance, issubclass, len, oct  # noqa: F401
        from hask3.Python.builtins import repr, setattr, sorted  # noqa: F401

        class Example(object):
            a = 1

        self.assertTrue(callable(__+1))
        self.assertEqual(1, cmp(10) % 9)
        self.assertEqual(divmod(5)(2), (2, 1))

        with self.assertRaises(te):
            cmp(1, "a")

        with self.assertRaises(te):
            oct(1.0)
        with self.assertRaises(te):
            hex(1.0)
        with self.assertRaises(te):
            hasattr(list)(len)
        with self.assertRaises(te):
            getattr(list)(len)
        with self.assertRaises(te):
            setattr(list)(len)
        with self.assertRaises(te):
            delattr(list)(len)
