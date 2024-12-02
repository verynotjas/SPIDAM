# model.py

import numpy as np
import librosa
import soundfile as sf
import os

from matplotlib import pyplot as plt
from scipy.io import wavfile
from tkinter import messagebox

def remove_metadata(file_path):
    """
    This function checks for metadata in a WAV file, removes it if present,
    and skips rewriting if no metadata is found.

    Parameters: (str) file_path

    Returns: (str) new_file_path, (str) file_path
    """
    try:
        new_file_path = os.path.splitext(file_path)[0] + "_removed_metadata.wav"
        meta_data = False

        with open(file_path, 'rb') as original_file:
            riff_header = original_file.read(12)
            while True:
                chunk_header = original_file.read(8)
                if len(chunk_header) < 8:
                    break

                chunk_id = chunk_header[:4]
                chunk_size = int.from_bytes(chunk_header[4:], 'little')

                if chunk_id not in (b'fmt ', b'data'):
                    meta_data = True
                    break

                original_file.seek(chunk_size, 1)

        if not meta_data:
            return file_path

        with open(file_path, 'rb') as original_file:
            with open(new_file_path, 'wb') as new_file:
                new_file.write(riff_header)

                while True:
                    chunk_header = original_file.read(8)
                    if len(chunk_header) < 8:
                        break

                    chunk_id = chunk_header[:4]
                    chunk_size = int.from_bytes(chunk_header[4:], 'little')
                    chunk_data = original_file.read(chunk_size)

                    if chunk_id in (b'fmt ', b'data'):
                        new_file.write(chunk_header)
                        new_file.write(chunk_data)
                    else:
                        print(f"Skipping metadata chunk: {chunk_id.decode(errors='ignore')}")

        messagebox.showinfo("Success", f"Metadata removed. New file saved as {new_file_path}")
        return new_file_path

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while removing metadata: {e}")
        return file_path

def convert_to_mono(file_path, ofp=None):
    """
    This function converts the input audio file into a mono file

    Parameters: (str) file_path
    Returns: y_mono, (float) sr
    """
    y, sr = librosa.load(file_path, sr=None, mono=False)

    if y.ndim > 1:
        y_mono = y.mean(axis=1)
    else:
        y_mono = y

    if ofp:
        sf.write(ofp, y_mono, sr)
        return None
    else:
        return y_mono, sr

def calculate_rt60(data, freqs, spectrum, t, freq_range):
    """
    This function calculated the low, mid, and high RT60 of the audio

    Parameters: (tuple) freqs, (tuple) spectrum, (tuple) t, (tuple) freq_range
    Returns: (int) rt60, trimmed_t, trimmed_db
    """
    mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
    target_spectrum = np.mean(spectrum[mask], axis=0)

    data_in_db = 10 * np.log10(target_spectrum + 1e-10)

    index_of_max = np.argmax(data_in_db)
    value_of_max = data_in_db[index_of_max]
    value_max_less_5 = value_of_max - 5
    value_max_less_25 = value_of_max - 25

    def find_nearest_value(array, value):
        """
        This function finds the indices for -5 dB and -25 dB

        Parameters: (tuple) array, value
        Return: idx
        """

        idx = (np.abs(array - value)).argmin()
        return idx

    index_less_5 = find_nearest_value(data_in_db[index_of_max:], value_max_less_5) + index_of_max
    index_less_25 = find_nearest_value(data_in_db[index_of_max:], value_max_less_25) + index_of_max

    rt20 = t[index_less_25] - t[index_less_5]
    rt60 = rt20 * 3

    trimmed_t = t[index_less_5:index_less_25 + 1]
    trimmed_db = data_in_db[index_less_5:index_less_25 + 1]

    return rt60, trimmed_t, trimmed_db

def convert_to_wav(file_path):

    """
    The purpose of this function is to convert an audio file into a .wav file

    Parameters (str): File path (not in .wav format)

    Return: (str) new_file_path
    """

    y, sr = librosa.load(file_path, sr=None, mono=True)
    new_file_path = os.path.splitext(file_path)[0] + '.wav'
    sf.write(new_file_path, y, sr)

    print("File Converted Successfully!")

    return new_file_path

def calculate_duration(file_path):
    """
    This function is used to calculate the duration of the audio

    Parameter: (str) file_path
    Return: (float) duration
    """
    sr, y = wavfile.read(file_path)
    duration = len(y) / sr
    return duration

def calculate_max_frequency(file_path):
    """
    This function is used to calculate the maximum frequency of the audio

    Parameter: (str) file_path
    Return: max_frequency
    """
    sr, y = wavfile.read(file_path)
    fft_data = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), 1 / sr)
    max_freq = freqs[np.argmax(fft_data)]
    return max_freq

def difference_average(file_path):

    """
    This function calculates the difference average bewteen RT60 values

    Parameter: (str) file_path
    Return: (float) difference_average
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

    return (low_average + mid_average + high_average) / 3