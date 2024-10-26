import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider, QLabel
from PyQt5.QtCore import Qt
import pyqtgraph as pg

class Noise(QMainWindow):
    def __init__(self):
        super().__init__()
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        self.plot_widget = pg.PlotWidget(title="Noise")
        self.layout.addWidget(self.plot_widget)
        self.original_curve = self.plot_widget.plot(pen="b", name="Original Signal")
        self.noisy_curve = self.plot_widget.plot(pen="r", name="Noisy Signal")
        self.snr_slider = QSlider(Qt.Horizontal)
        self.snr_slider.setMinimum(0)
        self.snr_slider.setMaximum(30)
        self.snr_slider.setValue(15)
        self.snr_slider.valueChanged.connect(self.update_plot)
        self.layout.addWidget(QLabel("SNR (higher means less noise):"))
        self.layout.addWidget(self.snr_slider)
        self.fs = 500
        self.t = np.linspace(0, 1, self.fs)
        self.ecg_data = self.generate_ecg_signal()
        self.update_plot()
        self.plot_widget.setMouseTracking(True)
        self.plot_widget.getViewBox().setMouseEnabled(x=True, y=True)
        self.plot_widget.getViewBox().setLimits(xMin=0, xMax=1, yMin=-1, yMax=1)

    def generate_ecg_signal(self):
        heart_rate = 75
        frequency = heart_rate / 60
        ecg_signal = 0.6 * np.sin(2 * np.pi * frequency * self.t) + 0.1 * np.random.randn(len(self.t))
        return ecg_signal

    def add_noise(self, dataArray, snrdb):
        signal_power = np.sum(dataArray ** 2)
        Gaussian_noise = np.random.normal(0, 1, len(dataArray))
        noise_power = np.sum(Gaussian_noise ** 2)
        snr = 10 ** (snrdb * 0.1)
        alpha = np.sqrt(signal_power / (snr * noise_power))
        noisy_signal = dataArray + alpha * Gaussian_noise
        return noisy_signal

    def update_plot(self):
        snr_value = self.snr_slider.value()
        noisy_data = self.add_noise(self.ecg_data, snr_value)
        self.original_curve.setData(self.t, self.ecg_data)
        self.noisy_curve.setData(self.t, noisy_data)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Noise()
    window.setWindowTitle("Noise")
    window.setGeometry(100, 100, 800, 600)
    window.show()
    sys.exit(app.exec_())
