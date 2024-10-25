import numpy as np
import matplotlib.pyplot as plt
from Data_load import DataLoader
from PyQt5 import QtWidgets, QtCore
import sys
import json


def mixer(signal, amp, freq):
    sampling_rate = len(signal[:, 1])  # samples per second
    duration = 1.0  # seconds
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin = amp * np.sin(2 * np.pi * freq * t)
    print(len(signal[:, 1]))

    mixed_signal = sin + signal[:, 1]

    return mixed_signal

def remove_elements(signal, amp, freq):
    sampling_rate = len(signal)  # samples per second
    duration = 1.0  # seconds
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin = amp * np.sin(2 * np.pi * freq * t)

    new_signal = signal - sin

    return new_signal


def save_data(data, filename="sinData.json"):
    with open(filename, 'w') as file:
        json.dump(data, file)

def load_data(filename="sinData.json"):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Define the popup window class
class MixerInputPopup(QtWidgets.QDialog):
    def __init__(self, signal, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.signal = signal  # The signal data passed to the popup

        # Set up the window
        self.setWindowTitle("Mixer Input")
        self.setFixedSize(300, 150)

        # Create layout
        layout = QtWidgets.QVBoxLayout()

        # Amplitude input
        self.amp_label = QtWidgets.QLabel("Amplitude:")
        self.amp_input = QtWidgets.QLineEdit()
        layout.addWidget(self.amp_label)
        layout.addWidget(self.amp_input)

        # Frequency input
        self.freq_label = QtWidgets.QLabel("Frequency:")
        self.freq_input = QtWidgets.QLineEdit()
        layout.addWidget(self.freq_label)
        layout.addWidget(self.freq_input)

        # Submit button
        self.submit_button = QtWidgets.QPushButton("Mix Signal")
        self.submit_button.clicked.connect(self.submit_values)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_values(self):
        try:
            # Retrieve amplitude and frequency from input fields
            amp = float(self.amp_input.text())
            freq = float(self.freq_input.text())

            # Call the mixer function with provided amp and freq
            mixed_signal = mixer(self.signal, amp, freq)
            new_signal = remove_elements(mixed_signal, amp, freq)

            save_data({"amplitude": amp, "frequency": freq})
            print(load_data())
            # For demonstration, print the mixed signal length

            # Plot the signals
            plt.figure(figsize=(12, 8))
            plt.subplot(2, 1, 1)
            plt.plot(self.signal[:, 0], mixed_signal, label='Composite Signal')
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")
            
            plt.subplot(2, 1, 2)
            plt.plot(self.signal[:, 0], new_signal, label='Simple Signal')
            plt.legend()
            plt.xlabel("Time [s]")
            plt.ylabel("Amplitude")

            plt.tight_layout()
            plt.show()
            # Close the dialog after submission
            self.accept()

        except ValueError:
            # Show error message if conversion fails
            error_dialog = QtWidgets.QMessageBox()
            error_dialog.setText("Please enter valid numeric values for amplitude and frequency.")
            error_dialog.exec_()



# Main Application
app = QtWidgets.QApplication(sys.argv)

# Example signal for testing
ecg = DataLoader('Signal-Reconstructor\signals_data\EMG_Abnormal.csv').get_data()

# Create and show the mixer input popup
popup = MixerInputPopup(ecg)
popup.exec_()

sys.exit(app.exec_())

