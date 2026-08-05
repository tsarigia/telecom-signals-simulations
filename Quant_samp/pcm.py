import os

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def invalaw(y: np.ndarray, alpha: float = 87.6) -> np.ndarray:
    """Inverse A-Law Expander: Maps compressed y in [-1, 1] back to linear scale."""
    x = np.zeros_like(y)
    thresh = 1.0 / (1.0 + np.log(alpha))

    idx1 = np.abs(y) < thresh
    idx2 = np.abs(y) >= thresh

    x[idx1] = np.sign(y[idx1]) * (np.abs(y[idx1]) * (1.0 + np.log(alpha))) / alpha #[idx1] is the index of the elements in y that are less than thresh in absolute value. For these elements, we apply the inverse A-Law formula for small values. 
    x[idx2] = np.sign(y[idx2]) * (np.exp(np.abs(y[idx2]) * (1.0 + np.log(alpha)) - 1.0)) / alpha # [idx2] is the index of the elements in y that are greater than or equal to thresh in absolute value. For these elements, we apply the inverse A-Law formula for larger values.
    return x


def alaw_pcm(a: np.ndarray, n: int, alpha: float = 87.6):
    """A-Law PCM scheme: Compresses input, quantizes uniformly to n levels, and reconstructs via invalaw. Returns (sqnr_db, a_quan, code, x_rec).
    """
    y = np.zeros_like(a)
    thresh = 1.0 / alpha

    idx1 = np.abs(a) < thresh
    idx2 = np.abs(a) >= thresh

    y[idx1] = np.sign(a[idx1]) * (alpha * np.abs(a[idx1])) / (1.0 + np.log(alpha))
    y[idx2] = np.sign(a[idx2]) * (1.0 + np.log(alpha * np.abs(a[idx2]))) / (1.0 + np.log(alpha))

    # Uniform quantization of compressed signal
    a_quan, _, _ = uniform_pcm(y, n)
    code = a_quan  # Normalized quantization levels

    # Reconstruction via inverse A-Law
    x_rec = invalaw(a_quan, alpha)

    # Compute Signal-to-Quantization-Noise Ratio (SQNR in dB)
    sqnr = 10.0 * np.log10(np.sum(a**2) / np.sum((a - x_rec) ** 2))
    return sqnr, a_quan, code, x_rec



# 2. UNIFORM PCM, MU-LAW & DPCM HELPER FUNCTIONS

def uniform_pcm(x: np.ndarray, n_levels: int):
    """Standard Linear Uniform PCM over [-1, 1]."""
    step = 2.0 / n_levels
    levels = np.linspace(-1.0 + step / 2.0, 1.0 - step / 2.0, n_levels)
    idx = np.round((x + 1.0) / step).astype(int)
    idx = np.clip(idx, 0, n_levels - 1)
    x_rec = levels[idx]
    error = x - x_rec
    sqnr = 10.0 * np.log10(np.sum(x**2) / np.sum(error**2))
    return x_rec, error, sqnr


def mulaw_compress(x: np.ndarray, mu: float = 255.0) -> np.ndarray:
    """ITU-T G.711 mu-Law Compressor."""
    return np.sign(x) * np.log10(1.0 + mu * np.abs(x)) / np.log10(1.0 + mu)


def mulaw_expand(y: np.ndarray, mu: float = 255.0) -> np.ndarray:
    """ITU-T G.711 mu-Law Expander."""
    return np.sign(y) * (((1.0 + mu) ** np.abs(y) - 1.0) / mu)


def dpcm_pcm(x: np.ndarray, n_levels: int):
    """First-Order Differential PCM (DPCM). Quantizes prediction error."""
    l_len = len(x)
    x_rec = np.zeros(l_len)
    error = np.zeros(l_len)
    pred = 0.0

    # Quantization range for differences [-0.5, 0.5]
    step = 1.0 / n_levels
    levels = np.linspace(-0.5 + step / 2.0, 0.5 - step / 2.0, n_levels)

    for i in range(l_len):
        diff = x[i] - pred
        idx = int(np.round((diff + 0.5) / step))
        idx = max(0, min(idx, n_levels - 1))
        dq = levels[idx]

        x_rec[i] = pred + dq
        pred = x_rec[i]
        error[i] = x[i] - x_rec[i]

    sqnr = 10.0 * np.log10(np.sum(x**2) / np.sum(error**2))
    return x_rec, error, sqnr



