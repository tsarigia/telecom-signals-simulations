import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft, fftfreq, fftshift

#  Time Vector & Sampling Configuration
fs = 2000  # Sampling frequency (2000 Hz > 2*fc for Nyquist compliance)
dt = 1 / fs
t = np.arange(0, 2.5, dt)  # Duration from 0 to 2.5 seconds
N = len(t)

#  Piecewise Baseband Message Signal m(t) 
m = np.zeros_like(t)
mask1 = (t >= 0.1) & (t < 1.0)
mask2 = (t >= 1.0) & (t < 1.9)
mask3 = (t >= 1.9) & (t <= 2.0)

m[mask1] = t[mask1]
m[mask2] = -t[mask2] + 2.0
m[mask3] = 0.1

#  Carrier Signal c(t) 
Ac = 2.0
fc = 35.0   # Carrier frequency: 35 Hz
c = Ac * np.cos(2 * np.pi * fc * t)

#  DSB-SC Modulated Signal u(t) 
u = m * c

# 5. Average Power Calculation 
P_m = np.mean(m**2)  # Average power of message signal m(t)
P_u = np.mean(u**2)  # Average power of modulated signal u(t)
P_u_theory = (Ac**2 / 2.0) * P_m

print("AVERAGE POWER CALCULATION RESULTS")
print(f"Message Signal Power (P_m):           {P_m:.4f} W")
print(f"Modulated Signal Power (Numerical):   {P_u:.4f} W")
print(f"Modulated Signal Power (Theoretical): {P_u_theory:.4f} W")

#  AWGN Noise Addition 
np.random.seed(42)
noise_std = 0.4
noise = np.random.normal(0, noise_std, N)
u_noisy = u + noise

# 7. Fast Fourier Transform (FFT) Analysis 
freqs = fftshift(fftfreq(N, dt))

M_f = fftshift(fft(m)) / N
C_f = fftshift(fft(c)) / N
U_f = fftshift(fft(u)) / N
U_noisy_f = fftshift(fft(u_noisy)) / N

#PLOTTING 

# Figure 1: Time-Domain Waveforms 
fig1, axs1 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

axs1[0].plot(t, m, "b", linewidth=2)
axs1[0].set(
    title="Task A: Message Signal m(t)",
    ylabel="Amplitude (V)",
    xlim=(0, 2.5),
    ylim=(-0.2, 1.2),
)
axs1[0].grid(True)

axs1[1].plot(t, c, "g", linewidth=1)
axs1[1].set(
    title="Task B: Carrier Signal c(t) (35 Hz)",
    ylabel="Amplitude (V)",
    xlim=(0, 2.5),
    ylim=(-2.5, 2.5),
)
axs1[1].grid(True)

axs1[2].plot(t, u, "r", linewidth=1.2)
axs1[2].plot(t, Ac * m, "k--", label="Envelope +Ac*m(t)", alpha=0.6)
axs1[2].plot(t, -Ac * m, "k--", label="Envelope -Ac*m(t)", alpha=0.6)
axs1[2].set(
    title="Task C: Modulated DSB-SC Signal u(t)",
    xlabel="Time t (s)",
    ylabel="Amplitude (V)",
    xlim=(0, 2.5),
    ylim=(-2.5, 2.5),
)
axs1[2].legend(loc="upper right")
axs1[2].grid(True)

# Figure 2: Frequency-Domain Spectra 
fig2, axs2 = plt.subplots(4, 1, figsize=(10, 10), constrained_layout=True)

axs2[0].plot(freqs, np.abs(M_f), "b", linewidth=1.5)
axs2[0].set(
    title="Task E: Magnitude Spectrum of Message Signal |M(f)|",
    ylabel="Magnitude",
    xlim=(-100, 100),
)
axs2[0].grid(True)

axs2[1].plot(freqs, np.abs(C_f), "g", linewidth=1.5)
axs2[1].set(
    title="Task F(i): Magnitude Spectrum of Carrier Signal |C(f)|",
    ylabel="Magnitude",
    xlim=(-100, 100),
)
axs2[1].grid(True)

axs2[2].plot(freqs, np.abs(U_f), "r", linewidth=1.5)
axs2[2].set(
    title="Task F(ii): Magnitude Spectrum of Modulated DSB-SC Signal |U(f)|",
    ylabel="Magnitude",
    xlim=(-100, 100),
)
axs2[2].grid(True)

axs2[3].plot(freqs, np.abs(U_noisy_f), "m", linewidth=1.5)
axs2[3].set(
    title="Task G: Magnitude Spectrum of Modulated Signal with Noise",
    xlabel="Frequency f (Hz)",
    ylabel="Magnitude",
    xlim=(-100, 100),
)
axs2[3].grid(True)

plt.show()