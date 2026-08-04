import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, fftshift

# 1. Sampling Configuration
fs = 10000  # Sampling frequency: 10 kHz (>> 2*fc for high resolution)
dt = 1 / fs
t = np.arange(-0.5, 2.5, dt)  # Time window: -0.5 to 2.5 seconds
N = len(t)

# 2. Piecewise Message Signal m(t) 
m = np.full_like(t, 0.1)  # Default value: 0.1 V ("otherwise")
mask1 = (t >= 0.0) & (t < 1.0)
mask2 = (t >= 1.0) & (t <= 2.0)

m[mask1] = t[mask1]
m[mask2] = -t[mask2] + 2.0

# 3. Carrier Signal c(t) 
Ac = 1.0
fc = 1000.0  # Carrier frequency: 1000 Hz
c = Ac * np.cos(2 * np.pi * fc * t)

# 4. FM Modulated Signal s_FM(t) 
kf = 25.0  # Frequency deviation constant: 25 Hz/V

# Instantaneous phase via numerical integration (cumsum * dt)
phase = 2 * np.pi * fc * t + 2 * np.pi * kf * dt * np.cumsum(m)
s_fm = Ac * np.cos(phase)

f_min = fc + kf * np.min(m[(t >= 0) & (t <= 2)])
f_max = fc + kf * np.max(m)
delta_f = kf * np.max(m)
Bm = 1.0  # Significant baseband bandwidth of message (~1 Hz)
beta = delta_f / Bm
B_fm_carson = 2 * (delta_f + Bm)


print(
    f"Task (α) Instantaneous Frequency Range: [{f_min:.1f} Hz, {f_max:.1f} Hz]"
)
print(
    f"Task (ε) Modulation Index (β):          {beta:.1f} (Wideband FM)"
)
print(
    f"Task (β) Carson's FM Bandwidth (B_FM):  {B_fm_carson:.1f} Hz"
)
print("-" * 40)

# 5. FFT Spectral Analysis 
freqs = fftshift(fftfreq(N, dt))
M_f = fftshift(fft(m)) / N
C_f = fftshift(fft(c)) / N
S_fm_f = fftshift(fft(s_fm)) / N


# Figure 1: Time-Domain Waveforms 
fig1, axs1 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

axs1[0].plot(t, m, "b", linewidth=2)
axs1[0].set(
    title="Task γ(i): Message Signal m(t)",
    ylabel="Amplitude (V)",
    xlim=(-0.5, 2.5),
    ylim=(0, 1.1),
)
axs1[0].grid(True)

# Zoomed window (0.8s to 1.2s) to visibly see carrier & FM oscillations
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

# Figure 2: Frequency-Domain Spectra 
fig2, axs2 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

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