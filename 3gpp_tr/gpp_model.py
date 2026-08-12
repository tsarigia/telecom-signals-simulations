import matplotlib.pyplot as plt
import numpy as np


def main():
    # System Parameters
    f_c = 3.5   # Frequency in GHz
    h_UT = 1.5      # User Terminal height in m
    h_BS_UMa = 25  # Base Station height UMa
    h_BS_UMi = 10 # Base Station height UMi
    h_BS_RMa = 35  # Base Station height RMa
    h = 5  # Average building height RMa
    W = 20  # Average street width RMa

    # Distance array d_2D from 10 m to 2000 m with step 10 m
    # Using 2005 as stop to include 2000
    d_2D = np.arange(10, 2010, 10)

    # 1. Calculate 3D Distances
    d_3D_UMa = np.sqrt(d_2D**2 + (h_BS_UMa - h_UT)**2)
    d_3D_UMi = np.sqrt(d_2D**2 + (h_BS_UMi - h_UT)**2)
    d_3D_RMa = np.sqrt(d_2D**2 + (h_BS_RMa - h_UT)**2)

    # 2. Calculate Path Loss (NLOS) 
    
    # A. Urban Macrocell (UMa)
    term_hUT_UMa = 0.6 * (h_UT - 1.5) # This is 0 for h_UT = 1.5
    PL_UMa = 13.54 + 39.08 * np.log10(d_3D_UMa) + 20 * np.log10(f_c) - term_hUT_UMa

    # B. Urban Microcell (UMi)
    term_hUT_UMi = 0.3 * (h_UT - 1.5) # This is 0 for h_UT = 1.5
    PL_UMi = 35.3 * np.log10(d_3D_UMi) + 22.4 + 21.3 * np.log10(f_c) - term_hUT_UMi

    # C. Rural Macrocell (RMa)
    term_W = 7.1 * np.log10(W)
    term_h = 7.5 * np.log10(h)
    term_hBS1 = (24.37 - 3.7 * (h / h_BS_RMa)**2) * np.log10(h_BS_RMa)
    term_d3D = (43.42 - 3.1 * np.log10(h_BS_RMa)) * (np.log10(d_3D_RMa) - 3)
    term_fc = 20 * np.log10(f_c)
    term_hUT_RMa = 3.2 * (np.log10(11.75 * h_UT))**2 - 4.97

    PL_RMa = 161.04 - term_W + term_h - term_hBS1 + term_d3D + term_fc - term_hUT_RMa

    # 3. Plotting 
    plt.figure(figsize=(10, 6))

    plt.plot(d_2D, PL_UMa, label='Urban Macrocell (UMa)', color='red', linewidth=2)
    plt.plot(d_2D, PL_UMi, label='Urban Microcell (UMi)', color='orange', linewidth=2)
    plt.plot(d_2D, PL_RMa, label='Rural Macrocell (RMa)', color='green', linewidth=2)

    plt.title('3GPP TR 38.901 (NLOS): Path Loss vs Horizontal Distance', fontsize=14)
    plt.xlabel('Horizontal Distance $d_{2D}$ (m)', fontsize=12)
    plt.ylabel('Path Loss PL (dB)', fontsize=12)
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=12)
    plt.xlim(10, 2000)
    plt.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":
    main()