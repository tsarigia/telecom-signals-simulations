import unittest

import numpy as np
from freq_diagr import compute_fourier_transform, x


class SignalTests(unittest.TestCase):
    def test_piecewise_signal_values(self):
        times = np.array([-4, -3, -2.5, -2, -1, 0, 1, 2, 2.5, 3, 4], dtype=float)
        expected = np.array([0, 2, 2, 2, 3, 2, 3, 1.5, 1.5, 1.5, 0])

        np.testing.assert_array_equal(x(times), expected)

    def test_signal_is_not_even(self):
        times = np.array([2.5])

        self.assertNotEqual(x(-times)[0], x(times)[0])


class FourierTransformTests(unittest.TestCase):
    def test_transform_accounts_for_time_origin(self):
        times = np.linspace(-5, 5, 2000)
        samples = x(times)
        frequencies, spectrum = compute_fourier_transform(times, samples, 8192)
        bin_index = np.argmin(np.abs(frequencies - 0.5))
        frequency = frequencies[bin_index]
        dt = times[1] - times[0]
        direct_sum = dt * np.sum(
            samples * np.exp(-2j * np.pi * frequency * times)
        )

        self.assertAlmostEqual(spectrum[bin_index], direct_sum, places=10)

    def test_zero_frequency_approximates_signal_area(self):
        times = np.linspace(-5, 5, 2000)
        frequencies, spectrum = compute_fourier_transform(times, x(times), 8192)
        zero_index = np.argmin(np.abs(frequencies))

        self.assertAlmostEqual(spectrum[zero_index].real, 15.5, delta=0.02)
        self.assertAlmostEqual(spectrum[zero_index].imag, 0, places=12)


if __name__ == "__main__":
    unittest.main()
