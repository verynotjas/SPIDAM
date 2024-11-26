# view.py

import numpy as np
import librosa
import librosa.display
import soundfile as sf

from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def base_plot(file_path, root):
    """
    The purpose of this function is to display the audio file into waveform in the GUI

    Parameters: (str) File path, (str) root

    Returns: None
    """

    try:
        y, sample_rate = sf.read(file_path)

        if len(y.shape) != 1:
            messagebox.showerror("Error", "Please use a mono file.")
            return

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

def intensity_plot(file_path, root):
    """
    The purpose of this function is to plot the intensity plot of the sound file

    Parameters: (str) File path, (str) root

    Returns: None
    """

    try:
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


def RT60_plot(file_path, root):
    """
    The purpose of this function is to plot the RT60 plots of the sound file

    Parameters: (str) File path, (str) root

    Returns: None
    """

    pass

# Extra Credit
def combine_plots(file_path, root):
    """
    The purpose of this function is to combine all of the plots into one plot

    Parameters: (str) File path, (str) root

    Returns: None
    """

    pass