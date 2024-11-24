import numpy as np
import wave
import scipy.io.wavfile as wav


def read_audio(file_path):
    """
    Reads a .wav audio file and converts it into an array.

    Parameters:
        file_path (str): Path to the audio file.

    Returns:
        tuple: Sample rate (int) and audio data (np.ndarray).
    """
    # Read the audio file
    sample_rate, audio_data = wav.read(file_path)

    # If stereo, take one channel
    if audio_data.ndim > 1:
        audio_data = audio_data[:, 0]

    return sample_rate, audio_data


def compute_highest_resonance(audio_data):
    """
    Computes the highest resonance value (maximum amplitude) from audio data.

    Parameters:
        audio_data (np.ndarray): Audio data array.

    Returns:
        float: Maximum amplitude value in the audio data.
    """
    max_value = np.max(np.abs(audio_data))
    return max_value


if __name__ == "__main__":
    # Input: Path to the audio file
    file_path = input("Enter the path to your .wav audio file: ")

    try:
        sample_rate, audio_data = read_audio(file_path)
        max_resonance = compute_highest_resonance(audio_data)
        print(f"The highest resonance value (maximum amplitude) is: {max_resonance}")
    except Exception as e:
        print(f"Error: {e}")
