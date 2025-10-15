# 📘 Signal Spectrum Analysis – Fourier Series and Fourier Transform

## 🧠 Theoretical Background

The **Fourier Transform** is a mathematical tool that represents a time-domain signal \( x(t) \) as a function of frequency \( f \).  
It expresses the signal as a sum (or continuum) of sinusoids with different frequencies, amplitudes, and phases.

The **continuous-time Fourier Transform** is defined as:

\[
X(f) = \int_{-\infty}^{\infty} x(t) e^{-j 2\pi f t} \, dt
\]

The inverse transform reconstructs the time-domain signal:

\[
x(t) = \int_{-\infty}^{\infty} X(f) e^{j 2\pi f t} \, df
\]

The **magnitude** and **phase** of the spectrum are given by:

\[
|X(f)| = \sqrt{ \Re\{X(f)\}^2 + \Im\{X(f)\}^2 }
\]
\[
\angle X(f) = \tan^{-1}\left( \frac{\Im\{X(f)\}}{\Re\{X(f)\}} \right)
\]

These two quantities provide complementary information:
- The **magnitude spectrum** describes how much of each frequency is present.
- The **phase spectrum** encodes time and symmetry information about the signal.

---
## 📝 Exercise Statement

**Goal:**  
Analyze the frequency content of a given signal \( x(t) \) by computing and plotting:
1. The **magnitude spectrum** \( |X(f)| \)
2. The **phase spectrum** \( \angle X(f) \)

The signal is defined piecewise as:

\[
x(t) =
\begin{cases}
2, & -3 \le t \le -2 \\
|t| + 2, & -2 < t < 2 \\
1.5, & 2 \le t \le 3 \\
0, & \text{otherwise}
\end{cases}
\]

You are required to:
- Compute the frequency-domain representation \( X(f) \) using the **Fourier Transform**:
  \[
  X(f) = \int_{-\infty}^{\infty} x(t) e^{-j 2\pi f t} \, dt
  \]
- Plot the magnitude \( |X(f)| \) and phase \( \angle X(f) \) spectra.
- Interpret the results in terms of frequency content and phase behavior.

---

## ⚙️ MATLAB Implementation 

The MATLAB part of this exercise computes the **discrete Fourier series coefficients** of a periodic signal using **numerical integration**.

### 🔹 Main Script: `Illustrative_Problem_1_2.m`

This script is the main driver that:
- Defines the function name (in this case, `lambda`).
- Specifies the interval \([a, b]\) of one period.
- Chooses the number of coefficients \( n \) to compute.
- Calls the helper function `fseries` to evaluate the Fourier series coefficients.
- Plots the **discrete magnitude** and **phase spectra**.

**Conceptually:**  
It builds the two spectra:
\[
|a_k| \quad \text{and} \quad \angle a_k, \quad k = -n, \ldots, n
\]
representing the amplitude and phase contribution of each harmonic frequency component.

---

### 🔹 Function `fseries.m`

This function performs the **numerical integration** required to calculate the Fourier coefficients.

Mathematically, for each coefficient \( a_k \):

\[
a_k = \frac{1}{T} \int_{a}^{b} f(t) e^{-j 2\pi k t / T} \, dt
\]

Here, \( T = b - a \) is the period of the signal.

The script:
1. Computes \( a_0 \) directly (the DC component).
2. Loops for \( k = 1, 2, ..., n \) and uses another helper function (`exp_fnct`) to compute each \( a_k \) by multiplying the signal by \( e^{-j2\pi k t / T} \).
3. Uses MATLAB’s `quad` function for **numerical integration** with tolerance `tol`.

This approach builds the discrete spectrum coefficients from scratch.

---

### 🔹 Function `exp_fnct.m`

This helper function evaluates:
\[
f(t) \cdot e^{-j 2\pi k t / T}
\]
It is used inside the numerical integration process to compute the integrand for each \( a_k \).

