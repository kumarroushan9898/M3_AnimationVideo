import unittest

import numpy as np

from Code.math_utils import A, I, INPUT, ORIGIN, UNIT_SQUARE, intermediate, mapped, verify_math


class TransformationTests(unittest.TestCase):
    def test_exact_symbolic_verification(self):
        self.assertTrue(all(verify_math().values()))

    def test_numeric_example(self):
        self.assertEqual(mapped(INPUT), (5, 1))
        self.assertEqual(tuple(map(mapped, UNIT_SQUARE)), ((0, 0), (2, 0), (3, 1), (1, 1)))

    def test_animation_interpolates_one_linear_map(self):
        np.testing.assert_array_equal(intermediate(0), I)
        np.testing.assert_array_equal(intermediate(1), A)
        halfway = intermediate(0.5)
        self.assertEqual(mapped(ORIGIN, halfway), ORIGIN)
        self.assertEqual(mapped(INPUT, halfway), (3.5, 1))
        np.testing.assert_allclose(mapped((1, 1), halfway),
                                   np.add(mapped((1, 0), halfway), mapped((0, 1), halfway)))


if __name__ == "__main__":
    unittest.main()
