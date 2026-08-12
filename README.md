# Telecom Signals Simulations

This repository contains a codebase (MATLAB & Python) for various Telecommunications projects, ranging from signal fundamentals to advanced modulation techniques.

## 📑 Table of Contents:

### A. Analog Communications

1. [Amplitude Modulation (AM) Simulation with GUI (Python)](./amp_modu)  
  This exercise involves the development of a Python program with a **Graphical User Interface (GUI)** designed to simulate the fundamental processes of Amplitude Modulation (AM) and Demodulation.

2. [Double-Sideband Suppressed-Carrier (DSB-SC) Amplitude Modulation & Spectral Analysis](./DSB_sc)
   
   The project models a piecewise linear baseband message signal, performs time-domain modulation with a high-frequency carrier wave, calculates theoretical and numerical signal power, and evaluates the spectral behavior using Fast Fourier Transforms (FFT) both with and without Additive White Gaussian Noise (AWGN).

3. [Frequency Modulation (FM) & Spectral Analysis](./FM_mod)
   
   This file contains the theoretical analysis, mathematical derivation, and computational implementation for Frequency Modulation (FM) of a piecewise linear baseband message signal. 

### B. Signal Processing Fundamentals

4. [ Frequency Spectrum Analysis of a Signal](./freq_diag)  
   
   Analyze the frequency behavior of a time-domain signal \( x(t) \)
5. [Fourier Transform of a Rectangular Pulse](./fft_ex)
   
   This project demonstrates the Fourier Transform (FT) of a rectangular pulse both theoretically (using analytical derivation) and numerically (using the Fast Fourier Transform - FFT).

### C. Channel Modeling & Propagation

6. [COST-231 Walfisch-Ikegami](./COST_231)

   This repository contains the theoretical background, detailed step-by-step mathematical solutions, and analytical results for the COST-231 Walfisch-Ikegami empirical radio propagation model.

7. [Close-In (CI) Free Space Reference Distance empirical propagation model](./CI_model)
   
   This repository contains the theoretical background, detailed step-by-step mathematical solutions, and analytical results for the Close-In (CI) Free Space Reference Distance empirical propagation model, primarily used for 5G mmWave network planning.

8. [Stanford University Interim (SUI)](./SUI_model)
   
   This repository contains the theoretical background, step-by-step mathematical solutions, and a Python simulation for the Stanford University Interim (SUI) propagation model.

### D. Digital Communications

9. [ Non-Uniform Companding & PCM Quantization Analysis](./Quant_samp)

   The project implements custom non-linear companding functions (`alaw_pcm` and `invalaw`), evaluates the Signal-to-Quantization-Noise Ratio (SQNR in dB) across 256 quantization levels ($N = 256$, 8-bit resolution), and visualizes the quantization error waveforms for acoustic speech signals.

10. [Uniform Quantization Analysis & SQNR Evaluation](./Quantization)

   The project plots the quantizer input-output transfer characteristics, analyzes time-domain quantization error waveforms $e(t)$, and proves both analytically and experimentally the **$6.02\text{ dB/bit}$** Signal-to-Quantization-Noise Ratio (SQNR) scaling law.


## 🛠️ Prerequisites & Requirements

To run the projects in this repository, you will need the following tools and libraries:

**For Python Projects:**
* Python 3.13
* The required packages are listed in `requirements.txt`. You can install them by running:
  ```bash
  pip install -r requirements.txt
