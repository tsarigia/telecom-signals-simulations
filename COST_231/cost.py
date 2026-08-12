import matplotlib.pyplot as plt
import numpy as np


def main():
    # --- System Parameters ---
    f = 1900    # Operating Frequency (MHz)
    h_base = 30  # Base Station Height (m)
    h_mobile = 3  # Mobile Station Height (m)
    h_roof = 15  # Average building roof height (m)
    w = 25   # Street width (m)
    b = 50   # Building separation distance (m)
    phi_urb = 30  # Street orientation angle - Urban (degrees)
    phi_sub = 25  # Street orientation angle - Suburban (degrees)

    # array of distances from 0.02 km to 10 km (step of 0.02 km)
    # We use 10.02 as the stop value so that 10.0 is included in the array
    d = np.arange(0.02, 10.02, 0.02) 

    #  1. Rural Environment Calculation (LOS)
    PL_rural = 42.6 + 26 * np.log10(d) + 20 * np.log10(f)

    # 2.  Calculations for Urban & Suburban (NLOS)
    # Free Space Loss (L_fs)
    L_fs = 32.4 + 20 * np.log10(d) + 20 * np.log10(f)

    # Roof-to-street Diffraction and Scatter Loss (L_rts)
    delta_h_mobile = h_roof - h_mobile
    L_rts_base = -16.9 - 10 * np.log10(w) + 10 * np.log10(f) + 20 * np.log10(delta_h_mobile)

    L_ori_urb = -10 + 0.35 * phi_urb
    L_ori_sub = -10 + 0.35 * phi_sub

    L_rts_urb = L_rts_base + L_ori_urb
    L_rts_sub = L_rts_base + L_ori_sub

    # Multi-screen Diffraction Loss (L_MSD)
    delta_h_base = h_base - h_roof

    # Since h_base (30) > h_roof (15), parameters ka and kd are constant:
    L_bsh = -18 * np.log10(1 + delta_h_base)
    k_a = 54
    k_d = 18

    # Parameter k_f depends on the city size
    k_f_urb = -4 + 1.5 * (f / 925 - 1)  # Metropolitan Center
    k_f_sub = -4 + 0.7 * (f / 925 - 1)  # Medium Sized City

    # Calculate L_MSD
    L_msd_urb = L_bsh + k_a + k_d * np.log10(d) + k_f_urb * np.log10(f) - 9 * np.log10(b)
    L_msd_sub = L_bsh + k_a + k_d * np.log10(d) + k_f_sub * np.log10(f) - 9 * np.log10(b)

    # --- 3. Total Path Loss Calculation (NLOS) ---
    PL_urb = L_fs + L_rts_urb + L_msd_urb
    PL_sub = L_fs + L_rts_sub + L_msd_sub

    # --- 4. Plotting the results ---
    plt.figure(figsize=(10, 6))
    
    plt.plot(d, PL_urb, label='Urban (NLOS)', color='red', linewidth=2)
    plt.plot(d, PL_sub, label='Suburban (NLOS)', color='orange', linewidth=2)
    plt.plot(d, PL_rural, label='Rural (LOS)', color='green', linestyle='--', linewidth=2)

    plt.title('COST-231 Walfisch-Ikegami Model: Path Loss (f=1900 MHz)', fontsize=14)
    plt.xlabel('Distance d (km)', fontsize=12)
    plt.ylabel('Path Loss PL (dB)', fontsize=12)
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=12)
    plt.xlim(0, 10)
    plt.tight_layout()
    
    # Show the plot
    plt.show()

if __name__ == "__main__":# here we call the main function to execute the path loss calculations and plotting
    main()