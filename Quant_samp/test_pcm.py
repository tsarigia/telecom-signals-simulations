import unittest

import numpy as np

from pcm import dpcm_pcm, uniform_pcm


class UniformPcmTests(unittest.TestCase):
    def test_selects_the_correct_quantization_bins(self):
        samples = np.array([-0.01, 0.005])

        reconstructed, error, _ = uniform_pcm(samples, 256)

        np.testing.assert_allclose(reconstructed, [-0.01171875, 0.00390625])
        np.testing.assert_allclose(error, samples - reconstructed)

    def test_clips_samples_to_the_outer_quantization_levels(self):
        samples = np.array([-1.0, 1.0])

        reconstructed, _, _ = uniform_pcm(samples, 256)

        np.testing.assert_allclose(reconstructed, [-0.99609375, 0.99609375])


class DpcmTests(unittest.TestCase):
    def test_quantizes_prediction_error_to_the_correct_bin(self):
        reconstructed, error, _ = dpcm_pcm(np.array([0.01]), 256)

        np.testing.assert_allclose(reconstructed, [0.009765625])
        np.testing.assert_allclose(error, [0.000234375])


if __name__ == "__main__":
    unittest.main()
