import sys
import numpy as np
import pandas as pd
from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg
from scipy.fft import fft, fftfreq
from scipy.interpolate import CubicSpline

class DataLoader:
    """Class to load data from a CSV file."""

    def __init__(self, file_path):
        """Initialize with the path to the CSV file."""
        self.file_path = file_path
        self.data = None
        self.load_data()

    def load_data(self):
        """Load data from the CSV file into a DataFrame."""
        try:
            # Load the CSV file, assuming headers
            self.data = pd.read_csv(self.file_path)

            # Drop rows where all columns are NaN (if any)
            self.data.dropna(how='all', inplace=True)

            # Convert data to numeric, coercing errors to NaN
            self.data = self.data.apply(pd.to_numeric, errors='coerce')

            # print("Data loaded successfully.")
        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_data(self):
        """Return the first 1000 points of the loaded data as a NumPy array."""
        return self.data.to_numpy()[:1000]


def sinc_interp(sample_points, sample_values, interpolated_points):
    time_diff = sample_points[1] - sample_points[0] + 1e-9
    return np.array([np.sum(sample_values * np.sinc((t_i - sample_points) / time_diff)) for t_i in interpolated_points])

def linear_interp(sample_points, sample_values, interpolated_points):
    return np.interp(interpolated_points, sample_points, sample_values)

def zoh_reconstruction(sample_points, sample_values, interpolated_points):

    reconstructed_signal = np.zeros_like(interpolated_points)
    
    # Loop through each interval and hold the last sample value constant until the next sampled point
    for i in range(len(sample_points) - 1):
        
        mask = (interpolated_points >= sample_points[i]) & (interpolated_points < sample_points[i + 1])
        reconstructed_signal[mask] = sample_values[i]

    reconstructed_signal[interpolated_points >= sample_points[-1]] = sample_values[-1]
    
    return reconstructed_signal


def cubic_spline_interp(sample_points, sample_values, interpolated_points):
        
    cubic_spline = CubicSpline(sample_points, sample_values)
    
    # Evaluate the spline over the full time range
    reconstructed_signal = cubic_spline(interpolated_points)
    
    return reconstructed_signal

def sample_and_reconstruct(time, signal, sampling_rate, interp_method):
    sample_indices = np.linspace(0, len(time) - 1, sampling_rate).astype(int)
    sampled_time = time[sample_indices]
    sampled_signal = signal[sample_indices]
    reconstructed_signal = interp_method(sampled_time, sampled_signal, time)
    return sampled_time, sampled_signal, reconstructed_signal

def calculate_error(original_signal, reconstructed_signal):
    """Calculate the absolute error between the original and reconstructed signals."""
    return np.abs(original_signal - reconstructed_signal)

def calculate_frequency_domain(signal, time):
    """Calculate the frequency domain representation of the given signal."""
    freqs = fftfreq(len(time), time[1] - time[0])
    fft_signal = np.abs(fft(signal))

    # Scale the FFT result
    fft_signal[1:] *= 2
    fft_signal /= len(time)

    return freqs, fft_signal

def calculate_max_frequency(signal, time):
    """Calculate the maximum frequency of the signal."""
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
        # self.time = np.linspace(0, self.max_time_axis / 1000, self.max_time_axis)  # Assuming a sample rate of 1000Hz
        self.data_loader = DataLoader(csv_file_path)  # Load data from CSV
        data = self.data_loader.get_data()  # Get the loaded data as a NumPy array
        self.time = data[:, 0]  # Extract the first column as time
        self.signal = data[:, 1]  # Extract the second column as amplitude

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

        # Create plots
        self.original_plot = pg.PlotWidget(title="Original Signal")
        self.reconstructed_plot = pg.PlotWidget(title="Reconstructed Signal")
        self.error_plot = pg.PlotWidget(title="Absolute Error (Original - Reconstructed)")
        self.frequency_plot = pg.PlotWidget(title="Frequency Domain")

        # Add plots vertically
        layout.addWidget(self.original_plot)
        layout.addWidget(self.reconstructed_plot)
        layout.addWidget(self.error_plot)
        layout.addWidget(self.frequency_plot)

        # Slider for sampling
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

        # Reconstruction method selection
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
        """Reconfigure the sampling slider based on the current f_max."""
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
        """Update the interpolation method based on user selection."""
        self.interp_method = self.interp_methods[method_name]  # Set to the actual function
        self.sample_and_reconstruct()  # Call to update the signal with the new method

    def sample_and_reconstruct(self):
        sampled_time, sampled_signal, reconstructed_signal = sample_and_reconstruct(
            self.time, self.signal, self.sampling_rate, self.interp_method)

        self.update_plots(sampled_time, sampled_signal, reconstructed_signal)

    def update_plots(self, sampled_time=None, sampled_signal=None, reconstructed_signal=None):
        self.original_plot.clear()
        self.reconstructed_plot.clear()
        self.error_plot.clear()
        self.frequency_plot.clear()

        # Plot original signal
        self.original_plot.plot(self.time, self.signal, pen='#007AFF', name="Original Signal")
        if sampled_time is not None and sampled_signal is not None:
            self.original_plot.plot(sampled_time, sampled_signal, pen=None, symbol='o', symbolBrush='r',
                                    size=5)  # Adjust size

        # Plot reconstructed signal
        if reconstructed_signal is not None:
            self.reconstructed_plot.plot(self.time, reconstructed_signal, pen='#007AFF')

            # Calculate and plot absolute error
            error = calculate_error(self.signal, reconstructed_signal)  # Calculate absolute error
            self.error_plot.plot(self.time, error, pen='#FF0000')  # Plot absolute error in red

            # Frequency domain plot for original and reconstructed signals
            freqs_original, fft_original = calculate_frequency_domain(self.signal, self.time)
            freqs_reconstructed, fft_reconstructed = calculate_frequency_domain(reconstructed_signal, self.time)

            self.frequency_plot.plot(freqs_original[:len(freqs_original) // 2], fft_original[:len(freqs_original) // 2],
                                     pen='#007AFF')
            self.frequency_plot.plot(freqs_reconstructed[:len(freqs_reconstructed) // 2],
                                     fft_reconstructed[:len(freqs_reconstructed) // 2], pen=pg.mkPen('r', width=5))

        # Set view range for original and reconstructed plots
        self.original_plot.setXRange(self.time[0], self.time[-1])
        self.original_plot.setYRange(np.min(self.signal), np.max(self.signal))
        self.reconstructed_plot.setXRange(self.time[0], self.time[-1])
        self.reconstructed_plot.setYRange(np.min(self.signal), np.max(self.signal))

        # Set view range for error plot
        self.error_plot.setXRange(self.time[0], self.time[-1])
        self.error_plot.setYRange(0, np.max(error))

        # Set view range for frequency plot
        self.frequency_plot.setXRange(0, (1 / (self.time[1] - self.time[0])) / 2)  # Nyquist frequency
        self.frequency_plot.setYRange(0, np.max([fft_original, fft_reconstructed]).max())  # Set to max of both signals

    def main(self):
        self.show()


if __name__ == '__main__':
    csv_file_path = '../signals_data/EEG_Abnormal.csv'  # Specify the path to your CSV file
    app = QtWidgets.QApplication(sys.argv)
    window = SignalSamplingApp(csv_file_path)
    window.main()
    sys.exit(app.exec_())
