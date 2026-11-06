import matplotlib.pyplot as plt
import numpy as np


# Define the signal x(t).
def x(t):
    x_t = np.zeros_like(t)
    x_t[(t >= -3) & (t <= -2)] = 2
    x_t[np.abs(t) < 2] = np.abs(t[np.abs(t) < 2]) + 2
    x_t[(t >= 2) & (t <= 3)] = 1.5
    return x_t

# Create 2000 samples from -5 to 5 seconds.
t = np.linspace(-5, 5, 2000)
x_t = x(t)

# Zero-padding gives a denser frequency grid for plotting; it does not
# increase the signal's actual frequency resolution.
N = 8192
dt = t[1] - t[0]
X_f = np.fft.fftshift(np.fft.fft(x_t, N)) * dt
freq = np.fft.fftshift(np.fft.fftfreq(N, d=dt))

# Account for the fact that the sampled time axis starts at t[0], not at zero.
X_f *= np.exp(-2j * np.pi * freq * t[0])

# Normalize the magnitude for relative comparison; phase is in radians.
magnitude = np.abs(X_f) / np.max(np.abs(X_f))
phase = np.angle(X_f)

# Display only the frequency range from -10 Hz to 10 Hz.
mask = (freq >= -10) & (freq <= 10)

# Plot the signal and its spectra.
plt.figure(figsize=(12,8))

# Time-domain signal.
plt.subplot(3,1,1)
plt.plot(t, x_t, 'b', linewidth=2)
plt.title('Σήμα x(t)')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)

# Magnitude spectrum.
plt.subplot(3,1,2)
plt.plot(freq[mask], magnitude[mask], 'r')
plt.title('Φάσμα πλάτους |X(f)| (ομαλοποιημένο)')
plt.xlabel('Συχνότητα (Hz)')
plt.ylabel('|X(f)|')
plt.grid(True)

# Phase spectrum.
plt.subplot(3,1,3)
plt.plot(freq[mask], phase[mask], 'g')
plt.title('Φάσμα φάσης ∠X(f)')
plt.xlabel('Συχνότητα (Hz)')
plt.ylabel('Φάση (rad)')
plt.grid(True)

plt.tight_layout()
plt.show()
