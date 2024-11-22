# import matplotlib.pyplot as plt
# import numpy as np
# import wave
# import sys
#
# wav = wave.open("SPIDAM_1.wav", "r")
#
# raw = wav.readframes(-1)
# raw = np.frombuffer(raw, "int16")
#
# if wav.getnchannels() == 2:
#     print("Please use a mono file.")
#     sys.exit()
#
# sample_rate = wav.getframerate()
#
# time = np.linspace(0, len(raw) / sample_rate, num=len(raw))
#
# plt.figure(figsize=(10, 4))
# plt.title("Waveform of Wave File")
# plt.plot(raw, color="blue")
#
# plt.ylabel("Amplitude")
# plt.xlabel("Time")
#
# plt.show()
