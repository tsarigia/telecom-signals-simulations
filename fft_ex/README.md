# Fourier Transform of a Rectangular Pulse

This project demonstrates the **Fourier Transform** of a **rectangular pulse** both *theoretically* and *numerically* (using the Fast Fourier Transform - FFT).

---

## 🧠 Theoretical Background

The time-domain signal is defined as:

\[
x(t) = A \, \Pi\!\left(\frac{t}{T}\right)
\]

where

\[
\Pi(t) =
\begin{cases}
1, & |t| \le \frac{1}{2} \\
0, & |t| > \frac{1}{2}
\end{cases}
\]

Thus,

\[
x(t) =
\begin{cases}
A, & |t| \le \frac{T}{2} \\
0, & |t| > \frac{T}{2}
\end{cases}
\]

---

### 📘 Fourier Transform Definition

\[
X(f) = \int_{-\infty}^{+\infty} x(t) \, e^{-j 2\pi f t} \, dt
\]

Applying this to \( x(t) = A \, \Pi\left(\frac{t}{T}\right) \):

\[
X(f) = \int_{-T/2}^{T/2} A \, e^{-j 2\pi f t} \, dt
\]

Solving the integral:

\[
X(f) = A \frac{\sin(\pi f T)}{\pi f}
\]

Therefore, the Fourier Transform of a rectangular pulse is:

\[
\boxed{X(f) = A T \, \mathrm{sinc}(fT)}
\]

where

\[
\mathrm{sinc}(x) = \frac{\sin(\pi x)}{\pi x}
\]

---

## ⚙️ Numerical Implementation

The script computes the amplitude and phase spectra using the **Fast Fourier Transform (FFT)**.

### Steps:
1. Define a time vector \( t \) and create the rectangular pulse \( x(t) \).
2. Compute the FFT using `numpy.fft.fft`.
3. Shift zero frequency to the center using `fftshift`.
4. Plot:
   - Time-domain signal \( x(t) \)
   - Amplitude spectrum \( |X(f)| \)
   - Phase spectrum \( \angle X(f) \)

---

## 🧩 Requirements

```bash
pip install numpy matplotlib
