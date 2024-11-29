import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tkinter import filedialog


# Function to upload the WAV file
def upload_wav_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    return file_path


# Function to calculate RT60
def calculate_rt60(data, freqs, spectrum, t, freq_range):
    # Select target frequencies within the given range
    mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
    target_spectrum = np.mean(spectrum[mask], axis=0)

    # Convert to dB
    data_in_db = 10 * np.log10(target_spectrum)

    # Find max value and -5 dB, -25 dB below max
    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    value_max_less_5 = value_of_max - 5
    value_max_less_25 = value_of_max - 25

    # Find indices for -5 dB and -25 dB
    def find_nearest_value(array, value):
        idx = (np.abs(array - value)).argmin()
        return idx

    index_less_5 = find_nearest_value(data_in_db[index_of_max:], value_max_less_5) + index_of_max
    index_less_25 = find_nearest_value(data_in_db[index_of_max:], value_max_less_25) + index_of_max

    # Calculate RT20 and RT60
    rt20 = t[index_less_25] - t[index_less_5]
    rt60 = rt20 * 3

    return rt60, data_in_db, index_of_max, index_less_5, index_less_25


# Load the WAV file and calculate spectrogram
file_path = upload_wav_file()
if not file_path:
    print("No file selected. Exiting...")
    exit()

sample_rate, data = wavfile.read(file_path)
if len(data.shape) == 2:  # Stereo audio
    data = data[:, 0]  # Take only one channel

spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap="viridis")

# Calculate RT60 for Low, Mid, and High ranges
rt60_low, db_low, max_low, less_5_low, less_25_low = calculate_rt60(data, freqs, spectrum, t, (0, 250))
rt60_mid, db_mid, max_mid, less_5_mid, less_25_mid = calculate_rt60(data, freqs, spectrum, t, (250, 2000))
rt60_high, db_high, max_high, less_5_high, less_25_high = calculate_rt60(data, freqs, spectrum, t, (2000, 20000))

# Create Combined Graph
plt.figure(figsize=(10, 6))
plt.plot(t, db_low, color="blue", label="Low (0-250 Hz)")
plt.plot(t, db_mid, color="orange", label="Mid (250-2000 Hz)")
plt.plot(t, db_high, color="purple", label="High (2000-20000 Hz)")

# Add markers for key points
plt.plot(t[max_low], db_low[max_low], "go", label="Low Max dB")
plt.plot(t[less_5_low], db_low[less_5_low], "yo", label="Low -5 dB")
plt.plot(t[less_25_low], db_low[less_25_low], "ro", label="Low -25 dB")

plt.plot(t[max_mid], db_mid[max_mid], "g^", label="Mid Max dB")
plt.plot(t[less_5_mid], db_mid[less_5_mid], "y^", label="Mid -5 dB")
plt.plot(t[less_25_mid], db_mid[less_25_mid], "r^", label="Mid -25 dB")

plt.plot(t[max_high], db_high[max_high], "gs", label="High Max dB")
plt.plot(t[less_5_high], db_high[less_5_high], "ys", label="High -5 dB")
plt.plot(t[less_25_high], db_high[less_25_high], "rs", label="High -25 dB")

# Add title, labels, and legend
plt.title("Combined RT60 Graph", fontsize=16)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Power (dB)", fontsize=14)
plt.legend()
plt.grid()

# Display the plot
plt.tight_layout()
plt.show()

# Print RT60 Values
print(f"Low RT60: {round(rt60_low, 2)} seconds")
print(f"Mid RT60: {round(rt60_mid, 2)} seconds")
print(f"High RT60: {round(rt60_high, 2)} seconds")
