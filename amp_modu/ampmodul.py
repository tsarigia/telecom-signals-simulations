#ΕΙΣΑΓΩΓΗ ΒΙΒΛΙΟΘΗΚΩΝ 
 #Να γίνει σε γραφικό περιβάλλον σε Python ένα προγραμμα που να δέχεται πλάτος σήματος πληφορίας,  πλάτος φέροντος, συχνότητα σήματος πληροφορίας, συχνότητα σήματος πληροφορίας και να εμφανίζει στο πεδίο του χρόνου διάγραμμα του σήματος πληροφορίας, διάγραμμα του φέροντος, του σήματος ΑΜ και του αποδιαμορφωμένου σήματος ΑΜ. 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # Για να ενσωματωθεί το matplotlib στο Tkinter GUI
import tkinter as tk  # Για δημιουργία γραφικού περιβάλλοντος (GUI)
from tkinter import ttk # Βελτιωμένα γραφικά στοιχεία για Tkinter

# ΣΥΝΑΡΤΗΣΗ ΠΟΥ ΕΚΤΕΛΕΙ ΤΟΥΣ ΥΠΟΛΟΓΙΣΜΟΥΣ ΚΑΙ ΤΑ ΓΡΑΦΗΜΑΤΑ
def generate_plot():
    # Ανάγνωση τιμών από τα πεδία εισαγωγής του GUI 
    Am = float(entry_Am.get())   # Πλάτος σήματος πληροφορίας (π.χ. 0.5)
    fm = float(entry_fm.get())   # Συχνότητα πληροφορίας (π.χ. 20 Hz)
    Ac = float(entry_Ac.get())   # Πλάτος φέροντος σήματος (π.χ. 1)
    fc = float(entry_fc.get())   # Συχνότητα φέροντος (π.χ. 200 Hz)

    #Δημιουργία χρονικού άξονα 
    # Χρονικό διάστημα 0 έως 0.05 sec (ώστε να φαίνονται πλήρεις κύκλοι)
    # 5000 σημεία -> ομαλό ημίτονο
    t = np.linspace(0, 0.05,10000)
    
    message = Am*np.cos(2*np.pi*fm*t) # Σήμα πληροφορίας
    carrier = Ac * np.cos(2 * np.pi * fc * t)     # Φέρον σήμα
    mu = Am / Ac      # Συντελεστής διαμόρφωσης μ
    am_signal = Ac * (1 + mu * np.cos(2 * np.pi * fm * t)) * np.cos(2 * np.pi * fc * t)  # Σήμα AM
    demodulated = Ac * (1 + mu * np.cos(2 * np.pi * fm * t))  # Αποδιαμορφωμένο (περιβάλλουσα)
    
    # Καθαρισμός προηγούμενων γραφημάτων 
    for widget in frame_plot.winfo_children():
        widget.destroy()
    # Δημιουργία παραθύρου γραφημάτων 
    fig, axs = plt.subplots(4, 1, figsize=(7, 6), constrained_layout=True)
    
    # 1️⃣ Σήμα πληροφορίας
    axs[0].plot(t, message, 'b', linewidth=2)
    axs[0].set_title("Message Signal (Πληροφορία)")
    axs[0].set_xlabel("Χρόνος (s)")
    axs[0].set_ylabel("Πλάτος")
    axs[0].grid(True)
    
    # 2️⃣ Φέρον σήμα
    axs[1].plot(t, carrier, 'm', linewidth=1.5)
    axs[1].set_title("Carrier Signal (Φέρον)")
    axs[1].set_xlabel("Χρόνος (s)")
    axs[1].set_ylabel("Πλάτος")
    axs[1].grid(True)

    # 3️⃣ AM Σήμα (διαμορφωμένο)
    axs[2].plot(t, am_signal, 'r', linewidth=1.5)
    axs[2].set_title("AM Signal (Διαμορφωμένο)")
    axs[2].set_xlabel("Χρόνος (s)")
    axs[2].set_ylabel("Πλάτος")
    axs[2].grid(True)

    # 4️⃣ Αποδιαμορφωμένο (περιβάλλουσα)
    axs[3].plot(t, demodulated, 'g', linewidth=2)
    axs[3].set_title("Demodulated Signal (Αποδιαμορφωμένο)")
    axs[3].set_xlabel("Χρόνος (s)")
    axs[3].set_ylabel("Πλάτος")
    axs[3].grid(True)
    
    # Εμφάνιση των γραφημάτων στο GUI-Ενσωματώνουμε τα plots στο GUI
    canvas = FigureCanvasTkAgg(fig, master=frame_plot)
    canvas.draw()
    canvas.get_tk_widget().pack()
    
# ΔΗΜΙΟΥΡΓΙΑ ΓΡΑΦΙΚΟΥ ΠΕΡΙΒΑΛΛΟΝΤΟΣ (Tkinter)
root = tk.Tk()
root.title("Amplitude Modulation (AM) Demo")

#Περιοχή εισαγωγής παραμέτρων
frame_input = ttk.Frame(root, padding=10)
frame_input.pack(side=tk.LEFT,fill=tk.Y)

ttk.Label(frame_input, text="Message Amplitude (Am):").pack()#κείμενο (“Message Amplitude”).
entry_Am = ttk.Entry(frame_input)#πεδίο για να γράψει ο χρήστης.
entry_Am.insert(0, "0.5")#αρχική τιμή (π.χ. 0.5).
entry_Am.pack()#τοποθετεί το widget μέσα στο παράθυρο.

ttk.Label(frame_input, text="Message Frequency (fm) [Hz]:").pack()
entry_fm = ttk.Entry(frame_input)
entry_fm.insert(0, "200")
entry_fm.pack()

ttk.Label(frame_input, text="Carrier Amplitude (Ac):").pack()
entry_Ac = ttk.Entry(frame_input)
entry_Ac.insert(0, "1")
entry_Ac.pack()

ttk.Label(frame_input, text="Carrier Frequency (fc) [Hz]:").pack()
entry_fc = ttk.Entry(frame_input)
entry_fc.insert(0, "1000")
entry_fc.pack()

#Κουμπί για παραγωγή γραφημάτων 
ttk.Button(frame_input, text="Generate & Plot", command=generate_plot).pack(pady=10)#Όταν το πατήσεις, καλεί τη συνάρτηση generate_plot().

# Περιοχή εμφάνισης γραφημάτων
frame_plot = ttk.Frame(root, padding=10)#Είναι το “δεξί” κομμάτι του παραθύρου όπου θα εμφανίζονται τα γραφήματα.
frame_plot.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

#Εκκίνηση GUI
root.mainloop()

#tkinter: Δημιουργεί το γραφικό παράθυρο (GUI).
#matplotlib.backends.backend_tkagg: Ενώνει το matplotlib με το Tkinter — ώστε τα plots να φαίνονται μέσα στο GUI, όχι σε ξεχωριστό παράθυρο.