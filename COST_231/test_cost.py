import unittest

import numpy as np
from cost import calculate_path_losses


class Cost231Tests(unittest.TestCase):
    def test_path_losses_match_reference_values_at_five_kilometers(self):
        rural, urban, suburban = calculate_path_losses(np.array([5.0]))

        self.assertAlmostEqual(rural[0], 126.35, places=2)
        self.assertAlmostEqual(urban[0], 157.63, places=2)
        self.assertAlmostEqual(suburban[0], 153.12, places=2)
