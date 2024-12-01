# Audio Visualization and RT60 Analysis Tool

## Overview
This project is a Python-based application designed to analyze and visualize audio files. It provides multiple features, including plotting waveforms, intensity, and calculating RT60 values for low, mid, and high-frequency bands. Users can view these through a graphical user interface created with Tkinter and Matplotlib. The tool utilizes several scientific calculations and data visualization techniques to address challenges in acoustic analysis by specifically focusing on voice intelligibility issues caused by excessive reverberation in enclosed spaces. It offers an understanding for analyzing and improving sound quality in places such as classrooms, auditoriums, and other large enclosed areas.

## Why It Exists
Voice intelligibility in enclosed spaces is a challenge that  can affect learning, communication, and productivity. Large spaces that are not acoustically managed can create long reverberation times which makes it difficult for people to hear and understand speech clearly. The purpose of this project is to provide an easy-to-use tool for audio analysis and visualization, particularly for those interested in studying reverberation characteristics of sound. By enabling the analysis of reverberation time across low, mid, and high-frequency bands, this tool helps identify and quantify problematic acoustic behaviors for optimizing sound quality and ensuring better voice intelligibility.

## Features
1. **Waveform Visualization**: Displays the amplitude of the audio file over time.
2. **Intensity Spectrogram**: Shows the intensity of the signal across different frequencies over time.
3. **RT60 Analysis**:
   - Low-frequency band (0-250 Hz)
   - Mid-frequency band (250-2000 Hz)
   - High-frequency band (2000-20000 Hz)
4. **Combined Plot**: Displays all RT60 plots on a single graph for comparison.
5. **Interactive GUI**: Allows users to load files and switch between plots easily.

## Requirements
- Python 3.7+
- Required packages (listed in requirements.txt)

## Installation
1. Clone the repository or download the source code.
2. Install the required Python packages:
