# controller.py

from tkinter import *
from tkinter import filedialog
from view import *
from scipy.io import wavfile

import soundfile as sf
import tkinter as tk
import os

def set_gui(root):

    file_path = None

    file_name_label = Label(root, text = "No File", fg = "grey")
    file_name_label.place(x = 400, y = 50)


    # Display duration and frequency
    duration_label = Label(root, text="Duration: N/A")
    duration_label.place(x=650, y=500)

    frequency_label = Label(root, text="Peak Frequency: N/A")
    frequency_label.place(x=650, y=550)

    def load_file():

        """
        This function loads and checks if a file is in .wav format. If not in .wav format, the file is sent
        to convert_to_wav()

        Parameters: None

        Returns: None
        """

        # Takes the file_path variable from outside the scope
        nonlocal file_path

        # Looks for file with audio file format
        file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])

        if file_path:
            try:
                file_name_label.config(text = f"File: {os.path.basename(file_path)}", fg = "green")
                # Checks if file ends in .wav, if not, converts the file to .wav format
                if not file_path.endswith('.wav'):
                    new_file_path = convert_to_wav(file_path)
                    messagebox.showinfo("Successfully Converted", f"Converted file saved: {new_file_path}")
                else:
                    messagebox.showinfo("Alert!", "File is already in .wav format")
                # Update duration and frequency labels
                update_duration(file_path)
                update_max_frequency(file_path)
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            except FileNotFoundError:
                messagebox.showinfo("Alert!", "File not found. Please select file.")
            except (ValueError, TypeError, RuntimeError) as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            file_name_label.config(text = "No File", fg = "grey")
    def convert_to_wav(file_path):

        """
        The purpose of this function is to convert an audio file into a .wav file

        Parameters (str): File path (not in .wav format)

        Returns: (str) new_file_path
        """

        y, sample_rate = librosa.load(file_path, sr=None, mono=True)
        new_file_path = os.path.splitext(file_path)[0] + '.wav'
        sf.write(new_file_path, y, sample_rate)

        print("File Converted Successfully!")

        return new_file_path
    def update_duration(file_path):
        """
        Updates the duration of the loaded .wav file.
        """
        sample_rate, data = wavfile.read(file_path)
        duration = len(data) / sample_rate
        duration_label.config(text=f"Duration: {duration:.2f} seconds")
    def update_max_frequency(file_path):
        """
        Updates the peak frequency of the loaded .wav file.
        """
        sample_rate, data = wavfile.read(file_path)
        fft_data = np.abs(np.fft.rfft(data))
        freqs = np.fft.rfftfreq(len(data), 1 / sample_rate)
        peak_freq = freqs[np.argmax(fft_data)]
        frequency_label.config(text=f"Peak Frequency: {peak_freq:.2f} Hz")

    # GUI load file button
    load_file_button = Button(root, text="Load file", command = load_file)  # Add command=load
    load_file_button.place(x=330, y=50)

    """
    Intensity graph, Wave graph, and Alternate plots buttons next to each other
    """

    # Intensity graph button setup
    intensity_graph_button = Button(root, text="Intensity graph", command = lambda: intensity_plot(file_path, root))
    intensity_graph_button.place(x=350, y=500)

    # Wave graph button setup
    wave_graph_button = Button(root, text="Wave graph", command=lambda: base_plot(file_path, root))
    wave_graph_button.place(x=500, y=500)

    # Alternate plot button set up
    alternate_plots_button = Button(root, text="Alternate plots", command = lambda: RT60_plot)  # Add command=alternate_plots
    alternate_plots_button.place(x=800, y=500)

    # Combine plots button below Alternate plots buttons
    combine_plots_button = Button(root, text="Combine plots", command = lambda: combine_plots)  # Add command=combine for extra credit
    combine_plots_button.place(x=950, y=500)

    return root