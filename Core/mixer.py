import numpy as np
import matplotlib.pyplot as plt
from Data_load import DataLoader

def mixer(signal, amp, freq):
    sampling_rate = len(signal[:, 1])  # samples per second
    duration = 1.0  # seconds
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    sin = amp * np.sin(2 * np.pi * freq * t)
    print(len(signal[:, 1]))

    mixed_signal = sin + signal[:, 1]

    return mixed_signal

# testing
ecg = DataLoader('Signal-Reconstructor\signals_data\EMG_Abnormal.csv').get_data()

composite_signal = mixer(ecg, 1, 10)

# Plot the signals
plt.figure(figsize=(12, 8))

# Plot Signal 1
plt.subplot(2, 1, 1)
plt.plot(ecg[:, 0], ecg[:, 1], label='Signal 1')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot Composite Signal
plt.subplot(2, 1, 2)
plt.plot(ecg[:, 0], composite_signal, label='Composite Signal')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
