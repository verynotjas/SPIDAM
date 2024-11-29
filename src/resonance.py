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

# Generate time array for plotting
if len(data.shape) == 2:  # Stereo audio
    data = data[:, 0]  # Take only one channel
time = np.linspace(0, len(data) / sample_rate, num=len(data))

# Plot the waveform
plt.figure(figsize=(10, 6))  # Set figure size for better visibility
plt.plot(time, data, color='blue', linewidth=1)

# Add title and labels
plt.title("Waveform Graph", fontsize=16)
plt.xlabel("Time (s)", fontsize=14)
plt.ylabel("Amplitude", fontsize=14)

# Add grid for better visibility
plt.grid()

# Adjust layout and display the plot
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()
