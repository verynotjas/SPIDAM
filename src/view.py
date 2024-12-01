# view.py

import librosa.display

from model import *
from tkinter import messagebox
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def clear_canvas(canvas_widget):
    """
    This functions clears the last plot plotted

    Parameter: canvas_widget
    Return: None
    """

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
        y, sr = sf.read(file_path)

        if len(y.shape) != 1:
            convert_to_mono(file_path)
        time = np.linspace(0, len(y) / sr, num=len(y))

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

def plot_low_rt60(file_path, root, canvas):
    """
    This function plots the low RT60 plot

    Parameters: (str) File path, (obj) root, canvas
    Returns: None
    """

    try:
        clear_canvas(canvas)
        y, sr = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        spectrum, freqs, t, _ = plt.specgram(y, Fs=sr, NFFT=1024)

        low_rt60, low_t, low_db = calculate_rt60(y, freqs, spectrum, t, (0, 250))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(low_t, low_db, color="orange")
        ax.set_title("Low RT60 (0-250 Hz)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

def plot_mid_rt60(file_path, root, canvas):
    """
    This function plots the mid RT60 plot

    Parameters: (str) File path, (obj) root, canvas
    Returns: None
    """

    try:
        clear_canvas(canvas)
        y, sr = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        spectrum, freqs, t, _ = plt.specgram(y, Fs=sr, NFFT=1024)

        mid_rt60, mid_t, mid_db = calculate_rt60(y, freqs, spectrum, t, (250, 2000))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(mid_t, mid_db, color="green")
        ax.set_title("Mid RT60 (250-2000 Hz)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)


    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

def plot_high_rt60(file_path, root, canvas):
    """
    This function plots the high RT60 plot

    Parameters: (str) File path, (obj) root, canvas
    Returns: None
    """

    try:
        clear_canvas(canvas)
        y, sr = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        spectrum, freqs, t, _ = plt.specgram(y, Fs=sr, NFFT=1024)

        high_rt60, high_t, high_db = calculate_rt60(y, freqs, spectrum, t, (2000, 20000))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(high_t, high_db, color="red")
        ax.set_title("High RT60 (2000-20000 Hz)")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)



    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while processing: {e}")

current_plot = {"index": 0}  # Track the current plot (0 = Low, 1 = Mid, 2 = High)

def alternate_rt60(file_path, root, canvas):
    """
    This function alternates through RT60 plots

    Parameters: (str) File path, (obj) root, canvas
    Returns: None
    """

    plots = [plot_low_rt60, plot_mid_rt60, plot_high_rt60]
    plot_func = plots[current_plot["index"]]
    plot_func(file_path, root, canvas)  # Call the current plot function
    current_plot["index"] = (current_plot["index"] + 1) % len(plots)  # Cycle to the next plot

def update_graph(rt60, trimmed_t, trimmed_db, title):
    """
    This function updates the graph

    Parameters: rt60, trimmed_t, trimmed_db, (title) root, canvas
    Return: None
    """

    plt.figure()
    plt.plot(trimmed_t, trimmed_db, label="Power (dB)", color="orange")
    plt.title(title)
    plt.xlabel("Time (s)")
    plt.ylabel("Power (dB)")
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
        clear_canvas(canvas)
        y, sr = sf.read(file_path)
        if len(y.shape) != 1:  # Convert to mono if stereo
            y = np.mean(y, axis=1)

        spectrum, freqs, t, _ = plt.specgram(y, Fs=sr, NFFT=1024)

        low_rt60, low_t, low_db = calculate_rt60(y, freqs, spectrum, t, (0, 250))
        mid_rt60, mid_t, mid_db = calculate_rt60(y, freqs, spectrum, t, (250, 2000))
        high_rt60, high_t, high_db = calculate_rt60(y, freqs, spectrum, t, (2000, 20000))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)

        ax.plot(low_t, low_db, color="orange", label="Low (0-250 Hz)", alpha=0.7)
        ax.plot(mid_t, mid_db, color="green", label="Mid (250-2000 Hz)", alpha=0.7)
        ax.plot(high_t, high_db, color="red", label="High (2000-20000 Hz)", alpha=0.7)

        ax.set_title("Combined RT60 for Low, Mid, and High Frequencies")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Power (dB)")
        ax.legend()
        ax.grid()

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=330, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while combining the plots: {e}")

def difference_average(file_path):

    """
    This function calculates the difference average bewteen RT60 values

    :param file_path:
    :return:
    """
    # Read the audio file
    y, sr = sf.read(file_path)
    if len(y.shape) != 1:  # Convert to mono if stereo
        y = np.mean(y, axis=1)

    # Calculate the spectrogram
    spectrum, freqs, t, _ = plt.specgram(y, Fs=sr, NFFT=1024)

    # Calculate RT60 values for low, mid, and high frequency ranges
    low_rt60, _, _ = calculate_rt60(y, freqs, spectrum, t, (0, 250))
    mid_rt60, _, _ = calculate_rt60(y, freqs, spectrum, t, (250, 2000))
    high_rt60, _, _ = calculate_rt60(y, freqs, spectrum, t, (2000, 20000))

    low_average = abs(low_rt60 - 0.5)
    mid_average = abs(mid_rt60 - 0.5)
    high_average = abs(high_rt60 - 0.5)

    return ((low_average + mid_average + high_average) / 3)
