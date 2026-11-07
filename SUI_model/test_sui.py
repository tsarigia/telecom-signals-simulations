import unittest

import numpy as np

from sui import calc_sui_pathloss


class SuiPathlossTests(unittest.TestCase):
    def test_pathloss_matches_reference_values_at_five_kilometers(self):
        expected = {
            30: [165.37, 158.24, 153.63],
            80: [154.54, 146.66, 142.30],
        }

        for base_station_height, terrain_values in expected.items():
            with self.subTest(base_station_height=base_station_height):
                actual = [
                    calc_sui_pathloss(5.0, 1900, base_station_height, 3, terrain)
                    for terrain in "ABC"
                ]
                np.testing.assert_allclose(actual, terrain_values, atol=0.01)

    def test_pathloss_increases_with_distance(self):
        distances_km = np.array([1.0, 5.0, 10.0])

        pathloss = calc_sui_pathloss(distances_km, 1900, 30, 3, "A")

        self.assertEqual(pathloss.shape, distances_km.shape)
        self.assertTrue(np.all(np.diff(pathloss) > 0))

    def test_pathloss_decreases_with_higher_base_station(self):
        lower_height = calc_sui_pathloss(5.0, 1900, 30, 3, "A")
        higher_height = calc_sui_pathloss(5.0, 1900, 80, 3, "A")

        self.assertLess(higher_height, lower_height)

    def test_pathloss_order_matches_terrain_types(self):
        pathlosses = [
            calc_sui_pathloss(5.0, 1900, 30, 3, terrain) for terrain in "ABC"
        ]

        self.assertGreater(pathlosses[0], pathlosses[1])
        self.assertGreater(pathlosses[1], pathlosses[2])


if __name__ == "__main__":
    unittest.main()
