import matplotlib.pyplot as plt
import numpy as np


def calc_sui_pathloss(d_km, f_mhz, h_b, h_r, terrain_type):
    
    # Distance in meters
    d_m = d_km * 1000
    
    # Constants
    c = 3 * (10**8)
    lambda_wave = c / (f_mhz * 10**6)
    d0 = 100
    
    # A factor
    A = 20 * np.log10((4 * np.pi * d0) / lambda_wave)
    
    # Frequency correction factor
    X_f = 6.0 * np.log10(f_mhz / 2000)
    
    # Terrain specific parameters [a, b, c, alpha]
    if terrain_type == 'A':
        a, b, c_param, alpha = 4.6, 0.0075, 12.6, 5.2
        X_h = -10.8 * np.log10(h_r / 2)
    elif terrain_type == 'B':
        a, b, c_param, alpha = 4.0, 0.0065, 17.1, 5.2
        X_h = -10.8 * np.log10(h_r / 2)
    elif terrain_type == 'C':
        a, b, c_param, alpha = 3.6, 0.0050, 20.0, 6.6
        X_h = -20.0 * np.log10(h_r / 2)
        
    # Path loss exponent gamma
    gamma = a - (b * h_b) + (c_param / h_b)
    
    # Shadowing parameter
    s = 0.65 * (np.log10(f_mhz)**2) - 1.3 * np.log10(f_mhz) + alpha
    
    # Avoid log of zero or negative distances (Model is theoretically for d > d0)
    # Using np.where to handle the array safely
    d_ratio = np.where(d_m > 0, d_m / d0, 1e-9)
    
    # Total Path Loss
    PL = A + 10 * gamma * np.log10(d_ratio) + X_f + X_h + s
    return PL

def main():
    # System Parameters
    f = 1900       # Frequency in MHz
    h_r = 3        # Receiver height in meters
    
    # Create distance array from 0.02 km to 10 km (step 0.02)
    # Note: SUI model is theoretically designed for d > 0.1 km (100m).
# Values between 0.02 and 0.1 are mathematically extrapolated.
    d = np.arange(0.02, 10.02, 0.02)
    
    # Calculate Path Loss for hb = 30m 
    hb_1 = 30
    PL_A_30 = calc_sui_pathloss(d, f, hb_1, h_r, 'A')
    PL_B_30 = calc_sui_pathloss(d, f, hb_1, h_r, 'B')
    PL_C_30 = calc_sui_pathloss(d, f, hb_1, h_r, 'C')

    # Calculate Path Loss for hb = 80m 
    hb_2 = 80
    PL_A_80 = calc_sui_pathloss(d, f, hb_2, h_r, 'A')
    PL_B_80 = calc_sui_pathloss(d, f, hb_2, h_r, 'B')
    PL_C_80 = calc_sui_pathloss(d, f, hb_2, h_r, 'C')

    # Plotting
    plt.figure(figsize=(12, 8))
    
    # Plot for hb = 30m (Solid lines)
    plt.plot(d, PL_A_30, label='Urban (Type A) - hb=30m', color='red', linestyle='-', linewidth=2)
    plt.plot(d, PL_B_30, label='Suburban (Type B) - hb=30m', color='orange', linestyle='-', linewidth=2)
    plt.plot(d, PL_C_30, label='Rural (Type C) - hb=30m', color='green', linestyle='-', linewidth=2)

    # Plot for hb = 80m (Dashed lines)
    plt.plot(d, PL_A_80, label='Urban (Type A) - hb=80m', color='darkred', linestyle='--', linewidth=2)
    plt.plot(d, PL_B_80, label='Suburban (Type B) - hb=80m', color='darkorange', linestyle='--', linewidth=2)
    plt.plot(d, PL_C_80, label='Rural (Type C) - hb=80m', color='darkgreen', linestyle='--', linewidth=2)

    # Formatting the plot
    plt.title('SUI Propagation Model: Path Loss vs Distance (f=1900 MHz)', fontsize=15, fontweight='bold')
    plt.xlabel('Distance d (km)', fontsize=13)
    plt.ylabel('Path Loss PL (dB)', fontsize=13)
    
    plt.grid(True, linestyle=':', alpha=0.7)
    plt.legend(fontsize=11, loc='lower right')
    plt.xlim(0, 10)
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()