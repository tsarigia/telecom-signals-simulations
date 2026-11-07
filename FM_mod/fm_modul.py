import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, fftshift


def message_signal(times):
    message = np.full_like(times, 0.1, dtype=float)# np.full_like creates an array of the same shape and type as 'times', filled with 0.1. This initializes the message signal with a default value of 0.1 for all time points.
    mask1 = (times >= 0.0) & (times < 1.0)
    mask2 = (times >= 1.0) & (times <= 2.0)

    message[mask1] = times[mask1]
    message[mask2] = -times[mask2] + 2.0
    return message


def carrier_signal(times, amplitude=1.0, frequency=1000.0):
    return amplitude * np.cos(2 * np.pi * frequency * times)


def fm_modulate(
    times,
    message,
    amplitude=1.0,
    carrier_frequency=1000.0,
    frequency_sensitivity=25.0,
):
    dt = times[1] - times[0]
    phase = (
        2 * np.pi * carrier_frequency * times
        + 2 * np.pi * frequency_sensitivity * dt * np.cumsum(message)
    )
    return amplitude * np.cos(phase)


def main():
    fs = 10000
    dt = 1 / fs
    t = np.arange(-0.5, 2.5, dt)
    N = len(t)

    m = message_signal(t)
    Ac = 1.0
    fc = 1000.0
    c = carrier_signal(t, Ac, fc)
    kf = 25.0
    s_fm = fm_modulate(t, m, Ac, fc, kf)

    f_min = fc + kf * np.min(m[(t >= 0) & (t <= 2)])
    f_max = fc + kf * np.max(m)
    delta_f = kf * np.max(m)
    Bm = 1.0
    beta = delta_f / Bm
    B_fm_carson = 2 * (delta_f + Bm)

    print(f"Task (α) Instantaneous Frequency Range: [{f_min:.1f} Hz, {f_max:.1f} Hz]")
    print(f"Task (ε) Modulation Index (β):{beta:.1f} (Wideband FM)")
    print(f"Task (β) Carson's FM Bandwidth (B_FM):  {B_fm_carson:.1f} Hz")
    print("-" * 40)

    freqs = fftshift(fftfreq(N, dt))# it returns the frequencies corresponding to the FFT output, shifted so that zero frequency is in the center of the array.
    M_f = fftshift(fft(m)) / N # Message spectrum
    C_f = fftshift(fft(c)) / N # Carrier spectrum
    S_fm_f = fftshift(fft(s_fm)) / N # FM modulated spectrum

    _fig1, axs1 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

    axs1[0].plot(t, m, "b", linewidth=2)
    axs1[0].set(
        title="Task γ(i): Message Signal m(t)",
        ylabel="Amplitude (V)",
        xlim=(-0.5, 2.5),
        ylim=(0, 1.1),
    )
    axs1[0].grid(True)

    zoom_t = (t >= 0.8) & (t <= 1.2)

    axs1[1].plot(t[zoom_t], c[zoom_t], "g", linewidth=1)
    axs1[1].set(
        title="Task : Carrier Signal c(t) [Zoomed 0.8s - 1.2s at 1000 Hz]",
        ylabel="Amplitude (V)",
        ylim=(-1.2, 1.2),
    )
    axs1[1].grid(True)

    axs1[2].plot(t[zoom_t], s_fm[zoom_t], "r", linewidth=1)
    axs1[2].set(
        title="Task: Modulated FM Signal s_FM(t) [Zoomed 0.8s - 1.2s]",
        xlabel="Time t (s)",
        ylabel="Amplitude (V)",
        ylim=(-1.2, 1.2),
    )
    axs1[2].grid(True)

    _fig2, axs2 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

    axs2[0].plot(freqs, np.abs(M_f), "b", linewidth=1.5)
    axs2[0].set(
        title="Task (i): Message Spectrum |M(f)| (Baseband)",
        ylabel="Magnitude",
        xlim=(-10, 10),
    )
    axs2[0].grid(True)

    axs2[1].plot(freqs, np.abs(C_f), "g", linewidth=1.5)
    axs2[1].set(
        title="Task (ii): Carrier Spectrum |C(f)| (Impulses at ±1000 Hz)",
        ylabel="Magnitude",
        xlim=(950, 1050),
    )
    axs2[1].grid(True)

    axs2[2].plot(freqs, np.abs(S_fm_f), "r", linewidth=1.5)
    axs2[2].axvline(
        fc - B_fm_carson / 2,
        color="k",
        linestyle="--",
        alpha=0.6,
        label="Carson Bandwidth Limits (±26 Hz)",
    )
    axs2[2].axvline(fc + B_fm_carson / 2, color="k", linestyle="--", alpha=0.6)
    axs2[2].set(
        title=f"Task (iii): FM Spectrum |S_FM(f)| around 1000 Hz (Carson Bandwidth ≈ {B_fm_carson} Hz)",
        xlabel="Frequency f (Hz)",
        ylabel="Magnitude",
        xlim=(950, 1050),
    )
    axs2[2].legend(loc="upper right")
    axs2[2].grid(True)

    plt.show()


if __name__ == "__main__":
    main()
