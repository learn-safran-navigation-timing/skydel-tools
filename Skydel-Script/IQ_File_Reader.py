import scipy
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt
import struct
import math
from scipy import signal
from PyQt5 import QtWidgets, QtGui, QtCore

rng = np.random.default_rng()
np.random.seed(1234)

# Initial parameters
L1 = 1575.42e6
speed_light = 299792458
LAM = speed_light / L1
Nblock = 500  # blocks to analyse
Fs = 25e6  # sample frequency
W = 1 * 1e3  # frequency resolution
offset = 200 * Fs / 1000 * 4  # bytes to skip

# offset = 8 * 1000 * Fs / 1000 * 4; % bytes to skip
N = 64  # itterations for spectrum average
new_off = 0

# Block length
Nsamples = 201 * round(Fs / W)
dt = np.int16
f = -0.518e3

# Specify files to open
file = "iq_file_2.iq"
fid1 = open(file, 'rb')
fid1.seek(int(offset))


def abs2(x):
    return x.real ** 2 + x.imag ** 2


# converting x and y into complex number

""" ************************** Specify file to open *********************** """
file1 = "Path/Your_IQ_file"
fid1 = open(file1, 'rb')
fid1.seek(int(offset))

t = list()
for o in np.arange(0, 0.001, Fs / 1000):
    t.append(o)

# Read I/Q data in int16 format
dataIQ_16_1 = np.fromfile(fid1, dt, count=Nsamples * 2, offset=new_off)

# Convert to complex double
I1 = dataIQ_16_1[::2]
Q1 = dataIQ_16_1[1::2]
data_complex_1 = list()

for j in range(len(I1)):
    i = I1[j]
    q = Q1[j]
    compl = complex(i, q)
    data_complex_1.append(complex(i, q))  # with open(file1, "r") as fid1:

# Construct a Welch spectrum object.
signal_f, signal_psd = scipy.signal.welch(data_complex_1, Fs, window='hamming', scaling='spectrum',
                                          return_onesided=False, axis=-1)
signal_f = np.fft.fftshift(signal_f)
signal_psd = np.fft.fftshift(signal_psd)

plt.figure(0)
plt.semilogy(signal_f, signal_psd, label='PSD')
plt.title("Welch spectrum")
plt.xlabel("Frequency [Hz]")
plt.ylabel("Power [dB]")
plt.grid(True)

# PSD sig 1
PSD = (np.abs(np.fft.fft(data_complex_1)) / N) ** 2
PSD_log = 10.0 * np.log10(PSD)
PSD_shifted = np.fft.fftshift(PSD_log)

f = np.arange(Fs / -2.0, Fs / 2.0, Fs / Nsamples)  # start, stop, step

plt.figure(1)
plt.title("Spectral density [PSD]")
plt.plot(f, PSD_shifted)
plt.xlabel("Frequency [Hz]")
plt.ylabel("Magnitude [dB]")
plt.grid(True)
plt.show()