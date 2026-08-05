import matplotlib.pyplot as plt
import numpy as np


def quantize_uniform(x: np.ndarray, m: int, x_min: float = 0.0, x_max: float = 1.0):
    """Applies mid-rise uniform quantization to signal x over [x_min, x_max]

    using M levels.
    """
    delta = (x_max - x_min) / m
    levels = x_min + (np.arange(m) + 0.5) * delta # Mid-rise quantization levels 

    # Find quantization bin index [0, M-1]
    bin_idx = np.floor((x - x_min) / delta).astype(int)
    bin_idx = np.clip(bin_idx, 0, m - 1)# Clip to ensure indices are within valid range

    xq = levels[bin_idx]
    error = x - xq# Compute quantization error
    return xq, error, delta


def main():
    # 1. Sampling & Periodic Triangular Waveform Setup [t in [0, 2) seconds]
    fs = 10000  # Sampling frequency: 10 kHz
    t = np.arange(0, 2.0, 1 / fs)
    n_samples = len(t)

    x = np.zeros_like(t)
    mask1 = (t >= 0.0) & (t < 1.0)
    mask2 = (t >= 1.0) & (t < 2.0)
    x[mask1] = t[mask1] # Triangular waveform rising edge
    x[mask2] = -t[mask2] + 2.0 # Triangular waveform falling edge

    # Average Signal Power calculation
    px_sim = np.sum(x**2) / n_samples # Average power of the signal x(t)

    # 2. Multi-Level Evaluation 
    m_values = [8, 16, 32, 64, 128]
    sqnr_sim = []#  Simulated SQNR values
    sqnr_theo = []# Theoretical SQNR values
    errors_dict = {}

    print("UNIFORM QUANTIZER SQNR ANALYSIS (T = 2s, [0,1]) ")
    print(
        "  M   | Bits (R)  |  Step Size (Delta)  | Simulated  | Theoretical "
    )
    

    for m in m_values:
        r_bits = int(np.log2(m))# Number of bits for M levels
        _xq, error, delta = quantize_uniform(x, m)
        errors_dict[m] = error

        # SQNR Calculation in dB
        pe_sim = np.sum(error**2) / n_samples# Average power of the quantization error
        sqnr_s = 10.0 * np.log10(px_sim / pe_sim)# Simulated SQNR in dB
        sqnr_t = 10.0 * np.log10(4.0 * (m**2))

        sqnr_sim.append(sqnr_s)# Store simulated SQNR
        sqnr_theo.append(sqnr_t) 

        print(
            f" {m:3d}   |  {r_bits:3d} bits  |      {delta:.6f} V      |  {sqnr_s:6.2f} dB  |  {sqnr_t:6.2f} dB  "
        )

    
    #  Complete Analysis for M = 8 
    
    xq8, e8, delta8 = quantize_uniform(x, 8)

    _fig1, axs1 = plt.subplots(3, 1, figsize=(10, 8), constrained_layout=True)

    # Task α(i): Time-Domain Input vs Quantized Waveform
    axs1[0].plot(
        t, x, "b--", linewidth=1.5, label="Original Input x(t)"
    )
    axs1[0].plot(
        t, xq8, "r", linewidth=1.5, label="Quantized Output x_q(t)"
    )
    axs1[0].set_title(
        " Time-Domain Input x(t) & Quantized Output x_q(t) (M = 8 Levels)"
    )
    axs1[0].set_ylabel("Amplitude (V)")
    axs1[0].legend(loc="upper right")
    axs1[0].grid(True)

    #  Quantizer Transfer Characteristic Curve (Input vs Output)
    axs1[1].plot(x, xq8, "g", linewidth=2)
    axs1[1].set_title(
        " Quantizer Input-Output Transfer Characteristic Curve (M = 8)"
    )
    axs1[1].set_xlabel("Input Amplitude x(t) [V]")
    axs1[1].set_ylabel("Quantized Output x_q(t) [V]")
    axs1[1].grid(True)

    # Quantization Error Waveform e(t)
    axs1[2].plot(t, e8, "m", linewidth=1.2)
    axs1[2].set_title(
        f" Quantization Error Waveform e(t) = x(t) - x_q(t) (SQNR = {sqnr_sim[0]:.2f} dB)"
    )
    axs1[2].set_xlabel("Time t (s)")
    axs1[2].set_ylabel("Error e(t) [V]")
    axs1[2].set_ylim(-delta8 * 1.2, delta8 * 1.2)
    axs1[2].grid(True)

    
    #  Comparative Quantization Error Waveforms across M 
   
    _fig2, axs2 = plt.subplots(5, 1, figsize=(10, 10), constrained_layout=True)
    colors = ["red", "blue", "green", "purple", "darkorange"]

    for i, m in enumerate(m_values):
        axs2[i].plot(t, errors_dict[m], color=colors[i], linewidth=1.0)
        axs2[i].set_title(
            f"Quantization Error e(t) for M = {m} ({int(np.log2(m))} bits) | SQNR = {sqnr_sim[i]:.2f} dB | Max Error = ±{1/(2*m):.4f} V"
        )
        axs2[i].set_ylabel("Error [V]")
        axs2[i].grid(True)
    axs2[-1].set_xlabel("Time t (s)")

    
    # SQNR (dB) vs Number of Quantization Levels M (6.02 dB/bit rule)
    
    _fig3, ax3 = plt.subplots(figsize=(8, 5), constrained_layout=True)
    bits = [np.log2(m) for m in m_values]

    ax3.plot(
        bits,
        sqnr_theo,
        "k--",
        marker="o",
        linewidth=2,
        label="Theoretical SQNR (6.02 dB/bit)",
    )
    ax3.plot(
        bits,
        sqnr_sim,
        "rx",
        markersize=10,
        markeredgewidth=2,
        label="Simulated SQNR",
    )
    ax3.set_title(
        " SQNR vs Quantization Resolution (6.02 dB/Bit Scaling Law)"
    )
    ax3.set_xlabel("Resolution R (Bits = log2(M))")
    ax3.set_ylabel("SQNR (dB)")
    ax3.set_xticks(bits)
    ax3.set_xticklabels([f"{m} levels\n({int(b)} bits)" for m, b in zip(m_values, bits)])
    ax3.legend(loc="upper left")
    ax3.grid(True)

    plt.show()


if __name__ == "__main__":
    main()