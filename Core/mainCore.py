import sys
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from scipy.fft import fft, fftfreq
from scipy.interpolate import CubicSpline

class DataLoader:

    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        try:
            self.data = pd.read_csv(self.file_path)

            self.data.dropna(how='all', inplace=True)

            self.data = self.data.apply(pd.to_numeric, errors='coerce')

            print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_data(self):
        return self.data.to_numpy()[:1000]


def sinc_interp(sample_points, sample_values, interpolated_points):
    time_diff = sample_points[1] - sample_points[0] + 1e-9
    return np.array([np.sum(sample_values * np.sinc((t_i - sample_points) / time_diff)) for t_i in interpolated_points])


def linear_interp(sample_points, sample_values, interpolated_points):
    return np.interp(interpolated_points, sample_points, sample_values)


def zoh_reconstruction(sample_points, sample_values, interpolated_points):
    reconstructed_signal = np.zeros_like(interpolated_points)

    for i in range(len(sample_points) - 1):
        mask = (interpolated_points >= sample_points[i]) & (interpolated_points < sample_points[i + 1])
        reconstructed_signal[mask] = sample_values[i]

    reconstructed_signal[interpolated_points >= sample_points[-1]] = sample_values[-1]

    return reconstructed_signal


def cubic_spline_interp(sample_points, sample_values, interpolated_points):
    cubic_spline = CubicSpline(sample_points, sample_values)

    reconstructed_signal = cubic_spline(interpolated_points)

    return reconstructed_signal



def sample_and_reconstruct(time, signal, sampling_rate, interp_method):
    sample_indices = np.linspace(0, len(time) - 1, int(sampling_rate * time[-1]) ).astype(int)
    sampled_time = time[sample_indices]
    sampled_signal = signal[sample_indices]
    reconstructed_signal = interp_method(sampled_time, sampled_signal, time)
    return sampled_time, sampled_signal, reconstructed_signal


# def sample_and_reconstruct(time, signal, sampling_rate, interp_method):
#     sampled_time = []
#     sampled_signal = []
#     for startpoint in range(0, len(time), 500):
#         endpoint = min(startpoint + 500, len(time))
#         sample_indices = np.linspace(startpoint, endpoint - 1, sampling_rate).astype(int)
#         # Collect sampled data for the current segment
#         sampled_time.extend(time[sample_indices])
#         sampled_signal.extend(signal[sample_indices])


def calculate_difference(original_signal, reconstructed_signal):

    return np.abs(original_signal - reconstructed_signal)


# def sinc_interp(sample_points, sample_values, interpolated_points):
#     time_diff = sample_points[1] - sample_points[0] + 1e-9
#     return np.array([np.sum(sample_values * np.sinc((t_i - sample_points) / time_diff)) for t_i in interpolated_points])
#
# def linear_interp(sample_points, sample_values, interpolated_points):
#     return np.interp(interpolated_points, sample_points, sample_values)
#
# def zoh_reconstruction(sample_points, sample_values, interpolated_points):
#
#     reconstructed_signal = np.zeros_like(interpolated_points)
#
#     for i in range(len(sample_points) - 1):
#
#         mask = (interpolated_points >= sample_points[i]) & (interpolated_points < sample_points[i + 1])
#         reconstructed_signal[mask] = sample_values[i]
#
#     reconstructed_signal[interpolated_points >= sample_points[-1]] = sample_values[-1]
#
#     return reconstructed_signal
#
#
# def cubic_spline_interp(sample_points, sample_values, interpolated_points):
#
#     cubic_spline = CubicSpline(sample_points, sample_values)
#
#     reconstructed_signal = cubic_spline(interpolated_points)
#
#     return reconstructed_signal
#
# def sample_and_reconstruct(time, signal, sampling_rate, interp_method):
#     sample_indices = np.linspace(0, len(time) - 1, sampling_rate).astype(int)
#     sampled_time = time[sample_indices]
#     sampled_signal = signal[sample_indices]
#     reconstructed_signal = interp_method(sampled_time, sampled_signal, time)
#     return sampled_time, sampled_signal, reconstructed_signal
#
# def calculate_error(original_signal, reconstructed_signal):
#     return np.abs(original_signal - reconstructed_signal)

def calculate_frequency_domain(signal, time):
    freqs = fftfreq(len(time), time[1] - time[0])
    fft_signal = np.abs(fft(signal))

    # Scale the FFT result
    fft_signal[1:] *= 2
    fft_signal /= len(time)

    return freqs, fft_signal

def calculate_max_frequency(signal, time):
    # Find the Nyquist frequency
    sampling_rate = 1 / (time[1] - time[0])
    max_frequency = sampling_rate / 2
    return max_frequency

