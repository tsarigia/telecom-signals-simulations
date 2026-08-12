# 5G mmWave Close-In (CI) Propagation Model

This repository contains the theoretical background, detailed step-by-step mathematical solutions, and analytical results for the **Close-In (CI) Free Space Reference Distance** empirical propagation model, primarily used for 5G mmWave network planning.

## 1. Theoretical Background & Equations

The Close-In (CI) model is one of the most widely adopted propagation models for 5G networks, especially in the mmWave bands (FR2). Unlike purely empirical models that use abstract curve-fitting parameters, the CI model is anchored to a physical constant: the free-space path loss at a 1-meter reference distance. 

The total Path Loss ($PL$) is calculated using the following equation:
$$PL^{CI}(f, d)[dB] = FSPL(f, d_0) + 10n \log_{10}\left(\frac{d}{d_0}\right) + X_{\sigma}$$

1. **Free Space Path Loss at Reference Distance ($FSPL$):** 
   For 5G mmWave, the standardized reference distance is $d_0 = 1\text{ m}$. The $FSPL$ at 1 meter depends strictly on the operating frequency ($f$ in GHz):
   $$FSPL(f, 1\text{m}) = 32.4 + 20\log_{10}(f_{GHz})$$

2. **Path Loss Exponent ($n$ / PLE):** 
   Describes how fast the signal attenuates with distance depending on the environment (e.g., $n \approx 2.1$ for LOS and $n \approx 3.19$ for NLOS in Urban Microcells).

3. **Shadow Fading ($X_{\sigma}$):** 
   A zero-mean Gaussian random variable with standard deviation $\sigma$ (in dB), representing signal fluctuations due to obstacles. (For deterministic calculations, $X_{\sigma} = 0$).

4. **Receiver Thermal Noise ($N$):**
   Calculated based on the channel bandwidth ($B$ in Hz) and the receiver's Noise Figure ($NF$):
   $$N[\text{dBm}] = -174 + 10\log_{10}(B) + NF$$

5. **Link Budget & SNR:**
   The received power ($P_r$) and Signal-to-Noise Ratio ($SNR$) are calculated as:
   $$P_r = P_t + G_t + G_r - L_c - PL$$
   $$SNR = P_r - N$$

---

## 2. System Parameters (Case Study)

The calculations in this project are based on an Urban Microcell (UMi) scenario operating at 28 GHz:
* **Operating Frequency ($f$)**: 28 GHz
* **Reference Distance ($d_0$)**: 1 m
* **Study Distance ($d$)**: 150 m
* **Channel Bandwidth ($B$)**: 400 MHz
* **gNB (Base Station) Tx Power ($P_{t,gNB}$)**: 40 dBm
* **UE (Mobile) Tx Power ($P_{t,UE}$)**: 23 dBm
* **gNB Antenna Gain ($G_{gNB}$)**: 24 dBi
* **UE Antenna Gain ($G_{UE}$)**: 10 dBi
* **Cable Losses ($L_c$)**: 1 dB
* **gNB Noise Figure ($NF_{gNB}$)**: 5 dB
* **UE Noise Figure ($NF_{UE}$)**: 7 dB
* **UMi LOS Parameters**: $n = 2.1$, $\sigma = 4.0$ dB
* **UMi NLOS Parameters**: $n = 3.19$, $\sigma = 8.2$ dB

---

## 3. Step-by-Step Analytical Solutions

### Question 1: FSPL at Reference Distance
Using the simplified formula for $d_0 = 1\text{ m}$ and $f = 28\text{ GHz}$:
$$FSPL(28, 1) = 32.4 + 20\log_{10}(28) = 32.4 + 20(1.447) = \mathbf{61.34 \text{ dB}}$$

### Question 2: Path Loss at 150m (Deterministic, $X_{\sigma} = 0$)
Using the CI model equation: $PL = 61.34 + 10 \cdot n \cdot \log_{10}(150)$.
*(Note: $10\log_{10}(150) = 21.76$)*
* **LOS ($n=2.1$):** $PL_{LOS} = 61.34 + 2.1(21.76) = \mathbf{107.04 \text{ dB}}$
* **NLOS ($n=3.19$):** $PL_{NLOS} = 61.34 + 3.19(21.76) = \mathbf{130.75 \text{ dB}}$

### Question 3: Receiver Noise Power ($N$)
First, we calculate the thermal noise floor for a 400 MHz bandwidth:
$$-174 + 10\log_{10}(400 \times 10^6) = -174 + 86.02 = -87.98 \text{ dBm}$$
* **Noise at UE ($NF = 7\text{ dB}$):** $N_{UE} = -87.98 + 7 = \mathbf{-80.98 \text{ dBm}}$
* **Noise at gNB ($NF = 5\text{ dB}$):** $N_{gNB} = -87.98 + 5 = \mathbf{-82.98 \text{ dBm}}$

### Question 4: Received Signal Power & SNR

**A. Downlink (gNB $\rightarrow$ UE)**
Constant Link Budget = $40 + 24 + 10 - 1 = \mathbf{73 \text{ dBm}}$
* **LOS:** $P_r = 73 - 107.04 = \mathbf{-34.04 \text{ dBm}}$ | $SNR = -34.04 - (-80.98) = \mathbf{46.94 \text{ dB}}$
* **NLOS:** $P_r = 73 - 130.75 = \mathbf{-57.75 \text{ dBm}}$ | $SNR = -57.75 - (-80.98) = \mathbf{23.23 \text{ dB}}$

**B. Uplink (UE $\rightarrow$ gNB)**
Constant Link Budget = $23 + 10 + 24 - 1 = \mathbf{56 \text{ dBm}}$
* **LOS:** $P_r = 56 - 107.04 = \mathbf{-51.04 \text{ dBm}}$ | $SNR = -51.04 - (-82.98) = \mathbf{31.94 \text{ dB}}$
* **NLOS:** $P_r = 56 - 130.75 = \mathbf{-74.75 \text{ dBm}}$ | $SNR = -74.75 - (-82.98) = \mathbf{8.23 \text{ dB}}$

### Question 5: Maximum Coverage Distance Analysis
By rearranging the Link Budget and CI model equations, we calculated the maximum coverage distance ($d_{max}$) based on two criteria: Minimum Sensitivity ($P_{sens} = -90\text{ dBm}$) and Minimum SNR ($SNR_{min} = 10\text{ dB}$). 

The results highlight the critical necessity of beamforming (antenna gains) in mmWave networks:

| Direction & Criterion | Scenario | WITH Antenna Gains | WITHOUT Antenna Gains (0 dBi) |
| :--- | :--- | :--- | :--- |
| **Downlink** ($P_{sens}$) | LOS <br> NLOS | 69,335 m <br> 1,537.6 m | 1,666.9 m <br> 132.1 m |
| **Downlink** ($SNR \ge 10\text{ dB}$) | LOS <br> NLOS | 8,614.7 m <br> 389.6 m | 207.1 m <br> 33.5 m |
| **Uplink** ($P_{sens}$) | LOS <br> NLOS | 10,750.5 m <br> 450.7 m | 258.4 m <br> 38.7 m |
| **Uplink** ($SNR \ge 10\text{ dB}$) | LOS <br> **NLOS** | 1,663.2 m <br> **131.9 m** | 40.0 m <br> **11.3 m** |

**Conclusion:** The network design is bottlenecked by the **Uplink NLOS scenario requiring an adequate SNR**. Without directional antenna gains (beamforming), the coverage radius collapses to a mere 11 meters. With beamforming, the realistic maximum cell radius is approximately **132 meters**, which aligns perfectly with modern 5G Small Cell deployment strategies.