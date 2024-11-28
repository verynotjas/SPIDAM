import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

def read_audio(file_path):
    """
    Reads a .wav audio file and returns its sample rate and data.

    Parameters:
        file_path (str): Path to the .wav file.

    Returns:
        tuple: Sample rate and audio data as a numpy array.
    """
    sample_rate, audio_data = wav.read(file_path)
    if audio_data.ndim > 1:
        audio_data = audio_data[:, 0]  # Use only one channel for stereo
    return sample_rate, audio_data

def compute_frequency_ranges(audio_data, sample_rate):
    """
    Computes the power of low, mid, and high frequency ranges in the audio data.

    Parameters:
        audio_data (np.ndarray): Audio signal data.
        sample_rate (int): Sample rate of the audio signal.

    Returns:
        dict: Power in low, mid, and high frequency ranges.
    """
    # Perform FFT
    n = len(audio_data)
    fft_result = np.fft.fft(audio_data)
    fft_magnitude = np.abs(fft_result[:n // 2])  # Take magnitude of first half
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)[:n // 2]

    # Define frequency ranges
    low_range = (0, 300)  # Low frequencies (e.g., bass)
    mid_range = (300, 2000)  # Mid frequencies (e.g., vocals)
    high_range = (2000, sample_rate // 2)  # High frequencies (e.g., treble)

    # Compute power in each range
    def compute_power_in_range(freq_range):
        indices = np.where((frequencies >= freq_range[0]) & (frequencies < freq_range[1]))
        return np.sum(fft_magnitude[indices]**2)

    power = {
        "Low": compute_power_in_range(low_range),
        "Mid": compute_power_in_range(mid_range),
        "High": compute_power_in_range(high_range)
    }
    return power

def plot_frequency_spectrum(audio_data, sample_rate):
    """
    Plots the frequency spectrum of the audio data.

    Parameters:
        audio_data (np.ndarray): Audio signal data.
        sample_rate (int): Sample rate of the audio signal.
    """
    n = len(audio_data)
    fft_result = np.fft.fft(audio_data)
    fft_magnitude = np.abs(fft_result[:n // 2])
    frequencies = np.fft.fftfreq(n, d=1/sample_rate)[:n // 2]

    plt.figure(figsize=(10, 6))
    plt.plot(frequencies, fft_magnitude)
    plt.title("Frequency Spectrum")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Input: Path to the audio file
    file_path = input("Enter the path to your .wav audio file: ")

    try:
        sample_rate, audio_data = read_audio(file_path)
        power = compute_frequency_ranges(audio_data, sample_rate)
        print("Frequency Power Distribution:")
        print(f"Low Frequency Power: {power['Low']:.2f}")
        print(f"Mid Frequency Power: {power['Mid']:.2f}")
        print(f"High Frequency Power: {power['High']:.2f}")

        plot_frequency_spectrum(audio_data, sample_rate)
    except Exception as e:
        print(f"Error: {e}")