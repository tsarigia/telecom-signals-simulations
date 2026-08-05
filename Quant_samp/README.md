# Non-Uniform Companding & PCM Quantization Analysis (A-Law, $\mu$-Law, DPCM & Uniform PCM)

This repository contains  theoretical foundations, mathematical derivations, and computational implementations (in **Python** and **MATLAB**). It explores Pulse Code Modulation (PCM) schemes, including **Uniform PCM**, **$\mu$-Law Companding**, **A-Law Companding**, and **Differential PCM (DPCM)**.

The project implements custom non-linear companding functions (`alaw_pcm` and `invalaw`), evaluates the Signal-to-Quantization-Noise Ratio (**SQNR** in dB) across 256 quantization levels ($N = 256$, 8-bit resolution), and visualizes the quantization error waveforms for acoustic speech signals.

---

## Table of Contents
1. [Theoretical Background & Companding Formulas](#1-theoretical-background--companding-formulas)
2. [Quantization Schemes & SQNR Definitions](#2-quantization-schemes--sqnr-definitions)
3. [Experimental Results & Telecommunication Analysis](#3-experimental-results--telecommunication-analysis)
---

## 1. Theoretical Background & Companding Formulas

In audio and speech processing, small-amplitude signals occur much more frequently than large-amplitude peaks. **Uniform quantization** applies constant step sizes across the entire dynamic range, yielding poor Signal-to-Quantization-Noise Ratios (SQNR) for low-level signals. **Companding** (Compressing + Expanding) applies a logarithmic non-linearity before uniform quantization, compressing large amplitudes and boosting quantization resolution for small amplitudes.

### 1.1 A-Law Compression & Inverse Expansion ($\alpha = 87.6$)
The standard European ITU-T G.711 **A-Law compression** function $F_A(x)$ maps an input signal $x \in [-1, 1]$ using parameter $\alpha$:

$$F_A(x) = \text{sgn}(x)  \begin{cases}  \frac{\alpha \vert{}x\vert{}}{1 + \ln(\alpha)}, & 0 \le \vert{}x\vert{} < \frac{1}{\alpha} \\  \frac{1 + \ln(\alpha \vert{}x\vert{})}{1 + \ln(\alpha)}, & \frac{1}{\alpha} \le \vert{}x\vert{} \le 1  \end{cases}$$

The **Inverse A-Law expansion** function $F_A^{-1}(y)$, implemented in `invalaw(y, alpha)`, reconstructs the normalized signal from compressed values $y \in [-1, 1]$:

$$F_A^{-1}(y) = \text{sgn}(y)  \begin{cases}  \frac{\vert{}y\vert{}(1 + \ln(\alpha))}{\alpha}, & 0 \le \vert{}y\vert{} < \frac{1}{1 + \ln(\alpha)} \\  \frac{e^{\vert{}y\vert{}(1 + \ln(\alpha)) - 1}}{\alpha}, & \frac{1}{1 + \ln(\alpha)} \le \vert{}y\vert{} \le 1  \end{cases}$$

### 1.2 $\mu$-Law Compression & Expansion ($\mu = 255$)
The North American ITU-T G.711 **$\mu$-Law compression** formula maps input $x \in [-1, 1]$ via a continuous logarithmic curve:

$$F_\mu(x) = \text{sgn}(x) \frac{\ln(1 + \mu \vert{}x\vert{})}{\ln(1 + \mu)}$$

Its corresponding inverse expansion is:

$$F_\mu^{-1}(y) = \text{sgn}(y) \frac{(1 + \mu)^{\vert{}y\vert{}} - 1}{\mu}$$

---

## 2. Quantization Schemes & SQNR Definitions

### 2.1 Signal-to-Quantization-Noise Ratio (SQNR)
For an original discrete-time sequence $x[n]$ and its reconstructed output $\hat{x}[n]$, the quantization error is $e[n] = x[n] - \hat{x}[n]$. The SQNR in decibels ($\text{dB}$) is defined as:

$$\text{SQNR}_{\text{dB}} = 10 \log_{10} \left( \frac{\sum_{n=0}^{L-1} \vert{}x[n]\vert{}^2}{\sum_{n=0}^{L-1} \vert{}e[n]\vert{}^2} \right)$$

### 2.2 Overview of the 4 Evaluated Schemes ($N = 256$ Levels)
* **a) Differential PCM (DPCM):** Exploits sample-to-sample correlation by predicting the next sample using a first-order predictor ($\hat{x}[n] = x[n-1]$) and quantizing the prediction error $d[n] = x[n] - \hat{x}[n]$.
* **b) $\mu$-Law PCM ($\mu = 255$):** Non-linear logarithmic compression with $\mu = 255$, followed by 8-bit ($N=256$) uniform quantization.
* **c) A-Law PCM ($\alpha = 87.6$):** ITU-T G.711 A-Law companding using custom functions `alaw_pcm` and `invalaw`.
* **d) Uniform PCM ($N = 256$):** Standard linear quantization dividing the dynamic range $[-1, 1]$ into 256 equal intervals ($\Delta = \frac{2}{256}$).

---

## 3. Experimental Results & Telecommunication Analysis

### 3.1 Laboratory SQNR Measurements (Acoustic Speech Signal)

```text

 SQNR COMPARISON (N = 256)       

 (a) Differential PCM (DPCM):        21.18 dB
 (b) mu-Law PCM (mu = 255):          32.05 dB
 (c) A-Law PCM (alpha = 87.6):       32.14 dB
 (d) Uniform PCM (N = 256):          28.46 dB
