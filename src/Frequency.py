import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# File upload functionality
def upload_wav_file():
    Tk().withdraw()  # Hide Tkinter root window
    file_path = askopenfilename(filetypes=[("WAV files", "*.wav")])
    return file_path

# Load the WAV file
file_path = upload_wav_file()
if not file_path:
    print("No file selected. Exiting...")
    exit()

sample_rate, data = wavfile.read(file_path)
print(f"Loaded file: {file_path}")

# Compute spectrogram
plt.figure(figsize=(10, 6))  # Set figure size for better visibility
spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap="autumn_r")

# Add title and labels
plt.title("Frequency Graph", fontsize=16)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Frequency (Hz)", fontsize=14)

# Add a colorbar
cbar = plt.colorbar(im)
cbar.set_label("Intensity (dB)", fontsize=12)

# Display the plot
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
