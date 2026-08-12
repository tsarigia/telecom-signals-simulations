import matplotlib.pyplot as plt
import numpy as np

# 1. Παράμετροι Συστήματος 

f_GHz = 28 # Συχνότητα λειτουργίας σε GHz
Pt_gNB = 40  # Ισχύς εκπομπής gNB σε dBm
Gt_gNB = 24 # Κέρδος κεραίας gNB σε dBi
Gr_UE = 10 # Κέρδος κεραίας UE σε dBi
Lc = 1   # Απώλειες καλωδίων σε dB
N_UE = -80.98 # Ισχύς θορύβου στο UE σε dBm (Υπολογίστηκε στο Ερ. 3)

# Εκθέτες Απώλειας Διαδρομής (PLE) για UMi
n_LOS = 2.1
n_NLOS = 3.19

# Συστοιχία αποστάσεων: από 10m έως 500m
d = np.linspace(10, 500, 500)


# 2. Βασικές Συναρτήσεις Υπολογισμού

def calc_fspl(f_ghz, d0=1):
    """Υπολογισμός Απώλειας Ελεύθερου Χώρου στην απόσταση αναφοράς d0."""
    return 32.4 + 20 * np.log10(f_ghz) + 20 * np.log10(d0)

def calc_pl(f_ghz, distance, n):
    """Υπολογισμός Συνολικής Απώλειας Διαδρομής (CI Model)."""
    fspl_1m = calc_fspl(f_ghz)
    return fspl_1m + 10 * n * np.log10(distance)


# 3. Υπολογισμοί Δεδομένων για τα Διαγράμματα

#Διάγραμμα 1: Path Loss vs Απόσταση
PL_LOS = calc_pl(f_GHz, d, n_LOS)
PL_NLOS = calc_pl(f_GHz, d, n_NLOS)

#Διάγραμμα 2: Ισχύς Λήψης στο UE vs Απόσταση 
# Pr = Pt + Gt + Gr - Lc - PL
Constant_Link_Budget = Pt_gNB + Gt_gNB + Gr_UE - Lc  # = 73 dBm
Pr_LOS = Constant_Link_Budget - PL_LOS
Pr_NLOS = Constant_Link_Budget - PL_NLOS

#Διάγραμμα 3: SNR στο UE vs Απόσταση 
# SNR = Pr - N
SNR_LOS = Pr_LOS - N_UE
SNR_NLOS = Pr_NLOS - N_UE

#Διάγραμμα 4: Σύγκριση συχνοτήτων (Για NLOS συνθήκες)
PL_3_5GHz = calc_pl(3.5, d, n_NLOS)
PL_28GHz = calc_pl(28, d, n_NLOS)
PL_39GHz = calc_pl(39, d, n_NLOS)



# 4. Σχεδίαση Διαγραμμάτων (Plotting)

plt.figure(figsize=(14, 10))
plt.suptitle('Ανάλυση Επίδοσης Ζεύξης 5G (Downlink) - Μοντέλο CI', fontsize=16, fontweight='bold')

#Plot 1 
plt.subplot(2, 2, 1)
plt.plot(d, PL_LOS, label='LOS (n=2.1)', color='blue', linewidth=2)
plt.plot(d, PL_NLOS, label='NLOS (n=3.19)', color='red', linewidth=2, linestyle='--')
plt.title('Απώλεια Διαδρομής (Path Loss) vs Απόσταση')
plt.xlabel('Απόσταση (m)')
plt.ylabel('Path Loss (dB)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

#Plot 2 
plt.subplot(2, 2, 2)
plt.plot(d, Pr_LOS, label='LOS', color='blue', linewidth=2)
plt.plot(d, Pr_NLOS, label='NLOS', color='red', linewidth=2, linestyle='--')
plt.axhline(-80.98, color='black', linestyle=':', label='Noise Floor (-80.98 dBm)')
plt.title('Ισχύς Λήψης (Pr) στο UE vs Απόσταση')
plt.xlabel('Απόσταση (m)')
plt.ylabel('Ισχύς Λήψης (dBm)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

#Plot 3
plt.subplot(2, 2, 3)
plt.plot(d, SNR_LOS, label='LOS', color='blue', linewidth=2)
plt.plot(d, SNR_NLOS, label='NLOS', color='red', linewidth=2, linestyle='--')
plt.axhline(0, color='black', linewidth=1) # Γραμμή μηδενός
plt.title('SNR στο UE vs Απόσταση')
plt.xlabel('Απόσταση (m)')
plt.ylabel('SNR (dB)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# Plot 4
plt.subplot(2, 2, 4)
plt.plot(d, PL_3_5GHz, label='3.5 GHz (Sub-6GHz)', color='green', linewidth=2)
plt.plot(d, PL_28GHz, label='28 GHz (mmWave)', color='orange', linewidth=2)
plt.plot(d, PL_39GHz, label='39 GHz (mmWave)', color='purple', linewidth=2)
plt.title('Σύγκριση Συχνοτήτων (PL σε συνθήκες NLOS)')
plt.xlabel('Απόσταση (m)')
plt.ylabel('Path Loss (dB)')
plt.grid(True, linestyle=':', alpha=0.7)
plt.legend()

# Προσαρμογή του layout 
plt.tight_layout()
plt.subplots_adjust(top=0.92) # Αφήνουμε χώρο για τον κεντρικό τίτλο

plt.show()