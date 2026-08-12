import matplotlib.pyplot as plt
import numpy as np


def main():
    # System Parameters
    f = 900   # Operating Frequency in MHz
    hb = 50 # Base Station Height in m
    hm = 1.5    # Mobile Height in m
    Pt_base = 46   # Base station Tx power in dBm
    
    # As per Question 4 instructions: Gt=0, Gr=0, Lc=0
    Gt, Gr, Lc = 0, 0, 0

    # Distance array from 1 km to 35 km (step 0.5 km)
    # Using 35.5 to include the 35km mark
    d = np.arange(1.0, 35.5, 0.5)

    # Calculate a(hm) for small/medium city
    a_hm = (1.1 * np.log10(f) - 0.7) * hm - (1.56 * np.log10(f) - 0.8)

    # 2. Calculate Path Loss (PL)
     # Urban
    PL_urban = (69.55 + 26.16 * np.log10(f) - 13.82 * np.log10(hb) - a_hm 
                + (44.9 - 6.55 * np.log10(hb)) * np.log10(d))
    
    # Suburban
    PL_suburban = PL_urban - 2 * (np.log10(f / 28))**2 - 5.4
    
    # Open / Rural
    PL_open = PL_urban - 4.78 * (np.log10(f))**2 + 18.33 * np.log10(f) - 40.94

    #  Calculate Received Power (Downlink) 
    # Pr = Pt + Gt + Gr - Lc - PL
    Pr_urban = Pt_base + Gt + Gr - Lc - PL_urban
    Pr_suburban = Pt_base + Gt + Gr - Lc - PL_suburban
    Pr_open = Pt_base + Gt + Gr - Lc - PL_open

    # 4. Plotting 
    _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    # Plot 1: Path Loss vs Distance
    ax1.plot(d, PL_urban, label='Urban', color='red', linewidth=2)
    ax1.plot(d, PL_suburban, label='Suburban', color='orange', linewidth=2)
    ax1.plot(d, PL_open, label='Open / Rural', color='green', linewidth=2)
    
    ax1.set_title('Okumura-Hata: Path Loss vs Distance', fontsize=14)
    ax1.set_xlabel('Distance (km)', fontsize=12)
    ax1.set_ylabel('Path Loss (dB)', fontsize=12)
    ax1.grid(True, linestyle=':', alpha=0.7)
    ax1.legend(fontsize=11)
    ax1.set_xlim(1, 35)

    # Plot 2: Received Power vs Distance
    ax2.plot(d, Pr_urban, label='Urban', color='red', linewidth=2)
    ax2.plot(d, Pr_suburban, label='Suburban', color='orange', linewidth=2)
    ax2.plot(d, Pr_open, label='Open / Rural', color='green', linewidth=2)
    
    # Add sensitivity threshold line (-100 dBm)
    ax2.axhline(-100, color='black', linestyle='--', linewidth=1.5, label='Sensitivity (-100 dBm)')
    
    ax2.set_title('Okumura-Hata: Received Power vs Distance (Gt=0, Gr=0)', fontsize=14)
    ax2.set_xlabel('Distance (km)', fontsize=12)
    ax2.set_ylabel('Received Power (dBm)', fontsize=12)
    ax2.grid(True, linestyle=':', alpha=0.7)
    ax2.legend(fontsize=11)
    ax2.set_xlim(1, 35)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()