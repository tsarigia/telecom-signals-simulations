import matplotlib.pyplot as plt
import numpy as np

# 1. Define the pulse parameters.
A = 1.0     # Pulse amplitude.
T = 2.0     # Pulse duration (seconds).
Fs = 200.0  # Sampling frequency (Hz).
Ts = 1.0 / Fs
N = 4096    # Number of samples.

# 2. Sample at time-bin centers so the pulse contains exactly T * Fs samples.
t = (np.arange(N) - N / 2 + 0.5) * Ts
x_t = np.where(np.abs(t) < T / 2, A, 0.0)

# 3. Compute the FFT and its corresponding frequency axis.
X_fft = np.fft.fft(x_t)
f = np.fft.fftfreq(N, d=Ts)

X_shift = np.fft.fftshift(X_fft)
f_shift = np.fft.fftshift(f)
X_fft_scaled = X_shift * Ts
# Correct for the time axis starting at t[0], rather than at zero.
X_fft_scaled *= np.exp(-2j * np.pi * f_shift * t[0])

# 4. Compute the analytical Fourier transform for comparison.
def normalized_sinc(value):
    """Return the normalized sinc function, sin(pi*x)/(pi*x)."""
    return np.sinc(value)

X_anal = A * T * normalized_sinc(f_shift * T)

# 5. Compute the analytical phase, which is 0 or pi for this real, even signal.
phase_anal = np.where(X_anal < 0, np.pi, 0.0)

# The phase is undefined at spectral zeros, so omit values with very small magnitude.
phase_threshold = np.max(np.abs(X_anal)) * 1e-3
phase_anal[np.abs(X_anal) < phase_threshold] = np.nan
phase_fft = np.angle(X_fft_scaled)
phase_fft[np.abs(X_fft_scaled) < phase_threshold] = np.nan
# Represent negative real values consistently as +pi despite FFT round-off.
phase_fft[np.isclose(phase_fft, -np.pi)] = np.pi

# 6. Mark the theoretical spectral zeros at nonzero integer multiples of 1/T.
zero_points = np.arange(-5, 6) / T
zero_points = zero_points[zero_points != 0]

# 7. Plot the pulse and compare analytical and numerical spectra.
plt.figure(figsize=(10, 12))

# (a) Rectangular pulse.
plt.subplot(3, 1, 1)
plt.plot(t, x_t, 'b', linewidth=2)
plt.title('(a) Rectangular Pulse $x(t)$', fontsize=14, weight='bold')
plt.xlabel('$t$ (seconds)')
plt.ylabel('$x(t)$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(-0.2, A + 0.2)
plt.xlim(-2*T, 2*T)
plt.xticks([-T/2, T/2], ['-T/2', 'T/2'])

# (b) Magnitude spectrum.
plt.subplot(3, 1, 2)
plt.plot(f_shift, np.abs(X_anal) / (A * T), 'r-', linewidth=2, label='Analytical $|X(f)|/(AT)$')
plt.plot(f_shift, np.abs(X_fft_scaled) / (A * T), 'b.', alpha=0.5, label='FFT $|X(f)|/(AT)$')
for zp in zero_points:
    plt.axvline(zp, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
plt.title('(b) Normalized Magnitude Spectrum $|X(f)|/(AT)$', fontsize=14, weight='bold')
plt.xlabel('$f$ (Hz)')
plt.ylabel('$|X(f)|$')
plt.xlim(-5/T, 5/T)
plt.ylim(0, 1.1)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xticks([-2/T, -1/T, 1/T, 2/T], ['-2/T', '-1/T', '1/T', '2/T'])
plt.axvline(0, color='gray', linewidth=0.8)

# (c) Phase spectrum.
plt.subplot(3, 1, 3)
plt.step(f_shift, phase_anal, 'g-', linewidth=2, label='Analytical phase')
plt.plot(f_shift, phase_fft, 'b.', alpha=0.5, label='FFT phase')
for zp in zero_points:
    plt.axvline(zp, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
plt.title('(c) Phase Spectrum $\\angle X(f)$', fontsize=14, weight='bold')
plt.xlabel('$f$ (Hz)')
plt.ylabel('$\\theta(f)$ (rad)')
plt.yticks([-np.pi, 0, np.pi], ['$-\\pi$', '0', '$\\pi$'])
plt.xlim(-5/T, 5/T)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower left')
plt.xticks([-2/T, -1/T, 1/T, 2/T], ['-2/T', '-1/T', '1/T', '2/T'])
plt.axvline(0, color='gray', linewidth=0.8)

plt.tight_layout(pad=3.0)
plt.show()