import numpy as np
import matplotlib.pyplot as plt

def mixer(signals):
    mixed_signal = np.zeros(1000)
    for signal in signals:
        mixed_signal += signal[1]
    return mixed_signal
    

# Parameters
sampling_rate = 1000  # samples per second
duration = 1.0  # seconds

# Time axis
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# Generate Signal 1: 5 Hz, amplitude 1
freq1 = 5  # Hz
amplitude1 = 1
signal1 = amplitude1 * np.sin(2 * np.pi * freq1 * t)
one = [t, signal1]

# Generate Signal 2: 10 Hz, amplitude 0.5
freq2 = 10  # Hz
amplitude2 = 0.5
signal2 = amplitude2 * np.sin(2 * np.pi * freq2 * t)
two = [t, signal2]

# Generate Signal 3: 15 Hz, amplitude 2
freq3 = 15  # Hz
amplitude3 = 2
signal3 = amplitude3 * np.sin(2 * np.pi * freq3 * t)
three = [t, signal3]

# Composite Signal by adding Signal 1 and Signal 2 ....
composite_signal = mixer([one, two, three])

# Plot the signals
plt.figure(figsize=(12, 8))

# Plot Signal 1
plt.subplot(4, 1, 1)
plt.plot(t, signal1, label='Signal 1 (5 Hz, Amplitude 1)')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot Signal 2
plt.subplot(4, 1, 2)
plt.plot(t, signal2, label='Signal 2 (10 Hz, Amplitude 0.5)')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot Signal 3
plt.subplot(4, 1, 3)
plt.plot(t, signal3, label='Signal 2 (15 Hz, Amplitude 2)')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

# Plot Composite Signal
plt.subplot(4, 1, 4)
plt.plot(t, composite_signal, label='Composite Signal (5 Hz + 10 Hz + 15 Hz)')
plt.legend()
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")

plt.tight_layout()
plt.show()
