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

class MainApp(QMainWindow):
    def __init__(self,file_path):
        super().__init__()

        # self.signalData = self.generate_default_data()
        # self.reconstructedSignalData = self.generate_default_data()

        self.data_loader = DataLoader(file_path)
        self.signalData = self.data_loader.get_data()  
        self.reconstructedSignalData = self.signalData



        self.setWindowTitle("Signal")
        self.resize(1080, 720)
        self.setWindowState(Qt.WindowMaximized)
        self.setStyleSheet("background-color: #f0f1f5;")


        self.controlBar = ToolBar()
        # self.controlBar.setStyleSheet("background:red;")
        self.controlBar.dataLoaded.connect(self.updateSignalData)
        self.controlBar.dataLoaded.connect(lambda data: self.updateSignalData(data.to_numpy()))
        self.controlBar.snrChanged.connect(self.updateNoise)

        self.composer = Composer()
        # self.composer.setStyleSheet("background:blue;")

        self.originalSignal = PlotWidget()
        self.originalSignal.setLabel('left', 'Amplitude')
        self.originalSignal.setLabel('bottom', 'Time', units='s')
        self.originalSignal.addLegend()

        self.noisySignal = PlotWidget()

        self.reconstructedSignal = PlotWidget()
        self.reconstructedSignal.setStyleSheet("background:purple;")

        self.diffrenceGraph = PlotWidget()
        self.diffrenceGraph.setStyleSheet("background:light blue;")

        self.frequencyDomain = PlotWidget()
        self.frequencyDomain.setStyleSheet("background:dark grey;")

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

        self.originalSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.originalSignal))
        self.reconstructedSignal.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.reconstructedSignal))
        self.diffrenceGraph.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.diffrenceGraph))
        self.frequencyDomain.sigXRangeChanged.connect(lambda: self.limit_x_axis(self.frequencyDomain))

    def limit_x_axis(self, plot_widget):
        x_min, x_max = plot_widget.viewRange()[0]
        if x_min < 0:
            plot_widget.setXRange(0, x_max, padding=0)
    
    def add_noise(self, data, snrdb):
        signal_power = np.sum(data ** 2)
        Gaussian_noise = np.random.normal(0, 1, len(data))
        noise_power = np.sum(Gaussian_noise ** 2)
        snr = 10 ** (snrdb * 0.1)
        alpha = np.sqrt(signal_power / (snr * noise_power))
        noisy_signal = data + alpha * Gaussian_noise
        return noisy_signal
    
    def updateNoise(self, snr_value):
      
        if self.signalData.shape[1] >= 2:
            y = self.signalData[:, 1]
            x = self.signalData[:, 0]
            noisy_signal = self.add_noise(y, snr_value)

           
            self.originalSignal.clear()
            self.originalSignal.plot(x, self.signalData[:, 1], pen=mkPen(color="b", width=2), name="Original Signal")
            self.originalSignal.plot(x, noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Signal")
            

    
    def generate_default_data(self): #testing
        time = np.linspace(0, 1, 1000)
        amplitude = np.sin(2 * np.pi * 122 * time)
        return np.column_stack((time, amplitude))

    def updateSignalData(self, data):
        self.signalData = np.array(data)
        snr_value = self.controlBar.snrSlider.value()
        
        print("data")
        if self.signalData.shape[1] >= 2:
            x = self.signalData[:, 0]
            y = self.signalData[:, 1]

            self.originalSignal.clear()
            self.originalSignal.plot(x, y, pen=mkPen(color="b", width=2), name="Original Signal")
                
            noisy_signal = self.add_noise(y, snr_value)
            
            self.originalSignal.plot(x, noisy_signal, pen=mkPen(color="r", width=1, style=Qt.DashLine), name="Noisy Signal")


        if self.reconstructedSignalData.shape[1] >= 2:
            x = self.reconstructedSignalData[:, 0]
            y = self.reconstructedSignalData[:, 1]

            self.reconstructedSignal.clear()
            self.reconstructedSignal.plot(x, y, pen=mkPen(color="b", width=2), name="Original Signal")

        print("Signal Data Updated:")
        print(self.signalData)

    
        self.diffrenceGraph.clear()
        if self.signalData.shape[1] >= 2 and self.reconstructedSignalData.shape[1] >= 2:
            difference = self.calculate_difference(self.signalData[:, 1], self.reconstructedSignalData[:, 1])
            self.diffrenceGraph.plot(self.signalData[:, 0], difference, pen=mkPen(color="r", width=2), name="Difference")


        self.plot_frequency_domain(self.signalData[:, 1], self.signalData[1, 0] - self.signalData[0, 0])

    def calculate_difference(self, signal1, signal2):

        length = max(len(signal1), len(signal2))
        padded_signal1 = np.pad(signal1, (0, length - len(signal1)), 'constant')
        padded_signal2 = np.pad(signal2, (0, length - len(signal2)), 'constant')
        return padded_signal1 - padded_signal2
    
    def plot_frequency_domain(self, amplitude, time_step):
        N = len(amplitude)
        fft_values = np.fft.fft(amplitude)
        fft_frequencies = np.fft.fftfreq(N, d=time_step)

        # Only use the positive half of the FFT results
        positive_frequencies = fft_frequencies[:N // 2]
        magnitudes = np.abs(fft_values[:N // 2])


        self.frequencyDomain.clear()
        self.frequencyDomain.plot(positive_frequencies, magnitudes, pen=mkPen(color="r", width=2), name="Frequency Domain")


if __name__ == "__main__":
    csv_file_path = 'signals_data/ECG_Normal.csv'
    app = QApplication(sys.argv)
    main_app = MainApp(csv_file_path)
    main_app.show()
    sys.exit(app.exec_())
