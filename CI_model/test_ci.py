import unittest

import numpy as np
from ci import calc_fspl, calc_pl


class CloseInModelTests(unittest.TestCase):
    def test_free_space_path_loss_at_one_meter(self):# it should be 61.34 dB at 28 GHz
        self.assertAlmostEqual(calc_fspl(28), 61.34, places=2)

    def test_path_loss_matches_reference_values_at_150_meters(self):# testing path loss at 150 meters for 28 GHz with reference values
        path_losses = calc_pl(28, np.array([150.0]), np.array([2.1, 3.19]))

        np.testing.assert_allclose(path_losses, [107.04, 130.76], atol=0.005)

    def test_path_loss_increases_with_distance(self):# testing that path loss increases with distance for 28 GHz and PLE of 2.1
        distances = np.array([10.0, 100.0, 500.0])

        path_losses = calc_pl(28, distances, 2.1)

        self.assertTrue(np.all(np.diff(path_losses) > 0))


if __name__ == "__main__":
    unittest.main()
