import numpy as np
import matplotlib.pyplot as plt

# --- 1. Ορισμός Παραμέτρων ---
A = 1.0     # Πλάτος παλμού
T = 2.0     # Διάρκεια παλμού
Fs = 200.0  # Ρυθμός δειγματοληψίας (Hz)
Ts = 1.0 / Fs
N = 4096    # Πλήθος δειγμάτων (μεγάλο για καλή ανάλυση)

# --- 2. Δημιουργία Χρονικού Άξονα και Παλμού ---
t = np.linspace(-N/(2*Fs), N/(2*Fs), N, endpoint=False)
x_t = np.where(np.abs(t) <= T/2, A, 0.0)  # Ορθογώνιος παλμός, np.where(condition, value_if_true, value_if_false)

# --- 3. Υπολογισμός FFT ---
X_fft = np.fft.fft(x_t)#πίνακας N μιγαδικών τιμών — κάθε στοιχείο αντιστοιχεί σε ένα “συντελεστή” του μετασχηματισμού Fourier, δηλαδή σε κάποια συχνότητα.

#Όμως, το np.fft.fft δεν μας λέει ποιες συχνότητες είναι αυτές.Απλώς δίνει τα N αποτελέσματα του διακριτού μετασχηματισμού, σε σειρά.
f = np.fft.fftfreq(N, d=Ts)#πίνακα συχνοτήτων που αντιστοιχεί σε κάθε δείγμα του FFT.
#Όταν σχεδιάζουμε το φάσμα στο πεδίο της συχνότητας, χρειάζεται να ξέρεις ποια συχνότητα αντιστοιχεί σε κάθε τιμή του FFT.

X_shift = np.fft.fftshift(X_fft)#συμμετρικά γύρω από το 0
f_shift = np.fft.fftshift(f)
X_fft_scaled = X_shift * Ts  # Κλιμάκωση για σωστό πλάτος

# --- 4. Θεωρητική Αναλυτική Μορφή ---ελέγχουμε αν το FFT συμφωνεί με τη θεωρία εφοσον γνωριζουμε και την θεωρητικη λυση
def normalized_sinc(x):
    """Ορισμός κανονικοποιημένης sinc: sin(pi*x)/(pi*x)"""
    return np.where(x == 0, 1.0, np.sin(np.pi * x) / (np.pi * x))

X_anal = A * T * normalized_sinc(f_shift * T)

# --- 5. Αναλυτική Φάση (+π / -π) ---
phase_anal = np.zeros_like(f_shift)
mask_neg = X_anal < 0
phase_anal[(f_shift > 0) & mask_neg] = -np.pi
phase_anal[(f_shift < 0) & mask_neg] = +np.pi

# --- 6. Φάση FFT (για σύγκριση) ---
phase_fft = np.angle(X_fft_scaled)
phase_fft = np.unwrap(np.angle(np.fft.fftshift(X_fft)))
phase_fft = np.fft.fftshift(phase_fft)

# --- 7. Θέσεις Μηδενισμών (±1/T, ±2/T, ±3/T, ...) ---
zero_points = np.arange(-5, 6) / T  # μέχρι ±5/T
zero_points = zero_points[zero_points != 0]

# --- 8. Σχεδίαση Διαγραμμάτων ---
plt.figure(figsize=(10, 12))

# (a) Ορθογώνιος Παλμός
plt.subplot(3, 1, 1)
plt.plot(t, x_t, 'b', linewidth=2)
plt.title('(α) Ορθογώνιος Παλμός $x(t)$', fontsize=14, weight='bold')
plt.xlabel('$t$ (Χρόνος)')
plt.ylabel('$x(t)$')
plt.grid(True, linestyle='--', alpha=0.6)
plt.ylim(-0.2, A + 0.2)
plt.xlim(-2*T, 2*T)
plt.xticks([-T/2, T/2], ['-T/2', 'T/2'])

# (b) Φάσμα Πλάτους
plt.subplot(3, 1, 2)
plt.plot(f_shift, np.abs(X_anal) / (A*T), 'r-', linewidth=2, label='Αναλυτικό |X(f)| / (A·T)')
plt.plot(f_shift, np.abs(X_fft_scaled) / (A*T), 'b.', alpha=0.5, label='FFT (κανονικοποιημένο)')
for zp in zero_points:
    plt.axvline(zp, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
plt.title('(β) Φάσμα Πλάτους $|X(f)|$ (με $AT=1$)', fontsize=14, weight='bold')
plt.xlabel('$f$ (Hz)')
plt.ylabel('$|X(f)|$')
plt.xlim(-5/T, 5/T)
plt.ylim(0, 1.1)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend()
plt.xticks([-2/T, -1/T, 1/T, 2/T], ['-2/T', '-1/T', '1/T', '2/T'])
plt.axvline(0, color='gray', linewidth=0.8)

# (γ) Φάσμα Φάσης
plt.subplot(3, 1, 3)
plt.step(f_shift, phase_anal, 'g-', linewidth=2, label='Αναλυτική Φάση (±π)')
plt.plot(f_shift, np.angle(X_anal), 'r--', linewidth=1, alpha=0.6, label='Περιττή Φάση (από X(f))')
for zp in zero_points:
    plt.axvline(zp, color='gray', linestyle='--', alpha=0.4, linewidth=0.8)
plt.title('(γ) Φάσμα Φάσης $\\theta(f)$', fontsize=14, weight='bold')
plt.xlabel('$f$ (Hz)')
plt.ylabel('$\\theta(f)$ (rad)')
plt.yticks([-np.pi, 0, np.pi], ['$-\\pi$', '0', '$\\pi$'])
plt.xlim(-5/T, 5/T)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='lower left')
plt.xticks([-2/T, -1/T, 1/T, 2/T], ['-2/T', '-1/T', '1/T', '2/T'])
plt.axvline(0, color='gray', linewidth=0.8)

plt.tight_layout(pad=3.0)
plt.show()