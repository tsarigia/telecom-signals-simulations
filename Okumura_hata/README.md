# Okumura-Hata Propagation Model

This repository contains the theoretical background, detailed step-by-step mathematical solutions, and a Python simulation for the **Okumura-Hata** empirical propagation model, widely used for predicting path loss in cellular mobile communications.

## 1. Theoretical Background & Equations

The Okumura-Hata model is an empirical formulation of the graphical path loss data provided by Okumura, valid for frequencies in the VHF and UHF bands. The core of the model calculates the path loss for an **Urban area**, and correction factors are applied for other environments.

### A. Urban Area
The basic equation for the median path loss in urban areas is given by:
$$L_{urban}(dB) = 69.55 + 26.16\log_{10}(f) - 13.82\log_{10}(h_b) - a(h_m) + (44.9 - 6.55\log_{10}(h_b))\log_{10}(d)$$

Where:
*   **$f$**: Operating frequency in MHz
*   **$h_b$**: Base station antenna height in meters (m)
*   **$h_m$**: Mobile antenna height in meters (m)
*   **$d$**: Transmitter-receiver distance in kilometers (km)
*   **$a(h_m)$**: Correction factor for the mobile antenna height.

For a **small or medium-sized city**, the correction factor is calculated as:
$$a(h_m) = (1.1\log_{10}(f) - 0.7)h_m - (1.56\log_{10}(f) - 0.8)$$

### B. Suburban Area
To find the path loss in a suburban environment, the urban path loss is modified as follows:
$$L_{suburban} = L_{urban} - 2\left(\log_{10}\left(\frac{f}{28}\right)\right)^2 - 5.4$$

### C. Open / Rural Area
For an open or rural area, the modification is:
$$L_{open} = L_{urban} - 4.78(\log_{10} f)^2 + 18.33\log_{10}(f) - 40.94$$

---

## 2. System Parameters (Case Study)

The analytical calculations and Python simulation are based on the following network parameters:
*   **Operating Frequency ($f$)**: 900 MHz
*   **Distance ($d$)**: 4 km
*   **Base Station Tx Power ($P_{t,base}$)**: 46 dBm
*   **Mobile Station Tx Power ($P_{t,mobile}$)**: 24 dBm
*   **Base Station Height ($h_b$)**: 50 m
*   **Mobile Height ($h_m$)**: 1.5 m
*   **Base Station Antenna Gain ($G_t$)**: 16 dBi
*   **Mobile Antenna Gain ($G_r$)**: 8 dBi
*   **Total Cable Losses ($L_c$)**: 0.5 dB
*   **Mobile Receiver Sensitivity**: -100 dBm

---

## 3. Step-by-Step Analytical Solutions

### Question 1: Correction Factor $a(h_m)$
Using the formula for a small/medium city with $f = 900\text{ MHz}$ and $h_m = 1.5\text{ m}$:
$$a(1.5) = (1.1\log_{10}(900) - 0.7)(1.5) - (1.56\log_{10}(900) - 0.8)$$
$$a(1.5) = (1.1 \times 2.954 - 0.7)(1.5) - (1.56 \times 2.954 - 0.8)$$
$$a(1.5) = (3.249 - 0.7)(1.5) - (4.608 - 0.8) = 3.824 - 3.808 = \mathbf{0.016 \text{ dB}}$$

### Question 2: Path Loss for the Three Environments ($d = 4\text{ km}$)
First, we calculate the constant terms for the Urban Path Loss equation:
*   $69.55 + 26.16\log_{10}(900) - 13.82\log_{10}(50) - a(1.5)$
*   $69.55 + 77.283 - 23.48 - 0.016 = 123.337$
*   Distance term: $(44.9 - 6.55\log_{10}(50))\log_{10}(4) = (44.9 - 11.128)(0.602) = (33.772)(0.602) = 20.332$

**1. Urban Path Loss:**
$$L_{urban} = 123.337 + 20.332 = \mathbf{143.67 \text{ dB}}$$

