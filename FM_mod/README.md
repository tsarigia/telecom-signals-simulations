# Frequency Modulation (FM) & Spectral Analysis

This repository contains the theoretical analysis, mathematical derivation, and computational implementation (in **Python** and **MATLAB**) for **Frequency Modulation (FM)** of a piecewise linear baseband message signal. 

The project evaluates instantaneous frequency variations, computes the modulation index and Carson's bandwidth, and performs time-domain and frequency-domain (FFT) spectral analysis around a $1000\text{ Hz}$ carrier wave.

---

## Table of Contents
1. [Theoretical Background & Signal Definitions](#1-theoretical-background--signal-definitions)
2. [Step-by-Step Analytical Solutions (Tasks α – ε)](#2-step-by-step-analytical-solutions-tasks-α--ε)

---

## 1. Theoretical Background & Signal Definitions

### 1.1 Baseband Message Signal $m(t)$
The information signal $m(t)$ is defined as a continuous-time piecewise linear triangular pulse active within the time interval $[0, 2]$ seconds, with a constant DC baseline of $0.1\text{ V}$ elsewhere:

$$m(t) =  \begin{cases}  t, & 0 \le t < 1 \\  -t + 2, & 1 \le t < 2 \\  0.1, & \text{otherwise}  \end{cases}$$

* **Physical Characteristics:**
  * Minimum amplitude: $\min[m(t)] = 0.0\text{ V}$ (at $t = 0\text{ s}$ and $t = 2\text{ s}$).
  * Maximum amplitude: $\max[m(t)] = 1.0\text{ V}$ (at the peak $t = 1.0\text{ s}$).
  * Practical Baseband Bandwidth ($B_m$): Since the triangular pulse completes its cycle in $T_0 = 2\text{ s}$, its fundamental frequency is $f_0 = 0.5\text{ Hz}$. The significant baseband energy (first major lobe of the squared sinc spectrum) is bounded by **$B_m \approx 1.0\text{ Hz}$**.

### 1.2 Unmodulated Carrier Signal $c(t)$
A high-frequency sinusoidal carrier wave is defined with amplitude $A_c = 1\text{ V}$ and frequency $f_c = 1000\text{ Hz}$:

$$c(t) = A_c \cos(2\pi f_c t) = \cos(2000\pi t)$$

### 1.3 Frequency Modulated Signal $s_{\text{FM}}(t)$
In Frequency Modulation (FM), the instantaneous frequency $f_i(t)$ of the carrier varies linearly with the message signal $m(t)$ according to the frequency deviation constant $k_f = 25\text{ Hz/V}$:

$$f_i(t) = f_c + k_f m(t) = 1000 + 25 m(t)$$

The instantaneous phase $\theta_i(t)$ is the integral of the instantaneous frequency over time:

$$\theta_i(t) = 2\pi \int_{0}^{t} f_i(\tau) \, d\tau = 2\pi f_c t + 2\pi k_f \int_{0}^{t} m(\tau) \, d\tau$$

Thus, the transmitted FM waveform is expressed as:

$$s_{\text{FM}}(t) = A_c \cos\left( 2\pi f_c t + 2\pi k_f \int_{0}^{t} m(\tau) \, d\tau \right)$$

---

## 2. Step-by-Step Analytical Solutions (Tasks α – ε)

### Task α: Range of Instantaneous Frequency
The instantaneous frequency of the modulated signal is given by $f_i(t) = f_c + k_f m(t)$. Using the extreme values of the message signal $m(t) \in [0.0, 1.0]\text{ V}$:

* **Minimum Instantaneous Frequency ($f_{\min}$):**
  $$f_{\min} = f_c + k_f \cdot \min[m(t)] = 1000 + 25(0) = \mathbf{1000\text{ Hz}}$$

* **Maximum Instantaneous Frequency ($f_{\max}$):**
  $$f_{\max} = f_c + k_f \cdot \max[m(t)] = 1000 + 25(1) = \mathbf{1025\text{ Hz}}$$

* **Instantaneous Frequency Range:** **$[1000\text{ Hz}, \, 1025\text{ Hz}]$**

---

### Task ε: Modulation Index ($\beta$)
*(Note: Computed before Task β as it is required for bandwidth classification).*

1. **Peak Frequency Deviation ($\Delta f$):**
   $$\Delta f = k_f \cdot \max\vert{}m(t)\vert{} = 25\text{ Hz/V} \times 1.0\text{ V} = \mathbf{25\text{ Hz}}$$

2. **Modulation Index ($\beta$):**
   The modulation index is the ratio of peak frequency deviation to the baseband message bandwidth ($B_m \approx 1.0\text{ Hz}$):
   $$\beta = \frac{\Delta f}{B_m} = \frac{25\text{ Hz}}{1\text{ Hz}} = \mathbf{25}$$

* **Classification:** Since $\beta = 25 \gg 1$, this system is classified as **Wideband FM (WBFM)**.

---

### Task β: Bandwidth of Modulated Signal (Carson's Rule)
According to **Carson's Bandwidth Rule**, approximately $98\%$ of the total FM signal power is contained within a bandwidth $B_{\text{FM}}$ given by:

$$B_{\text{FM}} \approx 2(\Delta f + B_m) = 2(1 + \beta)B_m$$

Substituting our calculated values ($\Delta f = 25\text{ Hz}$ and $B_m = 1\text{ Hz}$):

$$B_{\text{FM}} \approx 2(25 + 1) = \mathbf{52\text{ Hz}}$$

* **Spectral Range:** The FM sidebands extend approximately $\pm 26\text{ Hz}$ around the carrier, occupying the frequency band **$[974\text{ Hz}, \, 1026\text{ Hz}]$**.

---

### Tasks γ & δ: Time-Domain Waveforms & Frequency-Domain Spectra
* **Task γ (Time Domain):** Plots $m(t)$, $c(t)$, and $s_{\text{FM}}(t)$ across time. Because $f_c = 1000\text{ Hz}$ oscillates rapidly, the frequency variations are visually confirmed by plotting instantaneous density or observing zoomed intervals.

* **Task δ (Frequency Domain):** Uses the Fast Fourier Transform (FFT) to confirm that:
  * $\vert{}M(f)\vert{}$ is centered at **$0\text{ Hz}$** with bandwidth $\sim 1\text{ Hz}$.
  * $\vert{}C(f)\vert{}$ is a single pure impulse at **$1000\text{ Hz}$**.
  * $\vert{}S_{\text{FM}}(f)\vert{}$ is centered at **$1000\text{ Hz}$** and spans approximately **$52\text{ Hz}$** wide, validating Carson's Rule.