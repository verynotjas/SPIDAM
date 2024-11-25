# view.py
# This file displays the plots

import numpy as np
import wave
import librosa
import librosa.display

from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def base_plot(file_path, root):
    """
    The purpose of this function is to display the audio file into waveform in the GUI

    Parameters (str): File path

    Returns: None
    """

    try:
        wav = wave.open(file_path, "r")
        raw = wav.readframes(-1)
        raw = np.frombuffer(raw, dtype="int16")

        if wav.getnchannels() != 1:
            messagebox.showerror("Error", "Please use a mono file.")
            return

        sample_rate = wav.getframerate()
        time = np.linspace(0, len(raw) / sample_rate, num=len(raw))

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, raw, color="blue")
        ax.set_title("Waveform of Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {e}")

def intensity_plot(file_path, root):
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
        canvas.get_tk_widget().place(x=500, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting intensity: {e}")


def RT60_plot(file_path, root):
    try:
        y, sr = librosa.load(file_path, sr=None)
        onset_env = librosa.onset.onset_strength(y, sr=sr)
        rt60 = librosa.time_frequency.autocorr_to_bpm(onset_env)

        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(rt60)
        ax.set_title("RT60 Plot")
        ax.set_xlabel("Frequency (Hz)")
        ax.set_ylabel("RT60 (s)")

        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().place(x=500, y=90)

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting RT60: {e}")

def combine_plots(file_path, root):
    pass