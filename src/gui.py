from tkinter import *
from tkinter import messagebox, filedialog

import librosa
import soundfile as sf
import os
import numpy as np
import wave

# from PIL._tkinter_finder import tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def load_file():

    """
    This function loads and checks if a file is in .wav format. If not in .wav format, the file is sent
    to convert_to_wav()

    Parameters: None

    Returns: None
    """

    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
    if file_path:
        try:
            if not file_path.endswith('.wav'):
                new_file_path = convert_to_wav(file_path)
                messagebox.showinfo("Successfully Converted", f"Converted file saved: {new_file_path}")
                display_wave(new_file_path)
            else:
                messagebox.showinfo("Alert!", "File is already in .wav format")
                display_wave(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def convert_to_wav(file_path):

    """
    The purpose of this function is to convert an audio file into a .wav file

    Parameters: File path (not in .wav format)

    Returns: The new file path (in .wav format)
    """

    y, sr = librosa.load(file_path, sr=None, mono=True)
    new_file_path = os.path.splitext(file_path)[0] + '.wav'
    sf.write(new_file_path, y, sr)
    print("File Converted Successfully!")
    return new_file_path

def display_wave(file_path):

    """
    The purpose of this function is to display the audio file into waveform in the GUI

    Parameters: File path

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
        canvas.get_tk_widget().place(x = 500, y = 90)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {e}")

# GUI base setup

root = Tk()
root.title("Sound Wave Analysis")
root.geometry("1800x800")

# GUI load file button
load_file_button = Button(root, text="Load file", command = load_file)  # Add command=load if needed
load_file_button.place(x=900, y=50)

# Intensity graph, Wave graph, and Alternate plots buttons next to each other

# Intensity graph button setup
intensity_graph_button = Button(root, text="Intensity graph")
intensity_graph_button.place(x=780, y=500)

# Wave graph button setup
wave_graph_button = Button(root, text="Wave graph")
wave_graph_button.place(x=900, y=500)

# Alternate plot button set up
alternate_plots_button = Button(root, text="Alternate plots")  # Add command=combine if needed
alternate_plots_button.place(x=1000, y=500)


# Combine plots button below Alternate plots buttons
combine_plots_button = Button(root, text="Combine plots")  # Add command=alternate_plots for extra credit
combine_plots_button.place(x=1000, y=550)

# Run the main loop
root.mainloop()