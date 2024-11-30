# view.py

import numpy as np
import librosa
import librosa.display
import soundfile as sf


from tkinter import messagebox

from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.io import wavfile

# Function to clear the previous graph
def clear_canvas(canvas_widget):
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()

def base_plot(file_path, root, canvas):
    """
    The purpose of this function is to display the audio file into waveform in the GUI

    Parameters: (str) File path, (obj) root

    Returns: None
    """

    try:
        clear_canvas(canvas)
        y, sample_rate = sf.read(file_path)

        if len(y.shape) != 1:
            convert_to_mono(file_path)
        time = np.linspace(0, len(y) / sample_rate, num=len(y))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, y, color="blue")
        ax.set_title("Waveform of Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {e}")

def intensity_plot(file_path, root, canvas):
    """
    The purpose of this function is to plot the intensity plot of the sound file

    Parameters: (str) File path, (obj) root

    Returns: None
    """

    try:
        clear_canvas(canvas)
        y, sr = librosa.load(file_path, sr=None)
        S = librosa.power_to_db(np.abs(librosa.stft(y)), ref=np.max)

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        im = ax.imshow(S, aspect='auto', origin='lower', cmap='magma')
        fig.colorbar(im, ax=ax)
        ax.set_title("Intensity Plot")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Frequency (Hz)")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting intensity: {e}")


def convert_to_mono(file_path):

    # Load audio file
    y, sr = librosa.load(file_path, sr=None, mono=False)

    # Convert to mono by averaging channels
    if y.ndim > 1:
        y_mono = y.mean(axis=0)
    else:
        y_mono = y


# Extra Credit
def combine_plots(file_path, root):
    """
    The purpose of this function is to combine all the plots into one plot

    Parameters: (str) File path, (obj) root

    Returns: None
    """

    pass


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

    return rt60, trimmed_t, trimmed_db


def show_low_rt60(file_path, root, canvas):
    try:
        clear_canvas(canvas)  # Clear existing plot
        y, sample_rate = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        # Generate spectrogram
        spectrum, freqs, t, _ = plt.specgram(y, Fs=sample_rate, NFFT=1024)

        # Calculate RT60
        low_rt60, low_t, low_db = calculate_rt60(y, freqs, spectrum, t, (0, 250))

        # Plot graph
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(low_t, low_db, color="orange")
        ax.set_title("Low RT60 (0-250 Hz)", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=14)
        ax.set_ylabel("Power (dB)", fontsize=14)
        ax.grid()

        # Update the canvas with the new plot
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

def show_mid_rt60(file_path, root, canvas):
    try:
        # Load audio file
        clear_canvas(canvas)
        y, sample_rate = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        # Generate spectrogram
        spectrum, freqs, t, _ = plt.specgram(y, Fs=sample_rate, NFFT=1024)

        # Calculate RT60
        mid_rt60, mid_t, mid_db = calculate_rt60(y, freqs, spectrum, t, (250, 2000))

        # Plot graph
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(mid_t, mid_db, color="green")
        ax.set_title("Mid RT60 (250-2000 Hz)", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=14)
        ax.set_ylabel("Power (dB)", fontsize=14)
        ax.grid()

        # Add the plot to the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

def show_high_rt60(file_path, root, canvas):
    try:
        # Load audio file
        clear_canvas(canvas)
        y, sample_rate = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        # Generate spectrogram
        spectrum, freqs, t, _ = plt.specgram(y, Fs=sample_rate, NFFT=1024)

        # Calculate RT60
        high_rt60, high_t, high_db = calculate_rt60(y, freqs, spectrum, t, (2000, 20000))

        # Plot graph
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(high_t, high_db, color="red")
        ax.set_title("High RT60 (2000-20000 Hz)", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=14)
        ax.set_ylabel("Power (dB)", fontsize=14)
        ax.grid()

        # Add the plot to the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)



    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

# Alternate plot button set up
current_plot = {"index": 0}  # Track the current plot (0 = Low, 1 = Mid, 2 = High)

def show_next_rt60(file_path, root, canvas):
    plots = [show_low_rt60, show_mid_rt60, show_high_rt60]
    plot_func = plots[current_plot["index"]]
    plot_func(file_path, root, canvas)  # Call the current plot function
    current_plot["index"] = (current_plot["index"] + 1) % len(plots)  # Cycle to the next plot

# Function to update the graph
def update_graph(rt60, trimmed_t, trimmed_db, title):
    plt.figure()
    plt.plot(trimmed_t, trimmed_db, label="Power (dB)", color="orange")
    plt.title(title, fontsize=16)
    plt.xlabel("Time (s)", fontsize=14)
    plt.ylabel("Power (dB)", fontsize=14)
    plt.legend()
    plt.grid()
    plt.show()

def combine_plots(file_path, root, canvas):
    """
    The purpose of this function is to combine all the RT60 plots into one plot.
    It plots Low, Mid, and High frequency RT60s on a single figure.

    Parameters: (str) File path, (obj) root

    Returns: None
    """

    try:
        clear_canvas(canvas)  # Clear existing plot
        y, sample_rate = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        # Generate spectrogram
        spectrum, freqs, t, _ = plt.specgram(y, Fs=sample_rate, NFFT=1024)

        # Calculate RT60 for Low, Mid, and High frequency ranges
        low_rt60, low_t, low_db = calculate_rt60(y, freqs, spectrum, t, (0, 250))
        mid_rt60, mid_t, mid_db = calculate_rt60(y, freqs, spectrum, t, (250, 2000))
        high_rt60, high_t, high_db = calculate_rt60(y, freqs, spectrum, t, (2000, 20000))

        # Create the combined graph
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Plot all the RT60 graphs in one plot
        ax.plot(low_t, low_db, color="blue", label="Low (0-250 Hz)", alpha=0.7)
        ax.plot(mid_t, mid_db, color="green", label="Mid (250-2000 Hz)", alpha=0.7)
        ax.plot(high_t, high_db, color="red", label="High (2000-20000 Hz)", alpha=0.7)

        # Add titles and labels
        ax.set_title("Combined RT60 for Low, Mid, and High Frequencies", fontsize=16)
        ax.set_xlabel("Time (s)", fontsize=14)
        ax.set_ylabel("Power (dB)", fontsize=14)
        ax.legend()
        ax.grid()

        # Update the canvas with the new plot
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while combining the plots: {e}")