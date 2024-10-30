import numpy as np
import matplotlib.pyplot as plt
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Core.Data_load import DataLoader
from PyQt5 import QtWidgets, QtCore
import json
from scipy.signal import square

def mixer(signal, amp, freq, signal_type = 'sin'):
    sampling_rate = len(signal[:, 1])  # samples per second
    duration = 1.0  # seconds
    dummy_time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    if signal_type == 'sin':
        mixed_component = amp * np.sin(2 * np.pi * freq * dummy_time)
    elif signal_type == 'cos':
        mixed_component = amp * np.cos(2 * np.pi * freq * dummy_time)
    elif signal_type == 'square':
        mixed_component = amp * square(2 * np.pi * freq * dummy_time)
    elif signal_type == "triangular":
        mixed_component = amp * (2 * np.abs((dummy_time * freq) % 1 - 0.5) - 1)
    else:
        raise ValueError("Unsupported signal type")

    # save_data({'amplitude': amp, 'frequency': freq, 'type': type}) #interrupting the addition

    return signal[:, 1] + mixed_component

def remove_elements(signal, amp, freq, signal_type = 'sin'):
    sampling_rate = len(signal[:, 1])  # samples per second
    duration = 1.0  # seconds
    dummy_time = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    if signal_type == 'sin':
        mixed_component = amp * np.sin(2 * np.pi * freq * dummy_time)
    elif signal_type == 'cos':
        mixed_component = amp * np.cos(2 * np.pi * freq * dummy_time)
    elif signal_type == 'square':
        mixed_component = amp * square(2 * np.pi * freq * dummy_time)
    elif signal_type == "triangular":
        mixed_component = amp * (2 * np.abs((dummy_time * freq) % 1 - 0.5) - 1)
    else:
        raise ValueError("Unsupported signal type")

    return signal[:, 1] - mixed_component

# # Define the popup window class
# class MixerInputPopup(QtWidgets.QDialog):
#     def __init__(self, signal, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.signal = signal  # The signal data passed to the popup

#         # Set up the window
#         self.setWindowTitle("Mixer Input")
#         self.setFixedSize(300, 150)

#         # Create layout
#         layout = QtWidgets.QVBoxLayout()

#         # Amplitude input
#         self.amp_label = QtWidgets.QLabel("Amplitude:")
#         self.amp_input = QtWidgets.QLineEdit()
#         layout.addWidget(self.amp_label)
#         layout.addWidget(self.amp_input)

#         # Frequency input
#         self.freq_label = QtWidgets.QLabel("Frequency:")
#         self.freq_input = QtWidgets.QLineEdit()
#         layout.addWidget(self.freq_label)
#         layout.addWidget(self.freq_input)

#         # Submit button
#         self.submit_button = QtWidgets.QPushButton("Mix Signal")
#         self.submit_button.clicked.connect(self.submit_values)
#         layout.addWidget(self.submit_button)

#         self.setLayout(layout)

#     def submit_values(self):
#         # try:
#             # Retrieve amplitude and frequency from input fields
#             amp = float(self.amp_input.text())
#             freq = float(self.freq_input.text())

#             # Call the mixer function with provided amp and freq
#             mixed_signal = mixer(self.signal, amp, freq)
#             # print(self.signal[:, 0])
#             new_signal = remove_elements([self.signal[:, 0], mixed_signal], amp, freq)

#             # Plot the signals
#             plt.figure(figsize=(12, 8))
#             plt.subplot(2, 1, 1)
#             plt.plot(self.signal[:, 0], mixed_signal, label='Composite Signal')
#             plt.legend()
#             plt.xlabel("Time [s]")
#             plt.ylabel("Amplitude")
            
#             plt.subplot(2, 1, 2)
#             plt.plot(self.signal[:, 0], new_signal, label='Simple Signal')
#             plt.legend()
#             plt.xlabel("Time [s]")
#             plt.ylabel("Amplitude")

#             plt.tight_layout()
#             plt.show()
#             # Close the dialog after submission
#             self.accept()

#         # except ValueError:
#         #     # Show error message if conversion fails
#         #     error_dialog = QtWidgets.QMessageBox()
#         #     error_dialog.setText("Please enter valid numeric values for amplitude and frequency.")
#         #     error_dialog.exec_()



# # Main Application
# app = QtWidgets.QApplication(sys.argv)

# # Example signal for testing
# ecg = DataLoader('Signal-Reconstructor/signals_data/ECG_Normal.csv').get_data()

# # Create and show the mixer input popup
# popup = MixerInputPopup(ecg)
# popup.exec_()

# sys.exit(app.exec_())