**2. Suburban Path Loss:**
$$L_{suburban} = 143.67 - 2(\log_{10}(900 / 28))^2 - 5.4 = 143.67 - 4.542 - 5.4 = \mathbf{133.73 \text{ dB}}$$

**3. Open/Rural Path Loss:**
$$L_{open} = 143.67 - 4.78(\log_{10}900)^2 + 18.33\log_{10}(900) - 40.94$$
$$L_{open} = 143.67 - 41.717 + 54.151 - 40.94 = \mathbf{115.16 \text{ dB}}$$

### Question 3: Received Signal Power
We calculate the received power using the full Link Budget: $P_r = P_t + G_t + G_r - L_c - PL$

**A. Downlink (Signal reaching the Mobile):**
*   Total System Gain ($P_{t,base} + G_t + G_r - L_c$) = $46 + 16 + 8 - 0.5 = 69.5\text{ dBm}$
*   **Urban**: $P_{r} = 69.5 - 143.67 =$ **$-74.17 \text{ dBm}$**
*   **Suburban**: $P_{r} = 69.5 - 133.73 =$ **$-64.23 \text{ dBm}$**
*   **Open**: $P_{r} = 69.5 - 115.16 =$ **$-45.66 \text{ dBm}$**

**B. Uplink (Signal reaching the Base Station):**
*   Total System Gain ($P_{t,mobile} + G_t + G_r - L_c$) = $24 + 16 + 8 - 0.5 = 47.5\text{ dBm}$
*   **Urban**: $P_{r} = 47.5 - 143.67 =$ **$-96.17 \text{ dBm}$**
*   **Suburban**: $P_{r} = 47.5 - 133.73 =$ **$-86.23 \text{ dBm}$**
*   **Open**: $P_{r} = 47.5 - 115.16 =$ **$-67.66 \text{ dBm}$**

### Question 5: Maximum Coverage Distance (Sensitivity = -100 dBm)
To find the maximum distance, the received signal must equal the receiver sensitivity (-100 dBm). 
From Downlink: $P_{t,base} + G_t + G_r - L_c - PL_{max} = -100 \implies PL_{max} = 169.5\text{ dB}$

Using the equation $PL = C + 33.772\log_{10}(d)$, we solve for $d$:
*   **Urban ($C=123.337$)**: $33.772\log_{10}(d) = 169.5 - 123.337 \implies d = 10^{1.366} =$ **$23.27 \text{ km}$**
*   **Suburban ($C=113.395$)**: $33.772\log_{10}(d) = 169.5 - 113.395 \implies d = 10^{1.661} =$ **$45.84 \text{ km}$**
*   **Open ($C=94.831$)**: $33.772\log_{10}(d) = 169.5 - 94.831 \implies d = 10^{2.211} =$ **$162.55 \text{ km}$**

**What changes if Antenna Gains and Cable Losses are zero ($G_t=0, G_r=0, L_c=0$)?**
The new maximum allowable Path Loss drops dramatically to: $PL_{max} = 46 + 0 + 0 - 0 + 100 = 146\text{ dB}$.
Solving for $d$ again with the new $PL_{max}$:
*   **Urban**: $33.772\log_{10}(d) = 146 - 123.337 \implies d = 10^{0.671} =$ **$4.69 \text{ km}$**
*   **Suburban**: $33.772\log_{10}(d) = 146 - 113.395 \implies d = 10^{0.965} =$ **$9.23 \text{ km}$**
*   **Open**: $33.772\log_{10}(d) = 146 - 94.831 \implies d = 10^{1.515} =$ **$32.74 \text{ km}$**

**Conclusion:** Removing the antenna gains shrinks the coverage area by nearly 80%.

---

## 4. Python Simulation
This repository includes a Python script (`okumura_hata_simulation.py`) that calculates and plots the Path Loss and the Received Power vs. Distance (from 1 km to 35 km) for the three environments, assuming $G_t=0, G_r=0, L_c=0$ as per the problem instructions.