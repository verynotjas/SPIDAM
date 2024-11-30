import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile
import tkinter as tk
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

    # Trim data for plotting (start at -5 dB, end at -25 dB)
    trimmed_t = t[index_less_5:index_less_25 + 1]
    trimmed_db = data_in_db[index_less_5:index_less_25 + 1]

    return rt60, trimmed_t, trimmed_db, index_less_5, index_less_25


# Load the WAV file and calculate spectrogram
file_path = upload_wav_file()
if not file_path:
    print("No file selected. Exiting...")
    exit()

sample_rate, data = wavfile.read(file_path)
if len(data.shape) == 2:  # Stereo audio
    data = data[:, 0]  # Take only one channel

spectrum, freqs, t, im = plt.specgram(data, Fs=sample_rate, NFFT=1024, cmap="viridis")

# Pre-compute RT60 for Low, Mid, and High ranges
low_rt60, low_t, low_db, _, _ = calculate_rt60(data, freqs, spectrum, t, (0, 250))
mid_rt60, mid_t, mid_db, _, _ = calculate_rt60(data, freqs, spectrum, t, (250, 2000))
high_rt60, high_t, high_db, _, _ = calculate_rt60(data, freqs, spectrum, t, (2000, 20000))

# Tkinter GUI
root = tk.Tk()
root.title("RT60 Analysis")

# Create a Matplotlib figure
fig, ax = plt.subplots(figsize=(8, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()


# Function to update the graph
def update_graph(rt60, trimmed_t, trimmed_db, title):
    ax.clear()
    ax.plot(trimmed_t, trimmed_db, label="Power (dB)", color="orange")
    ax.set_title(title, fontsize=16)
    ax.set_xlabel("Time (s)", fontsize=14)
    ax.set_ylabel("Power (dB)", fontsize=14)
    ax.legend()
    ax.grid()
    canvas.draw()
    rt60_label.config(text=f"RT60: {round(rt60, 2)} seconds")


# Button callback functions
def show_low_rt60():
    update_graph(low_rt60, low_t, low_db, "Low RT60 (0-250 Hz)")


def show_mid_rt60():
    update_graph(mid_rt60, mid_t, mid_db, "Mid RT60 (250-2000 Hz)")


def show_high_rt60():
    update_graph(high_rt60, high_t, high_db, "High RT60 (2000-20000 Hz)")


# Buttons to cycle through graphs
button_low = tk.Button(root, text="Low RT60", command=show_low_rt60)
button_low.pack(side=tk.LEFT, padx=5, pady=5)

button_mid = tk.Button(root, text="Mid RT60", command=show_mid_rt60)
button_mid.pack(side=tk.LEFT, padx=5, pady=5)

button_high = tk.Button(root, text="High RT60", command=show_high_rt60)
button_high.pack(side=tk.LEFT, padx=5, pady=5)

# Label for RT60 value
rt60_label = tk.Label(root, text="RT60: -- seconds", font=("Arial", 14))
rt60_label.pack()

# Start with Low RT60
show_low_rt60()

# Start Tkinter main loop
root.mainloop()