Conceptually, it represents the **projection of the signal** onto a complex exponential of frequency \( k/T \).

---

### 🔹 Function `lambda.m`

This defines the **time-domain signal** \( \lambda(t) \), which is a **triangular waveform** defined as:

\[
\lambda(t) =
\begin{cases}
x + 1, & -1 < x < 0 \\
1, & x = 0 \\
-x + 1, & 0 < x < 1 \\
0, & \text{otherwise}
\end{cases}
\]

This signal is symmetric and continuous, so its Fourier series contains only **cosine (even)** terms, and its **phase spectrum** is expected to show symmetry around zero.

---

## 📊 Results from MATLAB

- **Magnitude Spectrum:**  
  The discrete spikes correspond to the amplitudes of each harmonic component.  
  As expected for a triangular waveform, the magnitudes decrease rapidly with frequency (proportional to \( 1/k^2 \)).

- **Phase Spectrum:**  
  Due to signal symmetry, the phase is approximately **0 or π**, alternating for successive harmonics.  
  Some numerical noise may appear due to finite integration accuracy.

---

## 🐍 Python Implementation

The Python version uses the **Fast Fourier Transform (FFT)** to compute the spectrum numerically and visualize it continuously.

### 🔹 Steps

1. Define the custom signal \( x(t) \) (piecewise waveform with triangular and constant segments).  
2. Sample it densely (e.g., 2000 samples from -5 to 5).  
3. Apply the **FFT** to compute its frequency-domain representation:
   \[
   X(f) = \mathcal{F}\{x(t)\}
   \]
4. Use `fftshift()` to center zero frequency.
5. Compute the **normalized magnitude** and **phase** spectra.
6. Plot:
   - \( x(t) \): Time-domain signal
   - \( |X(f)| \): Magnitude spectrum
   - \( \angle X(f) \): Phase spectrum

---

## 📈 Results and Discussion (Python)

- The **time-domain plot** clearly shows the triangular/plateau structure of \( x(t) \).
- The **magnitude spectrum** shows a smooth envelope that decays with frequency, consistent with the theory that smoother signals have faster spectral decay.
- The **phase spectrum** appears as a **sawtooth pattern**, which is a normal behavior of the FFT representation when the signal is not perfectly even or when it includes abrupt changes (discontinuities or asymmetries).

This effect occurs because the phase wraps around \( -\pi \) to \( +\pi \), producing a periodic "jump" in the phase plot.  
Such discontinuities can be unwrapped (using `np.unwrap`) to show a smoother phase curve if desired.

---

## 🔬 Mathematical Summary

For a periodic signal \( f(t) \) with period \( T \):

\[
a_k = \frac{1}{T} \int_{T} f(t) e^{-j 2\pi k t / T} \, dt
\]

and the reconstructed signal is:

\[
f(t) = \sum_{k=-\infty}^{\infty} a_k e^{j 2\pi k t / T}
\]

In practice:
- MATLAB numerically computes \( a_k \) coefficients and plots them as discrete points.
- Python approximates the **continuous Fourier Transform** via FFT, giving smooth, high-resolution spectra.

---

## 📚 Conclusions

- Both MATLAB and Python correctly represent the **frequency-domain structure** of the signal.  
- The **MATLAB code** emphasizes the **Fourier series** perspective (discrete harmonics).  
- The **Python FFT** version shows the **Fourier transform** perspective (continuous spectrum).  
- The **magnitude** confirms harmonic decay consistent with a triangular waveform (\( \propto 1/k^2 \)).  
- The **phase** confirms signal symmetry and shows expected π shifts.

---

## 🧾 References

- Oppenheim, A. V., & Willsky, A. S. *Signals and Systems*, Prentice Hall.  
- Bracewell, R. *The Fourier Transform and Its Applications*, McGraw-Hill.  
- MATLAB Documentation: `quad`, `fft`, `angle`, `abs`  
- NumPy & Matplotlib Libraries for FFT visualization
