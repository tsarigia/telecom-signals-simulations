import numpy as np
import matplotlib.pyplot as plt

# --- 1. Ορισμός Παραμέτρων και Συναρτήσεων ---
A = 1.0  # Πλάτος
T = 2.0  # Διάρκεια
T_anal = T 

# Κανονικοποιημένη sinc: sinc(x) = sin(pi*x) / (pi*x)
def normalized_sinc(x):
    """sinc(x) = sin(pi*x) / (pi*x), χειρίζεται την περίπτωση x=0."""
    return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

# --- 2. FFT Υπολογισμοί ---
Fs = 100.0   
Ts = 1.0 / Fs
N_periods = 10 
N_samples = int(Fs * N_periods) 

t = np.linspace(-N_periods/2, N_periods/2, N_samples, endpoint=False)
x_t = np.where(np.abs(t) <= T / 2, A, 0.0)

X_fft = np.fft.fft(x_t)
f = np.fft.fftfreq(N_samples, d=Ts)
X_shifted = np.fft.fftshift(X_fft)
f_shifted = np.fft.fftshift(f)
X_fft_scaled = X_shifted / Fs

# Αναλυτική Λύση (με τη συνθήκη AT=1)
arg_sinc = f_shifted * T_anal
X_anal_AT1 = 1.0 * normalized_sinc(arg_sinc)


# --- 3. Δημιουργία Αναλυτικού Φάσματος Φάσης ---
phase_anal_book = np.zeros_like(f_shifted)
sinc_negative = X_anal_AT1 < 0

# Για f > 0: Αν X(f) < 0 (περιττοί λοβοί), τότε φάση = -π
phase_anal_book = np.where(
    (f_shifted > 0) & sinc_negative, 
    -np.pi, 
    phase_anal_book
)
# Για f < 0: Αν X(f) < 0 (περιττοί λοβοί), τότε φάση = +π
phase_anal_book = np.where(
    (f_shifted < 0) & sinc_negative, 
    np.pi, 
    phase_anal_book
)


# --- 4. Σχεδίαση των Διαγραμμάτων ---
plt.figure(figsize=(10, 12))

# 4.1. Ορθογώνιος Παλμός x(t) 
plt.subplot(3, 1, 1)
plt.plot(t, x_t, 'b-', linewidth=2)
plt.title(f'$\\mathbf{{(a)}}$ Ορθογώνιος Παλμός $x(t)$', fontsize=14, weight='bold')
plt.xlabel('$\\mathbf{t}$ (Χρονικός Άξονας)') 
plt.ylabel('$x(t)$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(-0.1, A + 0.1)
plt.xlim(-T - 1, T + 1)
plt.xticks([-T/2, T/2], ['-T/2', 'T/2'])


# --- ΔΗΜΙΟΥΡΓΙΑ ΣΗΜΑΝΣΗΣ f ΓΙΑ ΤΙΣ ΕΤΙΚΕΤΕΣ $\pm 1/T, \pm 2/T$ ---
xticks_values = np.array([-2/T, -1/T, 1/T, 2/T])
xticks_pos = xticks_values[np.abs(xticks_values) <= 5/T]
xticks_labels = ['-2/T', '-1/T', '1/T', '2/T']


# 4.2. Φάσμα Πλάτους $|X(f)|$ 
plt.subplot(3, 1, 2)
plt.plot(f_shifted, np.abs(X_anal_AT1), 'r-', label='Αναλυτική Λύση $|X(f)| = |\\mathrm{sinc}(fT)|$', linewidth=2)
# Επικάλυψη FFT (Normalized)
plt.plot(f_shifted, np.abs(X_fft_scaled * (1/ (A*T))), 'b.', markersize=4, alpha=0.5, label='FFT (Normalized)') 

plt.title('$\\mathbf{{(b)}}$ Φάσμα Πλάτους $|X(f)|$ (με $AT=1$)', fontsize=14, weight='bold')
plt.xlabel('$\\mathbf{f}$ (Άξονας Συχνότητας - Hz)') 
plt.ylabel('$|X(f)|$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(-5/T, 5/T)
plt.ylim(0, 1.1)

plt.xticks(xticks_pos, xticks_labels)
plt.axvline(x=0, color='gray', linestyle='-', linewidth=0.8)
plt.legend()


# 4.3. Φάσμα Φάσης $\theta(f)$ 
plt.subplot(3, 1, 3)
plt.step(f_shifted, phase_anal_book, 'g-', linewidth=2, label='Αναλυτική Φάση (Όπως στο Σχήμα 2.13γ)')
plt.plot(f_shifted, np.angle(X_anal_AT1), 'r--', linewidth=1, alpha=0.5, label='Τυπική Περιττή Φάση')

plt.title('$\\mathbf{{(\\gamma)}}$ Φάσμα Φάσης $\\theta(f)$', fontsize=14, weight='bold')
plt.xlabel('$\\mathbf{f}$ (Άξονας Συχνότητας - Hz)') 
plt.ylabel('$\\theta(f)$ (rad)')
plt.yticks([-np.pi, 0, np.pi], ['$-\\pi$', '0', '$\\pi$'])
plt.grid(True, linestyle='--', alpha=0.6)
plt.xlim(-5/T, 5/T)

plt.xticks(xticks_pos, xticks_labels)
plt.axvline(x=0, color='gray', linestyle='-', linewidth=0.8)
plt.legend(loc='lower left')

plt.tight_layout(pad=3.0)
plt.show()