class SignalSamplingApp(QtWidgets.QWidget):
    def __init__(self, csv_file_path):
        super().__init__()

        # self.data_loader = DataLoader(csv_file_path)  # Load data from CSV
        # self.signal = self.data_loader.get_data().flatten()  # Flatten to ensure 1D array
        # self.max_time_axis = len(self.signal)
        # self.time = np.linspace(0, self.max_time_axis / 1000, self.max_time_axis)
        self.data_loader = DataLoader(csv_file_path)
        data = self.data_loader.get_data()
        self.time = data[:, 0]
        self.signal = data[:, 1]

        # self.max_time_axis = len(self.signal)
        self.f_max = calculate_max_frequency(self.signal, self.time)
        self.sampling_rate = 2

        self.initUI()
        self.interp_methods = {
            "Whittaker-Shannon (sinc)": sinc_interp,
            "Linear": linear_interp,
            "Zero-Order Hold": zoh_reconstruction,
            "Cubic-Spline":cubic_spline_interp
        }

        self.interp_method = self.interp_methods["Whittaker-Shannon (sinc)"]

        self.update_sampling_slider()
        self.sample_and_reconstruct()

    def initUI(self):
        self.setWindowTitle("Signal Sampling and Recovery")
        self.setGeometry(100, 100, 1200, 800)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)


        self.original_plot = pg.PlotWidget(title="Original Signal")
        self.reconstructed_plot = pg.PlotWidget(title="Reconstructed Signal")
        self.error_plot = pg.PlotWidget(title="Absolute Error (Original - Reconstructed)")
        self.frequency_plot = pg.PlotWidget(title="Frequency Domain")

        layout.addWidget(self.original_plot)
        layout.addWidget(self.reconstructed_plot)
        layout.addWidget(self.error_plot)
        layout.addWidget(self.frequency_plot)

        control_panel = QtWidgets.QHBoxLayout()
        self.sampling_slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        self.sampling_slider.setMinimum(2)
        self.sampling_slider.setMaximum(int(4 * self.f_max))
        self.sampling_slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.sampling_slider.setTickInterval(1)
        self.sampling_slider.setValue(self.sampling_rate)
        self.sampling_slider.valueChanged.connect(self.update_sampling)

        self.sampling_label = QtWidgets.QLabel(f"Sampling Frequency: {self.sampling_rate}")
        control_panel.addWidget(self.sampling_slider)
        control_panel.addWidget(self.sampling_label)
        layout.addLayout(control_panel)

        reconstruction_layout = QtWidgets.QHBoxLayout()
        self.reconstruction_method_label = QtWidgets.QLabel("Reconstruction Method: ")
        reconstruction_layout.addWidget(self.reconstruction_method_label)

        self.reconstruction_method_comboBox = QtWidgets.QComboBox(self)
        self.reconstruction_method_comboBox.addItems(
            ["Whittaker-Shannon (sinc)", "Linear","Zero-Order Hold"," Cubic-Spline"])
        self.reconstruction_method_comboBox.currentTextChanged.connect(self.update_reconstruction_method)

        reconstruction_layout.addWidget(self.reconstruction_method_comboBox)
        control_panel.addLayout(reconstruction_layout)

        layout.addLayout(control_panel)

    def update_sampling_slider(self):
        self.sampling_slider.setMaximum(int((4 * self.f_max)))
        self.sampling_slider.setTickInterval(int(self.f_max))
        self.sampling_slider.setValue(min(self.sampling_rate, 4 * self.f_max))
        self.sampling_label.setText(f"Sampling Frequency: {self.sampling_slider.value()}")

    def update_sampling(self):
        self.sampling_rate = self.sampling_slider.value()
        normalized_frequency = self.sampling_rate / self.f_max  # Normalized frequency calculation
        self.sampling_label.setText(
            f"Sampling Frequency: {self.sampling_rate} (Normalized: {normalized_frequency:.2f})")
        self.sample_and_reconstruct()

    def update_reconstruction_method(self, method_name):
        self.interp_method = self.interp_methods[method_name]
        self.sample_and_reconstruct()

    def sample_and_reconstruct(self):
        sampled_time, sampled_signal, reconstructed_signal = sample_and_reconstruct(
            self.time, self.signal, self.sampling_rate, self.interp_method)

        self.update_plots(sampled_time, sampled_signal, reconstructed_signal)

    def update_plots(self, sampled_time=None, sampled_signal=None, reconstructed_signal=None):
        self.original_plot.clear()
        self.reconstructed_plot.clear()
        self.error_plot.clear()
        self.frequency_plot.clear()


        self.original_plot.plot(self.time, self.signal, pen='#007AFF', name="Original Signal")
        if sampled_time is not None and sampled_signal is not None:
            self.original_plot.plot(sampled_time, sampled_signal, pen=None, symbol='o', symbolBrush='r',
                                    size=5)  # Adjust size


        if reconstructed_signal is not None:
            self.reconstructed_plot.plot(self.time, reconstructed_signal, pen='#007AFF')

            error = calculate_difference(self.signal, reconstructed_signal)
            self.error_plot.plot(self.time, error, pen='#FF0000')

            freqs_original, fft_original = calculate_frequency_domain(self.signal, self.time)
            freqs_reconstructed, fft_reconstructed = calculate_frequency_domain(reconstructed_signal, self.time)

            self.frequency_plot.plot(freqs_original[:len(freqs_original) // 2], fft_original[:len(freqs_original) // 2],
                                     pen='#007AFF')
            self.frequency_plot.plot(freqs_reconstructed[:len(freqs_reconstructed) // 2],
                                     fft_reconstructed[:len(freqs_reconstructed) // 2], pen=pg.mkPen('r', width=5))

        self.original_plot.setXRange(self.time[0], self.time[-1])
        self.original_plot.setYRange(np.min(self.signal), np.max(self.signal))
        self.reconstructed_plot.setXRange(self.time[0], self.time[-1])
        self.reconstructed_plot.setYRange(np.min(self.signal), np.max(self.signal))

        self.error_plot.setXRange(self.time[0], self.time[-1])
        self.error_plot.setYRange(0, np.max(error))

        self.frequency_plot.setXRange(0, (1 / (self.time[1] - self.time[0])) / 2)
        self.frequency_plot.setYRange(0, np.max([fft_original, fft_reconstructed]).max())

    def main(self):
        self.show()


if __name__ == '__main__':
    csv_file_path = '../signals_data/EEG_Abnormal.csv'  # Specify the path to your CSV file
    app = QtWidgets.QApplication(sys.argv)
    window = SignalSamplingApp(csv_file_path)
    window.main()
    sys.exit(app.exec_())
