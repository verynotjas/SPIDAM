# controller.py

from tkinter import *
from tkinter import filedialog
from view import *


def set_gui(root):
    """
    The purpose of this function is to set up the GUI

    Parameter: (obj) root
    Return: (obj) root
    """

    file_path = None
    canvas = None

    # Creating the labels and placing them

    file_name_label = Label(root, text = "No File", fg = "grey")
    file_name_label.place(x = 160, y = 53)

    fig = Figure(figsize=(5, 3), dpi = 100)
    ax = fig.add_subplot(111)

    # Creates empty initial plot
    canvas = FigureCanvasTkAgg(fig, master = root)
    canvas.draw()
    canvas.get_tk_widget().place(x = 100, y = 90)

    # Display duration and frequency
    duration_label = Label(root, text="Duration: N/A seconds")
    duration_label.place(x=280, y=400)

    frequency_label = Label(root, text="Peak Frequency: N/A Hz.")
    frequency_label.place(x=280, y=430)

    rt60_difference_label = Label(root, text="RT60 Difference: N/A seconds")
    rt60_difference_label.place(x=280, y=460)

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
                    file_path = new_file_path
                else:
                    messagebox.showinfo("Alert!", "File is already in .wav format")

                file_path = remove_metadata(file_path)

                update_duration(file_path)
                update_max_frequency(file_path)
                rt60_difference_label.config(text = f"RT60 Difference: {difference_average(file_path):.2f} seconds")

            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
            except FileNotFoundError:
                messagebox.showinfo("Alert!", "File not found. Please select file.")
            except (ValueError, TypeError, RuntimeError) as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
        else:
            file_name_label.config(text = "No File", fg = "grey")

    def update_duration(file_path):
        """
        Updates the duration of the loaded .wav file.

        Parameter: (str) file_path
        Return: None
        """

        duration = calculate_duration(file_path)
        duration_label.config(text=f"Duration: {duration:.2f} seconds")

    def update_max_frequency(file_path):
        """
        Updates the max frequency of the loaded .wav file.

        Parameter: (str) file_path
        Return: None
        """
        max_freq = calculate_max_frequency(file_path)
        frequency_label.config(text=f"Peak Frequency: {max_freq:.2f} Hz.")

    #Creating all the buttons and placing them

    # Load file button setup
    load_file_button = Button(root, text="Load file", command = load_file)  # Add command=load
    load_file_button.place(x=100, y=50)

    # Intensity graph button setup
    intensity_graph_button = Button(root, text="Intensity graph", command = lambda: intensity_plot(file_path, root, canvas))
    intensity_graph_button.place(x=100, y=400)

    # Wave graph button setup
    wave_graph_button = Button(root, text="Wave graph", command=lambda: base_plot(file_path, root, canvas))
    wave_graph_button.place(x=200, y=400)

    # Alternate plot button set up
    alternate_plots_button = Button(root, text="Alternate plots", command = lambda: alternate_rt60(file_path, root, canvas))  # Add command=alternate_plots
    alternate_plots_button.place(x=412, y=400)

    # Combine plots button below Alternate plots buttons
    combine_plots_button = Button(root, text="Combine plots", command = lambda: combine_plots(file_path, root, canvas))  # Add command=combine for extra credit
    combine_plots_button.place(x=512, y=400)

    return root