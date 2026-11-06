import unittest

import numpy as np
from dsb import average_power, carrier_signal, message_signal, modulate


class DsbSignalTests(unittest.TestCase):
    def test_message_signal_piecewise_values(self):
        times = np.array([0.0, 0.1, 0.5, 1.0, 1.5, 1.9, 2.0, 2.1])
        expected = np.array([0.0, 0.1, 0.5, 1.0, 0.5, 0.1, 0.1, 0.0])

        np.testing.assert_allclose(message_signal(times), expected)

    def test_modulated_signal_is_product_of_message_and_carrier(self):
        times = np.arange(0.0, 2.5, 0.001)
        message = message_signal(times)
        carrier = carrier_signal(times)

        np.testing.assert_allclose(modulate(message, carrier), message * carrier)

    def test_modulated_power_matches_theoretical_approximation(self):
        sample_rate = 2000
        times = np.arange(0, 2.5, 1 / sample_rate)
        message = message_signal(times)
        carrier = carrier_signal(times)
        modulated = modulate(message, carrier)
        theoretical_power = (2.0**2 / 2.0) * average_power(message)

        self.assertTrue(
            np.isclose(average_power(modulated), theoretical_power, rtol=1e-4)
        )


if __name__ == "__main__":
    unittest.main()