#  3. MAIN ANALYSIS SCRIPT

def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))# Get the directory of the current script
    wav_path = os.path.join(script_dir, "speech.wav")# Construct the full path to the speech.wav file in the same directory as the script
    if os.path.exists(wav_path): # Check if the speech.wav file exists
        fs, data = wavfile.read(wav_path)
        x = data.astype(float)
        if x.ndim > 1: # If the audio data has more than one channel (stereo), convert it to mono by taking the first channel
            x = x[:, 0]  # Mono conversion
    else:
        # Generate authentic speech-like synthetic signal if file not present
        fs = 8000
        t = np.arange(0, 1.0, 1 / fs)
        x = (
            0.5 * np.sin(2 * np.pi * 300 * t) * np.exp(-2 * t)
            + 0.3 * np.sin(2 * np.pi * 800 * t)
            + 0.1 * np.random.normal(0, 1, len(t))
        )

    # Normalize input to [-1, 1]
    x = x / np.max(np.abs(x))
    n_levels = 256  # 8-bit quantization

    # Scheme (δ): Uniform PCM
    _, e_unif, sqnr_unif = uniform_pcm(x, n_levels)

    # Scheme (γ): A-Law PCM (alpha = 87.6)
    sqnr_alaw, _, _, x_alaw = alaw_pcm(x, n_levels, alpha=87.6)
    e_alaw = x - x_alaw

    # Scheme (β): mu-Law PCM (mu = 255)
    y_mu = mulaw_compress(x, mu=255.0)
    y_mu_q, _, _ = uniform_pcm(y_mu, n_levels)
    x_mulaw = mulaw_expand(y_mu_q, mu=255.0)
    e_mulaw = x - x_mulaw
    sqnr_mulaw = 10.0 * np.log10(np.sum(x**2) / np.sum(e_mulaw**2))

    # Scheme (α): Differential PCM (DPCM)
    _, e_dpcm, sqnr_dpcm = dpcm_pcm(x, n_levels)

    # Print Comparative SQNR 
   
    print("  EXERCISE 6: SQNR COMPARISON (N = 256)  ")
  
    print(f"  Differential PCM (DPCM):   {sqnr_dpcm:6.2f} dB")
    print(f"  mu-Law PCM (mu = 255):   {sqnr_mulaw:6.2f} dB")
    print(f"  A-Law PCM (alpha = 87.6):  {sqnr_alaw:6.2f} dB")
    print(f"  Uniform PCM (N = 256): {sqnr_unif:6.2f} dB")
  

    # Plot Quantization Error Waveforms
    t_plot = np.arange(len(x)) / fs
    idx = slice(0, min(800, len(x)))  # First 800 samples

    _fig, axs = plt.subplots(4, 1, figsize=(10, 8), constrained_layout=True)

    axs[0].plot(t_plot[idx], e_dpcm[idx], "r", linewidth=1.2)
    axs[0].set_title(f"(α) DPCM Error Waveform (SQNR = {sqnr_dpcm:.2f} dB)")
    axs[0].set_ylabel("Error e[n]")
    axs[0].grid(True)

    axs[1].plot(t_plot[idx], e_mulaw[idx], "b", linewidth=1.2)
    axs[1].set_title(
        f"(β) µ-Law PCM Error Waveform (SQNR = {sqnr_mulaw:.2f} dB)"
    )
    axs[1].set_ylabel("Error e[n]")
    axs[1].grid(True)

    axs[2].plot(t_plot[idx], e_alaw[idx], "g", linewidth=1.2)
    axs[2].set_title(
        f"(γ) A-Law PCM Error Waveform (SQNR = {sqnr_alaw:.2f} dB)"
    )
    axs[2].set_ylabel("Error e[n]")
    axs[2].grid(True)

    axs[3].plot(t_plot[idx], e_unif[idx], "m", linewidth=1.2)
    axs[3].set_title(
        f"(δ) Uniform PCM Error Waveform (SQNR = {sqnr_unif:.2f} dB)"
    )
    axs[3].set_xlabel("Time (s)")
    axs[3].set_ylabel("Error e[n]")
    axs[3].grid(True)

    plt.show()


if __name__ == "__main__":
    main()