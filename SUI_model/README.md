# Stanford University Interim (SUI) Propagation Model

This repository contains the theoretical background, step-by-step mathematical solutions, and a Python simulation for the **Stanford University Interim (SUI)** propagation model.

## 1. Theoretical Background & Equations

Developed by Stanford University for the IEEE 802.16 standard, the SUI model is used to predict path loss for frequencies above 1900 MHz in three distinct environments[cite: 1]:

*   **Type A (Urban):** Hilly terrain with moderate to heavy tree density. Associated with maximum path loss[cite: 1].
*   **Type B (Suburban):** Mostly flat terrains with moderate to heavy tree density, or hilly terrains with light tree density[cite: 1].
*   **Type C (Rural):** Flat terrain with light tree density. Associated with minimum path loss[cite: 1].

The basic equation for predicting Path Loss ($PL$) for distances $d > d_0$ is[cite: 1]:
$$PL = A + 10\gamma \log_{10}\left(\frac{d}{d_0}\right) + X_f + X_h + s$$

**Key Components:**
*   **$A$**: Free space path loss at the reference distance $d_0 = 100\text{ m}$[cite: 1].
    $$A = 20\log_{10}\left(\frac{4\pi d_0}{\lambda}\right)$$
*   **$\gamma$**: Path loss exponent, dependent on the base station height ($h_b$)[cite: 1]:
    $$\gamma = a - b \cdot h_b + \frac{c}{h_b}$$
    *(Parameters $a, b, c$ are terrain-specific constants)*[cite: 1].
*   **$X_f$**: Frequency correction factor for $f > 1900\text{ MHz}$[cite: 1].
    $$X_f = 6.0\log_{10}\left(\frac{f}{2000}\right)$$
*   **$X_h$**: Receiver antenna height ($h_r$) correction factor.
    *   Type A & B: $X_h = -10.8\log_{10}\left(\frac{h_r}{2}\right)$
    *   Type C: $X_h = -20.0\log_{10}\left(\frac{h_r}{2}\right)$
*   **$s$**: Shadowing effect parameter.
    $$s = 0.65(\log_{10} f)^2 - 1.3\log_{10}(f) + \alpha$$
    *($\alpha = 5.2\text{ dB}$ for Urban/Suburban, $\alpha = 6.6\text{ dB}$ for Rural)*.

---

## 2. System Parameters (Case Study)

The analytical calculations and Python simulation are based on the following network parameters:
*   **Operating Frequency ($f$)**: 1900 MHz
*   **Distance ($d$)**: 5 km (5000 m)
*   **Base Station Tx Power ($P_{t,base}$)**: 35 dBm
*   **Mobile Station Tx Power ($P_{t,mobile}$)**: 20 dBm
*   **Base Station Heights ($h_b$)**: 30 m and 80 m
*   **Receiver Height ($h_r$)**: 3 m
*   **Antenna Gains**: Isotropic ($0\text{ dBi}$)

---

## 3. Step-by-Step Analytical Solutions

### Initial Constant Calculations
1. **Wavelength ($\lambda$)**: $c / f = 3 \times 10^8 / 1900 \times 10^6 = \mathbf{0.1579\text{ m}}$
2. **Reference Loss ($A$)**: $20\log_{10}\left(\frac{4\pi \cdot 100}{0.1579}\right) = \mathbf{78.017\text{ dB}}$[cite: 1]
3. **Distance Factor**: $10\log_{10}(5000 / 100) = \mathbf{16.99\text{ dB}}$[cite: 1]
4. **Freq. Correction ($X_f$)**: $6.0\log_{10}(1900 / 2000) = \mathbf{-0.134\text{ dB}}$[cite: 1]
5. **Height Correction ($X_h$)**: 
   * Types A & B: $-10.8\log_{10}(3 / 2) = \mathbf{-1.902\text{ dB}}$
   * Type C: $-20.0\log_{10}(3 / 2) = \mathbf{-3.522\text{ dB}}$
6. **Shadowing ($s$)**:
   * Types A & B ($\alpha = 5.2$): $\mathbf{7.925\text{ dB}}$
   * Type C ($\alpha = 6.6$): $\mathbf{9.325\text{ dB}}$

---

### Question 1: Path Loss Calculation for 3 Environments & 2 Heights

**Case 1: Base Station Height $h_b = 30\text{ m}$**
*   **Urban (Type A)**: $\gamma = 4.795 \implies PL_{A,30} = \mathbf{165.37\text{ dB}}$
*   **Suburban (Type B)**: $\gamma = 4.375 \implies PL_{B,30} = \mathbf{158.24\text{ dB}}$
*   **Rural (Type C)**: $\gamma = 4.117 \implies PL_{C,30} = \mathbf{153.63\text{ dB}}$

**Case 2: Base Station Height $h_b = 80\text{ m}$**
*   **Urban (Type A)**: $\gamma = 4.157 \implies PL_{A,80} = \mathbf{154.54\text{ dB}}$
*   **Suburban (Type B)**: $\gamma = 3.694 \implies PL_{B,80} = \mathbf{146.66\text{ dB}}$
*   **Rural (Type C)**: $\gamma = 3.450 \implies PL_{C,80} = \mathbf{142.30\text{ dB}}$

**Observation on Base Station Height:**
Increasing the base station antenna height (from 30m to 80m) significantly *decreases* the path loss exponent ($\gamma$). As a result, the total path loss is reduced by approximately 10 to 11 dB. This confirms that taller antennas provide much better coverage, allowing the signal to travel further with less attenuation.

### Question 2: Received Signal Power (Downlink)
The base station transmits at $P_{tx} = 35\text{ dBm}$. ($P_{rx} = P_{tx} - PL$)
*   **For $h_b = 30\text{ m}$**: Urban: **-130.37 dBm** | Suburban: **-123.24 dBm** | Rural: **-118.63 dBm**
*   **For $h_b = 80\text{ m}$**: Urban: **-119.54 dBm** | Suburban: **-111.66 dBm** | Rural: **-107.30 dBm**

### Question 3: Received Signal Power at Base Station (Uplink)
The mobile phone transmits at $P_{tx} = 20\text{ dBm}$.
*   **For $h_b = 30\text{ m}$**: Urban: **-145.37 dBm** | Suburban: **-138.24 dBm** | Rural: **-133.63 dBm**
*   **For $h_b = 80\text{ m}$**: Urban: **-134.54 dBm** | Suburban: **-126.66 dBm** | Rural: **-122.30 dBm**

---

## 4. Python Simulation
This repository includes a Python script (`sui_model_simulation.py`) that calculates and plots the Path Loss (dB) vs. Distance (km) for all three environments and both base station heights, for distances ranging from $0.02\text{ km}$ to $10\text{ km}$.