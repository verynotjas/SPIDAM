import tkinter as tk
from tkinter import filedialog, messagebox
import librosa
import soundfile as sf
import os

def load_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3;*.aac")])
    if file_path:
        try:
            if not file_path.endswith('.wav'):
                new_file_path = convert_to_wav(file_path)
                messagebox.showinfo("Success!!!", f"Converted file is saved as: {new_file_path}")
            else:
                messagebox.showinfo("Alert!", "File is already in .wav format")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

def convert_to_wav(file_path):
    y, sr = librosa.load(file_path, sr=None, mono=True)

    new_file_path = os.path.splitext(file_path)[0] + '.wav'

    sf.write(new_file_path, y, sr)
    print("File Converted")
    return new_file_path

root = tk.Tk()
root.geometry("800x700")
root.title("Interactive Data Acoustic Modeling")
load_button = tk.Button(root, text="Load Audio File", command=load_file)
load_button.pack(pady=20)

root.mainloop()