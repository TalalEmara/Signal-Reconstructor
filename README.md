## Sampling-Theory Studio

### Introduction
Sampling an analog signal is an essential step in any digital signal processing system. The Nyquist–Shannon sampling theorem guarantees full recovery of the signal when sampled at a frequency greater than or equal to twice the maximum frequency of the signal. This application demonstrates the process of signal sampling and recovery, validating the importance of the Nyquist rate.

![image](https://github.com/user-attachments/assets/b3dd6810-3c56-4457-92e7-4fc5e62df4f9)

### Features
**1. Sample & Recover**
Signal Loading: Load a mid-length signal (approximately 1000 points).
Visualization: Display the original signal with markers for sampled points.
Sampling Frequencies: Sample the signal using different frequencies (displayed as normalized or actual frequencies).
Signal Reconstruction: Recover the original signal using the Whittaker–Shannon interpolation formula.
Graphical Representation:
- Original Signal with Sample Points.
- Reconstructed Signal.
- Difference Signal: Display the error between the original and reconstructed signals.
- Frequency Domain: Visualize the frequency spectrum to inspect aliasing effects.

**2. Load & Compose**
Signal Loading: Load signals from a file or compose them within the application.
Signal Mixer:
- Add multiple sinusoidal signals with customizable frequencies and magnitudes.
- Remove any component from the signal composition.
- Default Values: Ensures no empty displays; a default signal is always visible.

**3. Additive Noise**
Add noise to the loaded signal with adjustable Signal-to-Noise Ratio (SNR).
Observe the dependency of noise effects on signal frequencies.

**4. Real-time Updates**
Sampling and recovery are performed in real time, reflecting changes instantly without requiring a refresh button.

**5. Reconstruction Methods**
Explore multiple reconstruction methods:
Whittaker–Shannon interpolation.
Other alternative methods, with their pros and cons available for comparison.
Select reconstruction methods via a combobox.

