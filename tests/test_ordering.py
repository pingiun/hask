import unittest

from hask3 import has_instance
from hask3 import Read, Show, Eq, Ord, Bounded


class TestOrdering(unittest.TestCase):

    def test_ordering(self):
        from hask3.Data.Ord import Ordering, LT, EQ, GT
        self.assertTrue(has_instance(Ordering, Read))
        self.assertTrue(has_instance(Ordering, Show))
        self.assertTrue(has_instance(Ordering, Eq))
        self.assertTrue(has_instance(Ordering, Ord))
        self.assertTrue(has_instance(Ordering, Bounded))

        from hask3.Prelude import show
        self.assertEqual("LT", show(LT))
        self.assertEqual("EQ", show(EQ))
        self.assertEqual("GT", show(GT))

        self.assertTrue(EQ == EQ and not EQ != EQ)
        self.assertTrue(LT == LT and not LT != LT)
        self.assertTrue(GT == GT and not GT != GT)
        self.assertFalse(LT == EQ)
        self.assertFalse(LT == GT)
        self.assertFalse(EQ == GT)
        self.assertTrue(LT < EQ < GT)
        self.assertTrue(LT <= EQ < GT)
        self.assertTrue(LT < EQ <= GT)
        self.assertTrue(LT <= EQ <= GT)
        self.assertFalse(LT > EQ or EQ > GT)
        self.assertFalse(LT >= EQ or EQ > GT)
        self.assertFalse(LT > EQ or EQ >= GT)
        self.assertFalse(LT >= EQ or EQ >= GT)

        with self.assertRaises(TypeError):
            EQ + EQ
