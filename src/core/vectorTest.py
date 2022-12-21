import unittest

from core.vector import Vector


class VectorTest(unittest.TestCase):
    def test_vector_creation(self):
        v = Vector([0, 1, 3])
        self.assertEqual(v.shape(), 3)

    def test_vector_vector_addition(self):
        v1 = Vector([0, 1, 3])
        v2 = Vector([2, 8, 1])
        self.assertEqual(v1 + v2, Vector([2, 9, 4]))

    def test_vector_int_addition(self):
        v1 = Vector([0, 2, 8])
        v2 = 3
        self.assertEqual(v1 + v2, Vector([3, 5, 11]))

    def test_vector_vector_addition_throw_error_if_not_same_length(self):
        v1 = Vector([0, 1, 3])
        v2 = Vector([2, 3])
        with self.assertRaises(ValueError):
            v1 + v2

    def test_vector_vector_addition_throw_error_if_other_is_not_vector_or_int(self):
        v1 = Vector([0, 1, 3])
        v2 = {0, 4}
        with self.assertRaises(ValueError):
            v1 + v2


if __name__ == '__main__':
    unittest.main()
