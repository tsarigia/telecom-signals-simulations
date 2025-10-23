# Fourier Transform of a Rectangular Pulse

This project demonstrates the **Fourier Transform** (FT) of a **rectangular pulse** both *theoretically* (using analytical derivation) and *numerically* (using the Fast Fourier Transform - FFT).

---

## 💡 Theoretical Background

The time-domain signal, $x(t)$, is a rectangular pulse defined by its amplitude $A$ and duration $T$.

The pulse function $\Pi(t)$ is defined as:

$$
\Pi(t) =
\begin{cases}
1, & |t| \le \frac{1}{2} \\
0, & |t| > \frac{1}{2}
\end{cases}
$$

Thus, the time-domain signal $x(t)$ is:

$$
x(t) = A \, \Pi\*\left(\frac{t}{T}\right) =
\begin{cases}
A, & |t| \le \frac{T}{2} \\
0, & |t| > \frac{T}{2}
\end{cases}
$$

### 📐 Fourier Transform Derivation

The Fourier Transform $X(f)$ is computed using the integral definition:

$$
X(f) = \int_{-\infty}^{+\infty} x(t) \, e^{-j 2\pi f t} \, dt
$$

Applying this to $x(t)$ and restricting the integration limits:

$$
X(f) = \int_{-T/2}^{T/2} A \, e^{-j 2\pi f t} \, dt
$$

Solving the integral yields:

$$
X(f) = A \frac{\sin(\pi f T)}{\pi f}
$$

The final analytical result for the Fourier Transform of a rectangular pulse is expressed using the normalized $\mathrm{sinc}$ function $\left(\mathrm{sinc}(x) = \frac{\sin(\pi x)}{\pi x}\right)$:

$$\boxed{\mathbf{X(f) = A T \, \mathrm{sinc}(fT)}}$$

---

## ⚙️ Numerical Implementation (Using FFT)

The accompanying Python script implements the calculation of the spectrum using the **Fast Fourier Transform (FFT)** algorithm.

### Implementation Steps:
1.  **Define Signal:** A discrete time vector $t$ is created, and the corresponding rectangular pulse $x(t)$ is generated.
2.  **Compute FFT:** The Discrete Fourier Transform (DFT) is calculated using `numpy.fft.fft`.
3.  **Spectral Shift:** The zero-frequency component ($f=0$) is shifted to the center of the spectrum using `numpy.fft.fftshift` for proper visualization.
4.  **Plotting:** The script generates plots for:
    * The time-domain signal $x(t)$.
    * The Amplitude Spectrum $|X(f)|$.
    * The Phase Spectrum $\angle X(f)$.

---
## 1. Spectrum Analysis (Figure 2.13)

### A. Magnitude Spectrum $|X(f)|$ (Figure 2.13b)

The magnitude spectrum is $|X(f)| = |\mathrm{sinc}(fT)|$.

* **Maximum:** The maximum value is **1.0** at $\mathbf{f=0}$.
* **Zero Crossings (Nulls):** The spectrum crosses zero at discrete frequencies $\mathbf{f = k/T}$, where $k$ is any non-zero integer ($\mathbf{k = \pm 1, \pm 2, \pm 3, \dots}$).
* **Time-Bandwidth Reciprocity:** The energy of the signal is concentrated mainly within the main lobe $\left[-\frac{1}{T}, \frac{1}{T}\right]$. A smaller pulse duration ($T$) leads to a larger spectrum spread (wider bandwidth).

### B. Phase Spectrum $\theta(f)$ (Figure 2.13c)

Since $X(f)$ is a **real-valued function** (the FT of a real and even signal), its phase $\theta(f)$ is restricted to $0$ or $\mathbf{\pm\pi}$.

* **Phase Logic:** The phase changes by $\mathbf{\pm\pi}$ every time the function $X(f)$ transitions from a positive to a negative value.
* **Negative Regions:** This sign change occurs in the intervals where the secondary lobes are negative:
    $$\mathbf{\frac{n}{T} < |f| < \frac{n+1}{T}, \quad n \text{ is a positive odd integer}}$$
  ---
## 🚀 Requirements and Installation

To run the Python script for the numerical computation, you need the following libraries:

| Library | Purpose |
| :--- | :--- |
| **NumPy** | Numerical operations and FFT computation |
| **Matplotlib** | Plotting and visualization |

### Installation

You can install the required packages using `pip`:

```bash
pip install numpy matplotlib
