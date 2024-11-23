import tkinter as tk
from tkinter import filedialog, messagebox

import librosa
import soundfile as sf
import os
import numpy as np
import wave

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_file():
# Function to load and convert file to .wav format
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
    if file_path:
        try:
            if not file_path.endswith('.wav'):
                new_file_path = convert_to_wav(file_path)
                messagebox.showinfo("Successfully Converted", f"Converted file saved: {new_file_path}")
                display_waveform(new_file_path)
            else:
                messagebox.showinfo("Alert!", "File is already in .wav format")
                display_waveform(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def convert_to_wav(file_path):
# Function to convert non-wav files to wav
    y, sr = librosa.load(file_path, sr=None, mono=True)
    new_file_path = os.path.splitext(file_path)[0] + '.wav'
    sf.write(new_file_path, y, sr)
    print("File Converted Successfully!")
    return new_file_path

def display_waveform(file_path):
# Function to display the waveform in the GUI
    try:
        wav = wave.open(file_path, "r")
        raw = wav.readframes(-1)
        raw = np.frombuffer(raw, dtype="int16")

        if wav.getnchannels() != 1:
            messagebox.showerror("Error", "Please use a mono file.")
            return

        sample_rate = wav.getframerate()
        time = np.linspace(0, len(raw) / sample_rate, num=len(raw))

        # Create figure for the waveform
        fig = Figure(figsize=(8, 4), dpi=100)
        ax = fig.add_subplot(111)
        ax.plot(time, raw, color="blue")
        ax.set_title("Waveform of Audio File")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")

        # Embed the plot into the tkinter window
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(pady=20)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {e}")
# GUI Setup
root = tk.Tk()
root.geometry("800x700")
root.title("Interactive Data Acoustic Modeling")

load_button = tk.Button(root, text="Load Audio File", command=load_file)
load_button.pack(pady=20)

root.mainloop()