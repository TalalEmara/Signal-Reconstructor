import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
import pyqtgraph as pg


def add_noise(data, snrdb):
    signal_power = np.sum(data ** 2)
    Gaussian_noise = np.random.normal(0, 1, len(data))
    noise_power = np.sum(Gaussian_noise ** 2)
    snr = 10 ** (snrdb * 0.1)
    alpha = np.sqrt(signal_power / (snr * noise_power))
    noisy_signal = data + alpha * Gaussian_noise
    return noisy_signal