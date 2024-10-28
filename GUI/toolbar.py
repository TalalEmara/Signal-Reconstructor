import os

import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSlider, QComboBox, QDoubleSpinBox, \
    QFileDialog, QCheckBox

from Styles.ToolBarStyling import toolBarStyle, buttonStyle, buttonWhiteStyle, comboBoxStyle, sliderOnStyle,sliderOffStyle, TitleStyle, labelOffStyle,labelOnStyle, numberInputOffStyle,numberInputOnStyle


class ToolBar(QWidget):
    dataLoaded = pyqtSignal(pd.DataFrame)
    snrChanged = pyqtSignal(float)
    methodChanged = pyqtSignal(str)
    snrEnabledChanged = pyqtSignal(bool)
    deleteSignal = pyqtSignal()

    samplingRateChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(toolBarStyle)

        self.signalName = "Default Signal"
        self.signalData = []
        self.signalfMax = 100

        self.title = QLabel("ReSigni | ")
        self.title.setStyleSheet(TitleStyle)
        self.nameLabel = QLabel("name: ")
        self.signalNameLabel = QLabel(self.signalName)
        self.signalNameLabel.setStyleSheet("color: black; font-size: 14px;")

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.loadSignal)
        self.browseButton.setStyleSheet(buttonStyle)

        self.clearButton = QPushButton("clear")
        self.clearButton.setStyleSheet(buttonWhiteStyle)




        self.snrEnable = QCheckBox("SNR: ")
        self.snrEnable.setStyleSheet(labelOffStyle)
        self.snrSlider = QSlider(Qt.Horizontal)
        self.snrSlider.setStyleSheet(sliderOffStyle)
        self.snrInput = QDoubleSpinBox()
        self.snrInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.snrInput.setAlignment(Qt.AlignCenter)
        self.snrInput.setStyleSheet(numberInputOffStyle)

        self.snrSlider.setRange(0, 30)

        self.snrInput.setRange(0, 30)
        self.snrSlider.setValue(30)
        self.snrInput.setDecimals(2)
        self.snrInput.setValue(30)
        self.snrInput.setAlignment(Qt.AlignCenter)

        self.snrSlider.setEnabled(False)
        self.snrInput.setEnabled(False)

        self.snrSlider.valueChanged.connect(lambda value: self.snrInput.setValue(value / 1.0))  # Convert to float
        self.snrInput.valueChanged.connect(lambda value: self.snrSlider.setValue(int(value)))
        self.snrSlider.valueChanged.connect(self.on_snr_changed)
        self.snrEnable.stateChanged.connect(self.on_snr_enabled_changed)

        self.samplingMethodLabel = QLabel("reconstruction method: ")
        self.samplingMethod = QComboBox()
        self.samplingMethod.setStyleSheet(comboBoxStyle)
        self.samplingMethod.addItem("Whittaker-Shannon (sinc)")
        self.samplingMethod.addItem("Linear")
        self.samplingMethod.addItem("Zero-Order Hold")
        self.samplingMethod.addItem("Cubic-Spline")


        self.samplingSlider = QSlider(Qt.Horizontal)
        self.samplingSlider.setRange(0, 400)
        self.samplingSlider.setSingleStep(1)
        self.samplingSlider.setStyleSheet(sliderOnStyle)

        self.samplingRateLabel = QLabel("sampling rate: ")
        self.samplingRateInput = QDoubleSpinBox()
        self.samplingRateInput.setRange(0, float('inf'))
        self.samplingRateInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.samplingRateInput.setAlignment(Qt.AlignRight)
        self.samplingRateInput.setStyleSheet(numberInputOnStyle)
        self.samplingRateInput.setSuffix("Hz")

        self.normSamplingRateInput = QDoubleSpinBox()
        self.normSamplingRateInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.normSamplingRateInput.setAlignment(Qt.AlignCenter)
        self.normSamplingRateInput.setStyleSheet(numberInputOnStyle)
        self.normSamplingRateInput.setSuffix(" fmax")
        self.normSamplingRateInput.setRange(0,4)

        self.samplingSlider.valueChanged.connect(lambda value: self.normSamplingRateInput.setValue(value / 100.0))
        self.normSamplingRateInput.valueChanged.connect(lambda value: self.samplingSlider.setValue(int(value * 100)))
        self.normSamplingRateInput.valueChanged.connect(lambda: self.samplingRateInput.setValue(self.signalfMax * self.normSamplingRateInput.value()))
        self.samplingRateInput.valueChanged.connect(lambda value: self.samplingSlider.setValue(int(value / self.signalfMax * 100)) if self.signalfMax else None)
        self.samplingRateInput.valueChanged.connect(self.on_sampling_rate_changed)
        self.samplingMethod.currentIndexChanged.connect(self.onMethodChanged)

        self.rowLayout = QHBoxLayout()
        self.rowLayout.addWidget(self.title, 1)
        self.rowLayout.addWidget(self.nameLabel, 1)
        self.rowLayout.addWidget(self.signalNameLabel, 1)
        self.rowLayout.addWidget(self.browseButton, 5)
        self.rowLayout.addWidget(self.clearButton, 3)
        self.rowLayout.addStretch(1)
        self.rowLayout.addWidget(self.samplingMethodLabel,2)
        self.rowLayout.addWidget(self.samplingMethod,10)
        self.rowLayout.addStretch(1)
        self.rowLayout.addWidget(self.samplingRateLabel,2)
        self.rowLayout.addWidget(self.samplingSlider,7)
        self.rowLayout.addWidget(self.normSamplingRateInput,5)
        self.rowLayout.addWidget(self.samplingRateInput,5)
        self.rowLayout.addStretch(1)
        self.rowLayout.addWidget(self.snrEnable,2)
        self.rowLayout.addWidget(self.snrSlider,8)
        self.rowLayout.addWidget(self.snrInput,5)
        # self.rowLayout.addStretch(20)


        self.layout = QVBoxLayout()
        self.layout.addLayout(self.rowLayout)
        self.setLayout(self.layout)

    def loadSignal(self):
        # Open a file dialog to select a CSV file
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open CSV File", "", "CSV Files (*.csv);;All Files (*)",
                                                   options=options)
        if file_name:
            self.signalName = os.path.basename(file_name)
            self.signalNameLabel.setText(self.signalName)
            try:
                data = pd.read_csv(file_name)
                self.dataLoaded.emit(data)
                print("CSV Data Loaded Successfully:")
                print(data)  # Print or process the data as needed
            except Exception as e:
                print(f"Error loading CSV file: {e}")

    def on_sampling_rate_changed(self, value):
        self.samplingRateChanged.emit(value)

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
            self.snrInput.setStyleSheet(numberInputOnStyle)
            self.snrEnable.setStyleSheet(labelOnStyle)
        else:
            self.snrSlider.setStyleSheet(sliderOffStyle)
            self.snrInput.setStyleSheet(numberInputOffStyle)
            self.snrEnable.setStyleSheet(labelOffStyle)


    def on_delete_clicked(self):
        self.deleteSignal.emit()