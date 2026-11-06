import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, fftshift


def message_signal(t):
    """Generate the piecewise baseband message signal."""
    message = np.zeros_like(t)
    mask1 = (t >= 0.1) & (t < 1.0)
    mask2 = (t >= 1.0) & (t < 1.9)
    mask3 = (t >= 1.9) & (t <= 2.0)

    message[mask1] = t[mask1]
    message[mask2] = -t[mask2] + 2.0
    message[mask3] = 0.1
    return message


def carrier_signal(t, amplitude=2.0, frequency=35.0):
    """Generate the sinusoidal carrier signal."""
    return amplitude * np.cos(2 * np.pi * frequency * t)


def modulate(message, carrier):
    """Generate the DSB-SC signal by multiplying message and carrier."""
    return message * carrier


def average_power(signal):
    """Return the mean-square power of a discrete-time signal."""
    return np.mean(signal**2)


def spectrum(signal, sample_interval):
    """Return the centered frequency axis and normalized FFT."""
    frequencies = fftshift(fftfreq(signal.size, sample_interval))
    values = fftshift(fft(signal)) / signal.size
    return frequencies, values


def main():
    # Time vector and sampling configuration.
    fs = 2000  # Sampling frequency (Hz).
    dt = 1 / fs
    t = np.arange(0, 2.5, dt)
    n_samples = len(t)

    # Generate the message, carrier, and DSB-SC modulated signal.
    amplitude = 2.0
    carrier_frequency = 35.0
    message = message_signal(t)
    carrier = carrier_signal(t, amplitude, carrier_frequency)
    modulated = modulate(message, carrier)

    # Compare numerical and theoretical average power.
    message_power = average_power(message)
    modulated_power = average_power(modulated)
    theoretical_power = (amplitude**2 / 2.0) * message_power

    print("AVERAGE POWER CALCULATION RESULTS")
    print(f"Message Signal Power (P_m):           {message_power:.4f} W")
    print(f"Modulated Signal Power (Numerical):   {modulated_power:.4f} W")
    print(f"Modulated Signal Power (Theoretical): {theoretical_power:.4f} W")

    # Add reproducible additive white Gaussian noise.
    np.random.seed(42)
    noise_std = 0.4
    noisy_modulated = modulated + np.random.normal(0, noise_std, n_samples)

    # Compute centered spectra for plotting.
    frequencies, message_spectrum = spectrum(message, dt)
    _, carrier_spectrum = spectrum(carrier, dt)
    _, modulated_spectrum = spectrum(modulated, dt)
    _, noisy_spectrum = spectrum(noisy_modulated, dt)

    # Plot time-domain waveforms.
    _, time_axes = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

    time_axes[0].plot(t, message, "b", linewidth=2)
    time_axes[0].set(
        title="Task A: Message Signal m(t)",
        ylabel="Amplitude (V)",
        xlim=(0, 2.5),
        ylim=(-0.2, 1.2),
    )
    time_axes[0].grid(True)

    time_axes[1].plot(t, carrier, "g", linewidth=1)
    time_axes[1].set(
        title="Task B: Carrier Signal c(t) (35 Hz)",
        ylabel="Amplitude (V)",
        xlim=(0, 2.5),
        ylim=(-2.5, 2.5),
    )
    time_axes[1].grid(True)

    time_axes[2].plot(t, modulated, "r", linewidth=1.2)
    time_axes[2].plot(
        t, amplitude * message, "k--", label="Envelope +Ac*m(t)", alpha=0.6
    )
    time_axes[2].plot(
        t, -amplitude * message, "k--", label="Envelope -Ac*m(t)", alpha=0.6
    )
    time_axes[2].set(
        title="Task C: Modulated DSB-SC Signal u(t)",
        xlabel="Time t (s)",
        ylabel="Amplitude (V)",
        xlim=(0, 2.5),
        ylim=(-2.5, 2.5),
    )
    time_axes[2].legend(loc="upper right")
    time_axes[2].grid(True)

    # Plot frequency-domain magnitude spectra.
    _, frequency_axes = plt.subplots(4, 1, figsize=(10, 10), constrained_layout=True)
    spectra = (
        (message_spectrum, "Task E: Magnitude Spectrum of Message Signal |M(f)|"),
        (carrier_spectrum, "Task F(i): Magnitude Spectrum of Carrier Signal |C(f)|"),
        (
            modulated_spectrum,
            "Task F(ii): Magnitude Spectrum of Modulated DSB-SC Signal |U(f)|",
        ),
        (noisy_spectrum, "Task G: Magnitude Spectrum of Modulated Signal with Noise"),
    )
    for axis, (values, title) in zip(frequency_axes, spectra):
        axis.plot(frequencies, np.abs(values), linewidth=1.5)
        axis.set(title=title, ylabel="Magnitude", xlim=(-100, 100))
        axis.grid(True)

    frequency_axes[-1].set_xlabel("Frequency f (Hz)")
    plt.show()


if __name__ == "__main__":
    main()
