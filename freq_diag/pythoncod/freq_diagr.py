import numpy as np
import matplotlib.pyplot as plt 

# Ορισμός του σήματος x(t)
def x(t):
    x_t = np.zeros_like(t)
    x_t[(t >= -3) & (t <= -2)] = 2
    x_t[np.abs(t) < 2] = np.abs(t[np.abs(t) < 2]) + 2
    x_t[(t >= 2) & (t <= 3)] = 1.5
    return x_t

#Δημιουργεί 2000 σημεία από -5 έως 5 sec (χρονική ανάλυση)
t = np.linspace(-5, 5, 2000)
x_t = x(t)

# --- Αυξάνει την ανάλυση FFT μέσω "zero padding" (προσθήκη μηδενικών). ---
N = 8192  # μεγαλύτερος αριθμός σημείων για πιο ομαλό φάσμα
X_f = np.fft.fftshift(np.fft.fft(x_t, N))#Υπολογίζει το φάσμα (Fourier Transform).np.fft.fftshift()->Τοποθετεί το 0 Hz στο κέντρο του διαγράμματος.
freq = np.fft.fftshift(np.fft.fftfreq(N, d=(t[1]-t[0])))#Υπολογίζει τις αντίστοιχες συχνότητες (άξονας f).

# --- Ομαλοποίηση ---Δίνουν το πλάτος και τη φάση του φάσματος.
magnitude = np.abs(X_f) / np.max(np.abs(X_f))
phase = np.angle(X_f)

# --- Περιορισμός εμφάνισης συχνότητας ---Κρατά μόνο το χρήσιμο κομμάτι του φάσματος (–10 Hz έως 10 Hz).
mask = (freq >= -10) & (freq <= 10)

# -------------------- Διαγράμματα --------------------
plt.figure(figsize=(12,8))

# Σήμα στο χρόνο
plt.subplot(3,1,1)
plt.plot(t, x_t, 'b', linewidth=2)
plt.title('Σήμα x(t)')
plt.xlabel('t')
plt.ylabel('x(t)')
plt.grid(True)

# Φάσμα πλάτους
plt.subplot(3,1,2)
plt.plot(freq[mask], magnitude[mask], 'r')
plt.title('Φάσμα πλάτους |X(f)| (ομαλοποιημένο)')
plt.xlabel('Συχνότητα (Hz)')
plt.ylabel('|X(f)|')
plt.grid(True)

# Φάσμα φάσης
plt.subplot(3,1,3)
plt.plot(freq[mask], phase[mask], 'g')
plt.title('Φάσμα φάσης ∠X(f)')
plt.xlabel('Συχνότητα (Hz)')
plt.ylabel('Φάση (rad)')
plt.grid(True)

plt.tight_layout()
plt.show()

#Πρώτο διάγραμμα – Το σήμα x(t) Είναι το σήμα στον χρονικό χώρο (domain of time).Το συμμετρικό σχήμα γύρω από το 0 δείχνει ότι το σήμα είναι πραγματικό και άρτιο.