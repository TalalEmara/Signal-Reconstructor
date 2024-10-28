import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QVBoxLayout, QWidget, QHBoxLayout, QSplitter
from pyqtgraph import PlotWidget, mkPen
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from toolbar import ToolBar
from Composer import Composer
from Core.Data_load import DataLoader
from Core.mixer import mixer, remove_elements
from Core.noise import add_noise
from Core.mainCore import sample_and_reconstruct, sinc_interp,linear_interp, calculate_max_frequency,zoh_reconstruction,cubic_spline_interp

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.old_amplitude = None
        self.old_frequency = None
        self.old_type = None


        self.interp_methods = {
            "Whittaker-Shannon (sinc)": sinc_interp,
            "Linear": linear_interp,
            "Zero-Order Hold": zoh_reconstruction,
            "Cubic-Spline":cubic_spline_interp
        }
        self.interp_method = self.interp_methods["Whittaker-Shannon (sinc)"]

        self.signalData = self.generate_default_data()
        self.signalfMax = calculate_max_frequency(self.signalData[:, 1],self.signalData[:, 0])
        print(self.signalfMax)


        self.sampling_rate = 900

        # self.reconstructedSignalData = self.generate_default_data()


        # self.data_loader = DataLoader(file_path)
        # self.signalData = self.data_loader.get_data()
        self.mixedSignalData = None  
        self.reconstructedSignalData = self.signalData

        

        self.setWindowTitle("Signal")
        self.resize(1080, 720)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("background-color: #f0f1f5;")


        self.controlBar = ToolBar()
        self.controlBar.signalfMax = self.signalfMax



        self.snr_enabled = False
        # self.controlBar.setStyleSheet("background:red;")
        self.controlBar.dataLoaded.connect(self.updateSignalData)
        self.controlBar.dataLoaded.connect(lambda data: self.updateSignalData(data.to_numpy()))
        self.controlBar.snrEnabledChanged.connect(self.set_snr_enabled)
        self.controlBar.snrChanged.connect(self.updateNoise)
        self.controlBar.samplingRateChanged.connect(self.updateSamplingRate)
        self.controlBar.methodChanged.connect(self.updateSamplingMethod)


        self.current_signal_index = None  
      

        self.composer = Composer()
        self.composer.valueAdded.connect(self.add_mixed_signal)
        self.composer.valueUpdated.connect(self.update_table_mixed_signal)
        self.composer.valueRemoved.connect(self.remove_element)
        # self.composer.setStyleSheet("background:blue;")

        self.originalSignal = PlotWidget()
        self.originalSignal.setLabel('left', 'Amplitude')
        self.originalSignal.setLabel('bottom', 'Time', units='s')
        self.originalSignal.addLegend()

        self.noisySignal = PlotWidget()

        self.reconstructedSignal = PlotWidget()
        # self.reconstructedSignal.setStyleSheet("background:purple;")

        self.diffrenceGraph = PlotWidget()
        # self.diffrenceGraph.setStyleSheet("background:light blue;")

        self.frequencyDomain = PlotWidget()
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

        self.graphsLayout.addLayout(self.originalSignalLayout,35)
        self.graphsLayout.addLayout(self.reconstructedSignalLayout,35)
        self.graphsLayout.addLayout(self.comparisonLayout,30)

        self.workspace.addLayout(self.controlBarLayout,5)
        self.workspace.addLayout(self.graphsLayout,95)

        self.mainLayout.addLayout(self.workspace,80)
        self.mainLayout.addLayout(self.composerLayout,20)

        self.controlBarLayout.addWidget(self.controlBar)
        self.composerLayout.addWidget(self.composer)
        self.originalSignalLayout.addWidget(self.originalSignal)
        self.reconstructedSignalLayout.addWidget(self.reconstructedSignal)
        self.diffrenceGraphLayout.addWidget(self.diffrenceGraph)
        self.frequencyDomainLayout.addWidget(self.frequencyDomain)

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.diffrenceGraph)
        self.splitter.addWidget(self.frequencyDomain)
        self.comparisonLayout.addWidget(self.splitter)

        mainWidget = QWidget()
        mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(mainWidget)

        self.updateSignalData(self.signalData) 

        #limit x 
        self.originalSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.originalSignal))
        self.reconstructedSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.reconstructedSignal))
        self.diffrenceGraph.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.diffrenceGraph))
        self.frequencyDomain.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.frequencyDomain))

    def limit_x_axis(self, plot_widget):
        x_min, x_max = plot_widget.viewRange()[0]
        if x_min < 0:
            plot_widget.setXRange(0, x_max, padding=0)
    
    def set_snr_enabled(self, enabled):
        self.snr_enabled = enabled
        self.updateSignalData(self.signalData)
    
    def updateNoise(self, snr_value):
        if not self.snr_enabled: 
            return
      
        if self.mixedSignalData is not None:
            x = self.mixedSignalData[:, 0]
            y = self.mixedSignalData[:, 1]
        else:
            x = self.signalData[:, 0]
            y = self.signalData[:, 1]

        noisy_signal = add_noise(y, snr_value)
        
        self.originalSignal.clear()
        self.originalSignal.plot(x, y, pen=mkPen(color="b", width=2), name="Original or Mixed Signal")
        self.originalSignal.plot(x, noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Signal")

        self.plot_frequency_domain(y, noisy_signal, x[1] - x[0])

    def generate_default_data(self): #testing
        time = np.linspace(0, 1, 1000)
        amplitude = np.sin(2 * np.pi * 122 * time)
        return np.column_stack((time, amplitude))

    def updateSamplingRate(self, samplingRate):
        self.sampling_rate = int(samplingRate)
        print(samplingRate)
        print(self.sampling_rate)
        try:
            self.updateSignalData(self.signalData)
        except Exception as e:
            # Handle the exception (e.g., log it or show a message)
            print(f"An error occurred while updating signal data: {e}")

    def updateSamplingMethod(self, method):
        print(method)
        self.interp_method = self.interp_methods[method]
        print(self.interp_method)
        self.updateSignalData(self.signalData)
    def updateSignalData(self, data):
        self.signalData = np.array(data)
        snr_value = self.controlBar.snrSlider.value()
        
        print("data")
        if self.signalData.shape[1] >= 2:
            x = self.signalData[:, 0]
            y = self.signalData[:, 1]

            self.originalSignal.clear()
            self.originalSignal.plot(x, y, pen=mkPen(color="b", width=2), name="Original Signal")
                
            if self.snr_enabled:
                noisy_signal = add_noise(y, snr_value)
                self.originalSignal.plot(x, noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Signal")

            else:
                noisy_signal = y

        self.sampledTime,self.sampledSignal,self.reconstructedSignalData = sample_and_reconstruct(self.signalData[:, 0], self.signalData[:, 1], self.sampling_rate, self.interp_method)
        x = self.signalData[:, 0]
        y = self.reconstructedSignalData
        # print(np.dim(y))

        self.originalSignal.plot(self.sampledTime, self.sampledSignal,symbol='o', symbolSize=8, symbolBrush='b')

        self.reconstructedSignal.clear()
        self.reconstructedSignal.plot(x, y, pen=mkPen(color="b", width=2), name="Original Signal")

        print("Signal Data Updated:")
        print(self.signalData)

        self.diffrenceGraph.clear()
        if self.signalData.shape[1] >= 2 and self.reconstructedSignalData.ndim == 1:
            difference = self.calculate_difference(self.signalData[:, 1], self.reconstructedSignalData)
            self.diffrenceGraph.plot(self.signalData[:, 0], difference, pen=mkPen(color="r", width=2),
                                     name="Difference")

        self.plot_frequency_domain(self.signalData[:, 1], noisy_signal, self.signalData[1, 0] - self.signalData[0, 0])

        self.add_frequency_domain(self.reconstructedSignalData , self.signalData[1, 0] - self.signalData[0, 0])

    def calculate_difference(self, signal1, signal2):

        length = max(len(signal1), len(signal2))
        padded_signal1 = np.pad(signal1, (0, length - len(signal1)), 'constant')
        padded_signal2 = np.pad(signal2, (0, length - len(signal2)), 'constant')
        return padded_signal1 - padded_signal2

    import numpy as np

    def add_frequency_domain(self, reconstructedSignalData, time_difference):
        reconstructedSignalData = np.array(reconstructedSignalData)

        # Perform FFT
        fft_result = np.fft.fft(reconstructedSignalData)

        N = len(reconstructedSignalData)
        frequencies = np.fft.fftfreq(N, d=time_difference)

        # Calculate the magnitude of the FFT
        magnitude = np.abs(fft_result)

        # Check if frequency and magnitude arrays are correctly formed
        if len(frequencies) != len(magnitude):
            print("Length mismatch between frequencies and magnitudes!")
            return

        # Plot the positive frequencies and their corresponding magnitudes
        self.frequencyDomain.plot(frequencies[:N // 2], magnitude[:N // 2], pen=(255, 0, 0), width=2)

        # Optionally, set the axis limits for better visibility
        self.frequencyDomain.setXRange(0, np.max(frequencies[:N // 2]), padding=0)
        self.frequencyDomain.setYRange(0, np.max(magnitude[:N // 2]), padding=0)
    def plot_frequency_domain(self, original_amplitude, noisy_amplitude,time_step):
        N = len(original_amplitude)

        original_fft_values = np.fft.fft(original_amplitude)
        original_fft_frequencies = np.fft.fftfreq(N, d=time_step)
        original_positive_frequencies = original_fft_frequencies[:N // 2]
        original_magnitudes = np.abs(original_fft_values[:N // 2])

        noisy_fft_values = np.fft.fft(noisy_amplitude)
        noisy_magnitudes = np.abs(noisy_fft_values[:N // 2])


        self.frequencyDomain.clear()
        self.frequencyDomain.plot(original_positive_frequencies, original_magnitudes, pen=mkPen(color="b", width=2), name="Original Signal Frequency Domain")
        
        if self.snr_enabled:
            self.frequencyDomain.plot(original_positive_frequencies, noisy_magnitudes, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Signal Frequency Domain")
    
    def add_mixed_signal(self, amplitude, frequency, signal_type):
        self.old_amplitude = amplitude
        self.old_frequency = frequency
        self.old_type = signal_type

        mixed_signal = mixer(self.signalData, amplitude, frequency,signal_type)
        # print(self.signalData[:, 1])
        self.signalData = np.column_stack((self.signalData[:, 0], mixed_signal)) 
        # print(self.signalData[:, 1])


        # self.originalSignal.clear()
        # self.originalSignal.plot(self.signalData[:, 0], mixed_signal, pen=mkPen(color="b", width=2), name="Mixed Signal")
        combined_signal = np.column_stack((self.signalData[:, 0], mixed_signal))

        self.updateSignalData(self.signalData)

        snr_value = self.controlBar.snrSlider.value()
        noisy_signal = add_noise(mixed_signal, snr_value) if self.snr_enabled else mixed_signal

        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Mixed Signal")
        time_step = self.signalData[1, 0] - self.signalData[0, 0]
        self.plot_frequency_domain(mixed_signal, noisy_signal, time_step)

    def update_table_mixed_signal(self, row, amplitude, frequency,signal_type):
        old_signal = remove_elements(self.signalData, self.old_amplitude, self.old_frequency, self.old_type)
        updated_signal = mixer(np.column_stack((self.signalData[:, 0], old_signal)), amplitude, frequency, signal_type)
        
        self.old_amplitude = amplitude
        self.old_frequency = frequency
        self.old_type = signal_type

        self.signalData = np.column_stack((self.signalData[:, 0], updated_signal))

        self.originalSignal.clear()
        self.originalSignal.plot(self.signalData[:, 0], updated_signal, pen=mkPen(color="b", width=2), name=f"Updated Signal Row {row}")

        self.updateSignalData(self.signalData)


        snr_value = self.controlBar.snrSlider.value()
        noisy_signal = add_noise(updated_signal, snr_value) if self.snr_enabled else updated_signal
        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Updated Signal")

    def remove_element(self, amplitude, frequency, signal_type):
        # Remove the specified elements from the signal data
        old_signal = remove_elements(self.signalData, amplitude, frequency, signal_type)
        
        # Update the signalData with the modified signal
        self.signalData = np.column_stack((self.signalData[:, 0], old_signal))

        # Clear the previous plot
        self.originalSignal.clear()
        
        # Plot the updated mixed signal
        self.originalSignal.plot(self.signalData[:, 0], old_signal, pen=mkPen(color="b", width=2), name="Updated Mixed Signal After Removal")
        
        self.updateSignalData(self.signalData)


        # Get the current SNR value and add noise if enabled
        snr_value = self.controlBar.snrSlider.value()
        noisy_signal = add_noise(old_signal, snr_value) if self.snr_enabled else old_signal
        
        # Plot the noisy version of the updated signal
        self.originalSignal.plot(self.signalData[:, 0], noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Updated Signal After Removal")
        
        # Update frequency domain plot
        time_step = self.signalData[1, 0] - self.signalData[0, 0]
        self.plot_frequency_domain(old_signal, noisy_signal, time_step)


if __name__ == "__main__":
    csv_file_path = '../signals_data/ECG_Abnormal.csv'
    app = QApplication(sys.argv)
    main_app = MainApp(csv_file_path)
    main_app.show()
    sys.exit(app.exec_())

