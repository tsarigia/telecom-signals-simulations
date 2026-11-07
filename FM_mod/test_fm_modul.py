import unittest

import numpy as np
from fm_modul import carrier_signal, fm_modulate, message_signal


class FmSignalTests(unittest.TestCase):
    def test_message_signal_piecewise_values(self):# This test checks if the message_signal function correctly generates a piecewise linear signal based on the specified time intervals. It verifies that the output matches the expected values for given time points.
        times = np.array([-0.1, 0.0, 0.25, 1.0, 1.5, 2.0, 2.1])
        expected = np.array([0.1, 0.0, 0.25, 1.0, 0.5, 0.0, 0.1])

        np.testing.assert_allclose(message_signal(times), expected)

    def test_carrier_signal_uses_configured_amplitude_and_frequency(self):# This test checks if the carrier_signal function correctly generates a cosine wave based on the specified amplitude and frequency. It verifies that the output matches the expected values for given time points.
        times = np.array([0.0, 0.025, 0.05])
        expected = 2.0 * np.cos(2 * np.pi * 4.0 * times)

        np.testing.assert_allclose(
            carrier_signal(times, amplitude=2.0, frequency=4.0), expected
        )

    def test_fm_modulation_integrates_message_into_phase(self):# This test checks if the fm_modulate function correctly integrates the message signal into the phase of the carrier signal. It verifies that the output matches the expected values for given time points, carrier frequency, and frequency sensitivity.
        times = np.arange(0.0, 0.01, 0.001)
        message = np.full_like(times, 0.4)# This creates a message signal with a constant value of 0.4 for all time points, which will be used to modulate the carrier signal in the FM modulation process.
        dt = times[1] - times[0]
        expected_phase = (
            2 * np.pi * 10.0 * times
            + 2 * np.pi * 2.0 * dt * np.cumsum(message)# This calculates the expected phase of the FM modulated signal by integrating the message signal into the phase of the carrier signal. The cumulative sum of the message signal is multiplied by the frequency sensitivity and time step to account for the modulation effect over time.
        )

        np.testing.assert_allclose(
            fm_modulate(
                times,
                message,
                carrier_frequency=10.0,
                frequency_sensitivity=2.0,
            ),
            np.cos(expected_phase),
        )


if __name__ == "__main__":
    unittest.main()
