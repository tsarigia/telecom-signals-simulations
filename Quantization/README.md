# Uniform Quantization Analysis & SQNR Evaluation (Triangular Waveform)

This repository contains theoretical analysis, mathematical derivation, and computational implementation (in **Python** and **MATLAB**). It evaluates a uniform quantizer applied to a periodic triangular baseband signal across multiple quantization levels ($M \in \{8, 16, 32, 64, 128\}$).

The project plots the quantizer input-output transfer characteristics, analyzes time-domain quantization error waveforms $e(t)$, and proves both analytically and experimentally the **$6.02\text{ dB/bit}$** Signal-to-Quantization-Noise Ratio (SQNR) scaling law.

---

## Table of Contents
1. [Theoretical Background & Analytical Derivations](#1-theoretical-background--analytical-derivations)
2. [Step-by-Step Analytical Results ($M = 8 \to 128$)](#2-step-by-step-analytical-results-m--8-\to-128)

---

## 1. Theoretical Background & Analytical Derivations

### 1.1 Periodic Signal Definition $x(t)$
The input signal $x(t)$ is a periodic triangular wave with fundamental period $T = 2\text{ s}$, defined over one period $t \in [0, 2)$ as:

$$
x(t) = 
\begin{cases} 
t, & 0 \le t < 1 \\ 
-t + 2, & 1 \le t < 2 
\end{cases}
$$

* **Dynamic Range:** The minimum amplitude is $X_{\min} = 0.0\text{ V}$ and the maximum amplitude is $X_{\max} = 1.0\text{ V}$. Therefore, the peak-to-peak dynamic range is:
  $$A = X_{\max} - X_{\min} = 1.0\text{ V}$$

### 1.2 Theoretical Signal Power ($P_x$)
The total average normalized power $P_x$ of the periodic triangular wave over one period $T = 2\text{ s}$ is computed via integration:

$$
P_x = \frac{1}{T} \int_{0}^{T} x^2(t) \, dt = \frac{1}{2} \left( \int_{0}^{1} t^2 \, dt + \int_{1}^{2} (-t + 2)^2 \, dt \right)
$$

By symmetry, both halves of the period contribute equally:

$$
P_x = \int_{0}^{1} t^2 \, dt = \left[ \frac{t^3}{3} \right]_{0}^{1} = \frac{1}{3} \approx 0.33333\text{ W}
$$

### 1.3 Uniform Quantizer Step Size ($\Delta$) & Noise Power ($P_e$)
For an $M$-level uniform quantizer dividing the range $[0, 1]$ into equal intervals, the step size $\Delta$ is:

$$
\Delta = \frac{X_{\max} - X_{\min}}{M} = \frac{1}{M}
$$

Assuming the quantization error $e(t) = x(t) - x_q(t)$ is uniformly distributed across the interval $[-\frac{\Delta}{2}, \frac{\Delta}{2}]$, the theoretical quantization noise power $P_e$ is:

$$
P_e = \frac{1}{\Delta} \int_{-\Delta/2}^{\Delta/2} e^2 \, de = \frac{\Delta^2}{12} = \frac{1}{12 M^2}
$$

### 1.4 Theoretical SQNR Formula (in dB)
The Signal-to-Quantization-Noise Ratio (SQNR) is the ratio of average signal power to average quantization noise power:

$$
\text{SQNR} = \frac{P_x}{P_e} = \frac{1/3}{1 / (12 M^2)} = 4 M^2
$$

Expressing this ratio in decibels ($\text{dB}$) as a function of the number of levels $M$ (or bits $R = \log_2 M$):

$$
\text{SQNR}_{\text{dB}} = 10 \log_{10}(4 M^2) = 10 \log_{10}(4) + 20 \log_{10}(M) \approx \mathbf{6.02 + 20 \log_{10}(M)}
$$

In terms of bit resolution $R$:

$$
\text{SQNR}_{\text{dB}} \approx 6.02 + 6.02 R \text{ dB}
$$

---

## 2. Step-by-Step Analytical Results ($M = 8 \to 128$)

The table below summarizes the step size $\Delta$, bit depth $R$, theoretical SQNR, and expected simulation results across all evaluated quantization levels:

| Quantization Levels ($M$) | Bits ($R = \log_2 M$) | Step Size ($\Delta = 1/M$) | Theoretical SQNR ($\text{dB}$) | Expected Simulation SQNR ($\text{dB}$) |
| :---: | :---: | :---: | :---: | :---: |
| **$M = 8$** | 3 bits | $0.12500\text{ V}$ | **$24.08\text{ dB}$** | **$24.08\text{ dB}$** |
| **$M = 16$** | 4 bits | $0.06250\text{ V}$ | **$30.10\text{ dB}$** | **$30.10\text{ dB}$** |
| **$M = 32$** | 5 bits | $0.03125\text{ V}$ | **$36.12\text{ dB}$** | **$36.12\text{ dB}$** |
| **$M = 64$** | 6 bits | $0.01562\text{ V}$ | **$42.14\text{ dB}$** | **$42.14\text{ dB}$** |
| **$M = 128$** | 7 bits | $0.00781\text{ V}$ | **$48.16\text{ dB}$** | **$48.16\text{ dB}$** |

* Every time the number of quantization levels doubles (+1 bit of resolution), the SQNR improves by exactly **$6.02\text{ dB}$**.*

---