# controller.py

from tkinter import *
from tkinter import filedialog
from view import *

import soundfile as sf
import os

def set_gui(root):

    file_path = None

    file_name_label = Label(root, text = "No File", fg = "grey")
    file_name_label.place(x = 400, y = 50)

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

        Returns (str): The new file path (in .wav format)
        """

        y, sr = librosa.load(file_path, sr=None, mono=True)
        new_file_path = os.path.splitext(file_path)[0] + '.wav'
        sf.write(new_file_path, y, sr)

        print("File Converted Successfully!")

        return new_file_path

    # GUI load file button
    load_file_button = Button(root, text="Load file", command = load_file)  # Add command=load
    load_file_button.place(x=330, y=50)

    """
    Intensity graph, Wave graph, and Alternate plots buttons next to each other
    """

    # Intensity graph button setup
    intensity_graph_button = Button(root, text="Intensity graph", command = lambda: intensity_plot(file_path, root))
    intensity_graph_button.place(x=580, y=500)

    # Wave graph button setup
    wave_graph_button = Button(root, text="Wave graph", command=lambda: base_plot(file_path, root))
    wave_graph_button.place(x=700, y=500)

    # Alternate plot button set up
    alternate_plots_button = Button(root, text="Alternate plots", command = lambda: RT60_plot)  # Add command=alternate_plots
    alternate_plots_button.place(x=800, y=500)

    # Combine plots button below Alternate plots buttons
    combine_plots_button = Button(root, text="Combine plots", command = lambda: combine_plots)  # Add command=combine for extra credit
    combine_plots_button.place(x=693, y=550)

    return root