import os
import sys
import numpy as np
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, QCheckBox, \
    QDoubleSpinBox, QSlider, QLabel, QSpinBox
from pyqtgraph import PlotWidget, mkPen
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toolbar import ToolBar
from Composer import Composer
from Core.mixer import mixer, remove_elements
from Core.noise import add_noise
from Core.mainCore import sample_and_reconstruct, sinc_interp, linear_interp, calculate_max_frequency, \
    zoh_reconstruction, cubic_spline_interp, calculate_difference
from Styles.ToolBarStyling import sliderOnStyle, \
    sliderOffStyle, labelOffStyle, labelOnStyle, numberInputOffStyle, samplingRateInputOnStyle, DoubleInputOnStyle


class MainApp(QMainWindow):
    snrEnabledChanged = pyqtSignal(bool)
    snrChanged = pyqtSignal(float)
    # samplingRateChanged = pyqtSignal(float)

    def initialize(self):
        self.old_amplitude = None
        self.old_frequency = None
        self.old_type = None
        self.interp_methods = {
            "Whittaker-Shannon (sinc)": sinc_interp,
            "Linear": linear_interp,
            "Zero-Order Hold": zoh_reconstruction,
            "Cubic-Spline": cubic_spline_interp
        }
        self.interp_method = self.interp_methods["Whittaker-Shannon (sinc)"]
        # self.data_loader = DataLoader(csv_file_path)
        # self.signalData = self.data_loader.get_data()
        self.signalData = self.generate_default_data()
        # self.signalfMax = calculate_max_frequency(self.signalData[:, 1], self.signalData[:, 0])
        self.signalfMax = 5
        self.sampling_rate = 13
        self.mixedSignalData = None
        self.reconstructedSignalData = self.signalData



        self.is_panning = False
        self.current_signal_index = None

    def createUI(self):
        self.createUIElements()
        self.stylingUI()
        self.settingUI()
        self.linkingUI()
        print("Created UI")

    def createUIElements(self):
        self.controlBar = ToolBar()
        self.composer = Composer()

        self.snrEnable = QCheckBox("SNR: ")
        self.snrSlider = QSlider(Qt.Horizontal)
        self.snrInput = QDoubleSpinBox()

        self.samplingRateLabel = QLabel("Sampling Rate: ")
        self.samplingSlider = QSlider(Qt.Horizontal)
        self.samplingRateInput = QSpinBox()
        self.normSamplingRateInput = QDoubleSpinBox()

        self.originalSignal = PlotWidget()
        self.reconstructedSignal = PlotWidget()
        self.diffrenceGraph = PlotWidget()
        self.frequencyDomain = PlotWidget()

        print("Created UI elements")
    def stylingUI(self):

        self.snrEnable.setStyleSheet(labelOffStyle)
        self.snrSlider.setStyleSheet(sliderOffStyle)
        self.snrInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.snrInput.setAlignment(Qt.AlignCenter)
        self.snrInput.setStyleSheet(numberInputOffStyle)
        self.snrInput.setAlignment(Qt.AlignCenter)

        self.samplingRateLabel.setStyleSheet("""font-family: 'Samsung Sans'; font-size: 14px; font-weight: 600; color: #2252A0;""")
        self.samplingRateInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.samplingRateInput.setAlignment(Qt.AlignCenter)
        self.samplingRateInput.setStyleSheet(samplingRateInputOnStyle)
        self.samplingRateInput.setSuffix("Hz")

        self.samplingSlider.setStyleSheet(sliderOnStyle)
        self.normSamplingRateInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.normSamplingRateInput.setAlignment(Qt.AlignCenter)
        self.normSamplingRateInput.setStyleSheet(DoubleInputOnStyle)
        self.normSamplingRateInput.setSuffix(" fmax")
        self.originalSignal.setLabel('left', 'Amplitude')
        self.originalSignal.setLabel('bottom', 'Time', units='s')
        self.originalSignal.addLegend()
        self.reconstructedSignal.addLegend()
        self.diffrenceGraph.addLegend()
        self.frequencyDomain.addLegend()

        print("Ui is styled")

    def linkingUI(self):
        self.controlBar.dataLoaded.connect(self.updateSignalData)
        self.controlBar.dataLoaded.connect(lambda data: (self.updateSignalData(data.to_numpy()), self.updateFrequency(data.to_numpy())))


        self.controlBar.dataLoaded.connect(self.composer.clear_table)
        self.controlBar.methodChanged.connect(self.updateSamplingMethod)
        self.controlBar.clearButton.clicked.connect(self.clearAll)

        self.samplingSlider.sliderReleased.connect(lambda: self.samplingRateInput.setValue(self.samplingSlider.value()))

        self.samplingSlider.valueChanged.connect(
            lambda value: self.samplingRateInput.setValue(value) if self.samplingRateInput.value() != value else None)
        self.samplingRateInput.valueChanged.connect(
            lambda value: (
                self.updateSamplingRate(value),
                self.samplingSlider.setValue(value) if self.samplingSlider.value() != value else None
            )
        )

        self.snrEnabledChanged.connect(self.updateNoise)
        self.snrChanged.connect(self.updateNoise)

        #repeatition!!!
        self.snrSlider.valueChanged.connect(lambda value: self.snrInput.setValue(value / 1.0))  # Convert to float
        self.snrInput.valueChanged.connect(lambda value: self.snrSlider.setValue(int(value)))
        self.snrSlider.valueChanged.connect(self.on_snr_changed)
        self.snrEnable.stateChanged.connect(self.on_snr_enabled_changed)
        # self.snrChanged.connect(self.updateNoise)

        # limit x
        # self.originalSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.originalSignal))
        # self.reconstructedSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.reconstructedSignal))
        # self.diffrenceGraph.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.diffrenceGraph))

        # self.frequencyDomain.sigXRangeChanged.connect(lambda: self.limit_axis(self.frequencyDomain))


        # link panning
        # self.originalSignal.sigXRangeChanged.connect(self.sync_pan)
        # self.reconstructedSignal.sigXRangeChanged.connect(self.sync_pan)
        # self.diffrenceGraph.sigXRangeChanged.connect(self.sync_pan)

        print("UI is linked")

    def settingUI(self):


        self.snrSlider.setRange(1, 30)
        self.snrInput.setRange(1, 30)
        self.snrSlider.setValue(30)
        self.snrInput.setDecimals(2)
        self.snrInput.setValue(30)

        self.samplingSlider.setValue(self.sampling_rate)
        self.samplingSlider.setRange(1,300)
        self.samplingSlider.setSingleStep(1)
        self.samplingRateInput.setRange(0, 300)

        self.normSamplingRateInput.setEnabled(False)

        self.snr_enabled = False
        self.snrSlider.setEnabled(False)
        self.snrInput.setEnabled(False)




        print("Ui is set")

    def __init__(self, csv_file_path):
        super().__init__()
        self.initialize()
        self.createUI()


        self.setWindowTitle("Signal")
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("background-color: #f0f1f5;")







        self.composer.valueAdded.connect(self.add_mixed_signal)
        self.composer.valueRemoved.connect(self.remove_element)
        self.composer.valueUpdated.connect(self.update_table_mixed_signal)




        #
        # self.samplingSlider.setValue(int(200 / self.signalfMax))

        # self.normSamplingRateInput.setRange(0, 4)

        # Update normalized sampling rate input when the slider is changed
        # self.samplingSlider.valueChanged.connect(lambda value: self.samplingRateInput.setValue(value/1.0))

        # Update slider when the normalized sampling rate input is changed
        # self.normSamplingRateInput.valueChanged.connect(lambda value: self.samplingSlider.setValue(int(value * 100)))

        # Update sampling rate input when normalized sampling rate input is changed
        # self.normSamplingRateInput.valueChanged.connect(
        #     lambda: self.samplingRateInput.setValue(self.signalfMax * self.normSamplingRateInput.value())
        # )

        # Update slider when the sampling rate input is changed
        # self.samplingRateInput.valueChanged.connect(
        #     lambda value: self.samplingSlider.setValue(int(value / self.signalfMax * 100)) if self.signalfMax else None
        # )
        # self.samplingRateInput.valueChanged.connect(self.on_sampling_rate_changed)


        # self.composer.setStyleSheet("background:blue;")


        # self.noisySignal = PlotWidget()
        # self.reconstructedSignal.setStyleSheet("background:purple;")

        # self.diffrenceGraph.setStyleSheet("background:light blue;")

        # self.frequencyDomain.setStyleSheet("background:dark grey;")

        self.mainLayout = QHBoxLayout()
        self.controlBarLayout = QHBoxLayout()
        self.workspace = QHBoxLayout()
        self.graphsLayout = QVBoxLayout()
        self.workspace = QVBoxLayout()
        self.composerLayout = QVBoxLayout()
        self.graphsLayout = QVBoxLayout()
        self.originalSignalLayout = QHBoxLayout()
        self.reconstructedSignalLayout = QHBoxLayout()
        self.comparisonLayout = QHBoxLayout()
        self.diffrenceGraphLayout = QVBoxLayout()
        self.frequencyDomainLayout = QVBoxLayout()

        # self.comparisonLayout.addLayout(self.diffrenceGraphLayout)
        # self.comparisonLayout.addLayout(self.frequencyDomainLayout)

        self.graphsLayout.addLayout(self.originalSignalLayout, 30)
        self.graphsLayout.addLayout(self.reconstructedSignalLayout, 30)
        self.graphsLayout.addLayout(self.comparisonLayout, 40)

        self.workspace.addLayout(self.controlBarLayout, 5)
        self.workspace.addLayout(self.graphsLayout, 95)

        self.mainLayout.addLayout(self.workspace, 85)
        self.mainLayout.addLayout(self.composerLayout, 15)

        self.controlBarLayout.addWidget(self.controlBar)
        # self.composerLayout.addWidget(self.composer)
        # Adding the SNR and sampling sliders to the composerLayout

        # horizontal layout for the 2 fields of sampling values
        samplingRateInputLayout = QHBoxLayout()
        samplingRateInputLayout.addWidget(self.samplingRateInput)
        # samplingRateInputLayout.addStretch(10)
        samplingRateInputLayout.addWidget(self.normSamplingRateInput)

        # self.composerLayout.addSpacing(10)
        self.composerLayout.addWidget(self.samplingRateLabel)
        self.composerLayout.addSpacing(10)
        self.composerLayout.addWidget(self.samplingSlider)
        self.composerLayout.addSpacing(10)
        self.composerLayout.addLayout(samplingRateInputLayout)
        self.composerLayout.addSpacing(20)

        self.composerLayout.addWidget(self.snrEnable)
        self.composerLayout.addSpacing(10)
        self.composerLayout.addWidget(self.snrSlider)
        self.composerLayout.addSpacing(10)
        self.composerLayout.addWidget(self.snrInput)
        self.composerLayout.addSpacing(20)
        self.composerLayout.addWidget(self.composer)

        self.originalSignalLayout.addWidget(self.originalSignal)
        self.reconstructedSignalLayout.addWidget(self.reconstructedSignal)
        self.diffrenceGraphLayout.addWidget(self.diffrenceGraph)
        self.frequencyDomainLayout.addWidget(self.frequencyDomain)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.diffrenceGraph)
        self.splitter.addWidget(self.frequencyDomain)
        self.comparisonLayout.addWidget(self.splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.updateSignalData(self.signalData)


    def onMethodChanged(self, value):
        self.methodChanged.emit(self.samplingMethod.currentText())

    def on_snr_changed(self, value):
        self.snrChanged.emit(value / 1.0)

    def on_snr_enabled_changed(self, state):
        is_enabled = state == Qt.Checked
        self.snrEnabledChanged.emit(is_enabled)

        self.snrSlider.setEnabled(is_enabled)
        self.snrInput.setEnabled(is_enabled)

        if is_enabled:
            self.snrSlider.setStyleSheet(sliderOnStyle)
            self.snrInput.setStyleSheet(DoubleInputOnStyle)
            self.snrEnable.setStyleSheet(labelOnStyle)
        else:
            self.snrSlider.setStyleSheet(sliderOffStyle)
            self.snrInput.setStyleSheet(numberInputOffStyle)
            self.snrEnable.setStyleSheet(labelOffStyle)

    def sync_pan(self, plot_widget):

        if self.is_panning:
            return

        self.is_panning = True
        time_min, time_max = plot_widget.viewRange()[0]

        if plot_widget != self.originalSignal:
            self.originalSignal.setXRange(time_min, time_max, padding=0)

        if plot_widget != self.reconstructedSignal:
            self.reconstructedSignal.setXRange(time_min, time_max, padding=0)

        if plot_widget != self.diffrenceGraph:
            self.diffrenceGraph.setXRange(time_min, time_max, padding=0)

        self.originalSignal.setXRange(7, 13)
        self.is_panning = False

    def limit_x_axis(self, plot_widget):
        time_min, time_max = plot_widget.viewRange()[0]

        if time_min < 0:
            time_min = 0

        time_end = self.signalData[-1, 0]

        if time_max > time_end:
            time_max = time_end

        plot_widget.setXRange(time_min, time_max, padding=0)

    def updateNoise(self, enabled):
        if not self.snr_enabled:
            self.snr_enabled = enabled
        self.updateSignalData(self.signalData)
        # self.updateNoise(self.snrSlider.value())

    # def updateNoise(self, snr_value):
    #     if not self.snr_enabled:
    #         return
    #
    #     time = self.signalData[:, 0]
    #     amplitude = self.signalData[:, 1]
    #
    #     self.noisy_amplitude = add_noise(amplitude, snr_value)
    #
    #     self.sampledTime, self.sampledSignal, self.reconstructedSignalData = sample_and_reconstruct(
    #         self.signalData[:, 0], self.noisy_amplitude, self.sampling_rate, self.interp_method)
    #
    #     noisy_signal_reconstructed = self.reconstructedSignalData
    #
    #     self.originalSignal.clear()
    #
    #     self.originalSignal.plot(time, self.noisy_amplitude, pen=mkPen(color="#a000c8", width=2),
    #                              name="Original Signal With Noise")
    #     self.originalSignal.plot(self.sampledTime, self.sampledSignal, pen=None, symbol='o', symbolSize=5,
    #                              symbolBrush='w')
    #     self.reconstructedSignal.clear()
    #
    #     self.reconstructedSignal.plot(time, noisy_signal_reconstructed, pen=mkPen(color="b", width=2),
    #                                   name="Reconstructed Signal")
    #     self.diffrenceGraph.clear()
    #     noise_difference = calculate_difference(self.signalData[:, 1], noisy_signal_reconstructed)
    #     meanError = np.mean(noise_difference)
    #     self.diffrenceGraph.plot(time, noise_difference, pen=mkPen(color="r", width=2),
    #                              name=f"Difference graph with Error: {meanError:.4f}")
    #     time_step = time[1] - time[0]
    #     self.frequencyDomain.clear()
    #     self.plot_frequency_domain(self.noisy_amplitude, time_step)

    def generate_default_data(self):  # testing
        time = np.linspace(0, 10, 5000)
        amplitude = np.sin(2 * np.pi * 5 * time)
        return np.column_stack((time, amplitude))

    def updateSamplingRate(self, samplingRate):
        self.sampling_rate = samplingRate

        try:
            self.updateSignalData(self.signalData)
        except Exception as e:
            print(f"An error occurred while updating signal data AFTER SAMPLING SLIDER: {e}")

    def updateSamplingMethod(self, method):
        self.interp_method = self.interp_methods[method]
        self.updateSignalData(self.signalData)

    def updateSignalData(self, data):
        self.signalData = np.array(data)
        # self.signalfMax = calculate_max_frequency(self.signalData[:, 1], self.signalData[:, 0])

        snr_value = self.snrSlider.value()

        if self.signalData.shape[1] >= 2:
            time = self.signalData[:, 0]
            amplitude = self.signalData[:, 1]

            if self.snr_enabled:
                amplitude = add_noise(amplitude, snr_value)

            # reconstructed_amplitude = self.reconstructedSignalData
            self.originalSignal.clear()
            self.reconstructedSignal.clear()
            self.sampledTime, self.sampledSignal, reconstructed_amplitude = sample_and_reconstruct(time, amplitude, self.sampling_rate, self.interp_method)

            self.originalSignal.plot(time, amplitude, pen=mkPen(color="#a000c8", width=2), name="Original Signal")
            self.originalSignal.plot(self.sampledTime, self.sampledSignal, pen=None, symbol='o', symbolSize=5,symbolBrush='w')

            self.reconstructedSignal.plot(time, reconstructed_amplitude, pen=mkPen(color="#a000c8", width=2),name="Reconstructed Signal")


            difference = calculate_difference(self.signalData[:, 1], reconstructed_amplitude)
            self.diffrenceGraph.clear()
            self.diffrenceGraph.plot(self.signalData[:, 0], difference, pen=mkPen(color="r", width=2))

            # self.diffrenceGraph.setYRange(-5, 5, padding=1)

            self.plot_frequency_domain(reconstructed_amplitude, self.signalData[1, 0] - self.signalData[0, 0])
    def calculate_difference(self, originalSignal, reconstructedSignalData):
        length = max(len(originalSignal), len(reconstructedSignalData))
        padded_originalSignal = np.pad(originalSignal, (0, length - len(originalSignal)), 'constant')
        padded_reconstructedSignalData = np.pad(reconstructedSignalData, (0, length - len(reconstructedSignalData)),
                                                'constant')
        return padded_originalSignal - padded_reconstructedSignalData


    def plot_frequency_domain(self, amplitude, time_step):
        reconstructed_length = len(amplitude)
        #
        # original_fft_values = np.fft.fft(original_amplitude)
        # original_fft_frequencies = np.fft.fftfreq(reconstructed_length, d=time_step)
        #
        # original_positive_frequencies = original_fft_frequencies[:reconstructed_length // 2]
        # original_magnitudes = np.abs(original_fft_values[:reconstructed_length // 2])

        reconstructed_fft_values = np.fft.fft(amplitude)
        reconstructed_fft_frequencies = np.fft.fftfreq(reconstructed_length, d=time_step)
        reconstructed_positive_frequencies = reconstructed_fft_frequencies[:reconstructed_length // 2]
        reconstructed_magnitudes = np.abs(reconstructed_fft_values[:reconstructed_length // 2])

#Need to be called only when original is changed #LOADED #ADD OR REMOVE Composer
        # threshold = 0.1 * np.max(original_magnitudes)  # Adjust threshold as needed
        # significant_frequencies = original_positive_frequencies[original_magnitudes > threshold]
        # self.signalfMax = np.max(significant_frequencies)

        self.frequencyDomain.clear()
        self.frequencyDomain.plot(reconstructed_positive_frequencies, reconstructed_magnitudes,
                                  pen=mkPen(color="#a000c8", width=2), name="Original Signal Frequency Domain")
        self.frequencyDomain.plot(-1 * reconstructed_positive_frequencies, reconstructed_magnitudes,
                                  pen=mkPen(color="#a000c8", width=2))

        self.frequencyDomain.plot(reconstructed_positive_frequencies + self.sampling_rate, reconstructed_magnitudes,
                                  pen=mkPen(color=(0, 0, 255, 150), width=2), name=" Signals due to periodicity")
        self.frequencyDomain.plot(-reconstructed_positive_frequencies + self.sampling_rate, reconstructed_magnitudes,
                                  pen=mkPen(color=(0, 0, 255, 150), width=2), )

        self.frequencyDomain.plot(reconstructed_positive_frequencies - self.sampling_rate, reconstructed_magnitudes,
                                  pen=mkPen(color=(0, 0, 255, 150), width=2))
        self.frequencyDomain.plot(-reconstructed_positive_frequencies - self.sampling_rate, reconstructed_magnitudes,
                                  pen=mkPen(color=(0, 0, 255, 150), width=2), )


        max_frequency = np.max(reconstructed_positive_frequencies) * 0.5
        max_magnitude = np.max(reconstructed_magnitudes)
        self.frequencyDomain.setXRange(-max_frequency, max_frequency, padding=0)
        self.frequencyDomain.setYRange(0, max_magnitude * 1.1, padding=0.05)

        # max_frequency = np.max(original_positive_frequencies) + self.sampling_rate
        # max_magnitude = np.max(original_magnitudes)

        # self.frequencyDomain.setXRange(-max_frequency * 1.1, max_frequency * 1.1, padding=0.05)
        # self.frequencyDomain.setYRange(0, max_magnitude * 1.1, padding=0.05)

    # def add_mixed_signal(self, amplitude, frequency, signal_type):
    #     self.old_amplitude = amplitude
    #     self.old_frequency = frequency
    #     self.old_type = signal_type

    #     mixed_signal = mixer(self.signalData, amplitude, frequency, signal_type)

    #     self.signalData = np.column_stack((self.signalData[:, 0], mixed_signal))
    #     self.originalSignal.plot(self.sampledTime, self.sampledSignal, pen=None, symbol='o', symbolSize=5,
    #                              symbolBrush='w')
    #     self.updateSignalData(self.signalData)

    #     snr_value = self.snrSlider.value()
    #     noisy_signal = add_noise(mixed_signal, snr_value) if self.snr_enabled else mixed_signal

    #     self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="r", width=2),
    #                              name="Noisy Mixed Signal")
    #     time_step = self.signalData[1, 0] - self.signalData[0, 0]
    #     self.plot_frequency_domain(mixed_signal, time_step)

    def add_mixed_signal(self, amplitude, frequency, signal_type):
        # Only proceed if amplitude, frequency, or signal type has actually changed
        if (amplitude, frequency, signal_type) == (self.old_amplitude, self.old_frequency, self.old_type):
            return  # Skip redundant updates

        # Update cached signal parameters
        self.old_amplitude = amplitude
        self.old_frequency = frequency
        self.old_type = signal_type

        # Generate the mixed signal only if parameters have changed
        mixed_signal = mixer(self.signalData, amplitude, frequency, signal_type)
        self.signalData = np.column_stack((self.signalData[:, 0], mixed_signal))
        self.updateFrequency(self.signalData)

        # Clear and plot the sampled signal
        self.originalSignal.clear()
        self.originalSignal.plot(self.sampledTime, self.sampledSignal, pen=None, symbol='o', symbolSize=5,
                                symbolBrush='w')

        # Update signal data with newly mixed signal
        self.updateSignalData(self.signalData)

        # Check if noise addition is necessary based on SNR and snr_enabled status
        snr_value = self.snrSlider.value()
        if self.snr_enabled and not hasattr(self, 'noisy_signal_applied'):
            noisy_signal = add_noise(mixed_signal, snr_value)
            self.noisy_signal_applied = True
        elif not self.snr_enabled:
            self.noisy_signal_applied = False
            noisy_signal = mixed_signal
        else:
            noisy_signal = self.noisy_amplitude  # Reuse previous noisy signal if unchanged

        # Plot noisy signal, avoiding redundant plotting
        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="r", width=2),
                                name="Noisy Mixed Signal")

        # Compute FFT for frequency domain visualization only if signal data is modified
        time_step = self.signalData[1, 0] - self.signalData[0, 0]

        self.diffrenceGraph.clear()
        difference = self.calculate_difference(self.signalData[:, 1], self.reconstructedSignalData)
        meanError = np.mean(difference)

        self.plot_frequency_domain(mixed_signal, time_step)


    def update_table_mixed_signal(self, row, amplitude, frequency, signal_type):
        old_signal = remove_elements(self.signalData, self.old_amplitude, self.old_frequency, self.old_type)
        updated_signal = mixer(np.column_stack((self.signalData[:, 0], old_signal)), amplitude, frequency, signal_type)

        self.old_amplitude = amplitude
        self.old_frequency = frequency
        self.old_type = signal_type

        self.signalData = np.column_stack((self.signalData[:, 0], updated_signal))

        self.originalSignal.clear()
        self.originalSignal.plot(self.signalData[:, 0], updated_signal, pen=mkPen(color="#a000c8", width=2),
                                 name=f"Updated Signal Row {row}")

        self.updateSignalData(self.signalData)

        snr_value = self.snrSlider.value()
        noisy_signal = add_noise(updated_signal, snr_value) if self.snr_enabled else updated_signal
        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="#a000c8", width=2),
                                 name="Noisy Updated Signal")

    def remove_element(self, amplitude, frequency, signal_type, num_rows):
        old_signal = remove_elements(self.signalData, amplitude, frequency, signal_type)

        self.signalData = np.column_stack((self.signalData[:, 0], old_signal))
        self.updateFrequency(self.signalData)
        self.originalSignal.clear()

        self.originalSignal.plot(self.signalData[:, 0], old_signal, pen=mkPen(color="#a000c8", width=2),
                                 name="Updated Mixed Signal After Removal")
        self.updateSignalData(self.signalData)
        snr_value = self.snrSlider.value()
        noisy_signal = add_noise(old_signal, snr_value) if self.snr_enabled else old_signal

        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="#a000c8", width=2),
                                 name="Noisy Updated Signal After Removal")

        time_step = self.signalData[1, 0] - self.signalData[0, 0]
        self.plot_frequency_domain(old_signal, time_step)
        if not num_rows:
            self.originalSignal.clear()
            self.reconstructedSignal.clear()
            self.diffrenceGraph.clear()
            self.frequencyDomain.clear()
            if self.data_loader:
                self.updateSignalData(self.signalData)

    def clearAll(self):
        self.samplingRateInput.setValue(5)
        self.originalSignal.clear()
        self.signalData[:, 1] *= 0
        self.reconstructedSignal.clear()
        self.diffrenceGraph.clear()
        self.frequencyDomain.clear()
        self.composer.clear_table()
        self.controlBar.signalNameLabel.setText("No signal Loaded ")
        self.data_loader = None

    def updateFrequency(self, signal_data):
        amplitude= signal_data[:, 1]
        amplitude_length= len(amplitude)

        time_step = self.signalData[1, 0] - self.signalData[0, 0]
        original_fft_values = np.fft.fft(amplitude)
        original_fft_frequencies = np.fft.fftfreq(amplitude_length, d=time_step)

        original_positive_frequencies = original_fft_frequencies[:amplitude_length // 2]
        original_magnitudes = np.abs(original_fft_values[:amplitude_length // 2])
        threshold = 0.1 * np.max(original_magnitudes)  # Adjust threshold as needed
        significant_frequencies = original_positive_frequencies[original_magnitudes > threshold]
        self.signalfMax = np.max(significant_frequencies)
        print(self.signalfMax)

if __name__ == "__main__":
    csv_file_path = 'signals_data/ECG_Normal.csv'
    app = QApplication(sys.argv)
    main_app = MainApp(csv_file_path)
    main_app.show()
    sys.exit(app.exec_())
