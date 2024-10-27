import os

import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, \
    QPushButton, QSlider, QLineEdit, QComboBox, QDoubleSpinBox, QFileDialog

from Styles.ToolBarStyling import toolBarStyle, buttonStyle, comboBoxStyle, sliderStyle, numberInputStyle
from PyQt5.QtGui import QIcon 

class ToolBar(QWidget):
    dataLoaded = pyqtSignal(pd.DataFrame)
    snrChanged = pyqtSignal(float)
    deleteSignal = pyqtSignal() 
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(toolBarStyle)

        self.signalName = "Default Signal"
        self.signalData = []

        self.nameLabel = QLabel("name: ")
        self.signalNameLabel = QLabel(self.signalName)
        self.signalNameLabel.setStyleSheet("color: black; font-size: 14px;")

        self.browseButton = QPushButton("Browse")
        self.browseButton.clicked.connect(self.loadSignal)

        self.deleteButton = QPushButton()  
        self.deleteButton.setIcon(QIcon('delete.png'))  
        self.deleteButton.setStyleSheet(buttonStyle)
        self.deleteButton.clicked.connect(self.on_delete_clicked) 


        self.browseButton.setStyleSheet(buttonStyle)
        self.samplingMethodLabel = QLabel("sampling method: ")
        self.samplingMethod = QComboBox()
        self.samplingMethod.setStyleSheet(comboBoxStyle)
        self.samplingMethod.addItem("Nyquist–Shannon")
        self.samplingMethod.addItem("second Method")
        self.samplingMethod.addItem("Third Method")

        self.samplingRateLabel = QLabel("sampling rate: ")
        self.samplingRateInput = QDoubleSpinBox()
        self.samplingRateInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.samplingRateInput.setAlignment(Qt.AlignCenter)
        self.samplingRateInput.setStyleSheet(numberInputStyle)
        self.samplingRateInput.setSuffix("Hz")


        self.snrLabel = QLabel("SNR: ")
        self.snrSlider = QSlider(Qt.Horizontal)
        self.snrSlider.setStyleSheet(sliderStyle)
        self.snrInput = QDoubleSpinBox()
        self.snrInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.snrInput.setAlignment(Qt.AlignCenter)
        self.snrInput.setStyleSheet(numberInputStyle)

        self.snrSlider.setRange(0, 30)

        self.snrInput.setRange(0, 30)
        self.snrSlider.setValue(30)
        self.snrInput.setDecimals(2)
        self.snrInput.setValue(30)
        self.snrInput.setAlignment(Qt.AlignCenter)

        self.snrSlider.valueChanged.connect(lambda value: self.snrInput.setValue(value / 1.0))  # Convert to float
        self.snrInput.valueChanged.connect(lambda value: self.snrSlider.setValue(int(value)))
        self.snrSlider.valueChanged.connect(self.on_snr_changed)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.nameLabel, 1)
        self.layout.addWidget(self.signalNameLabel, 1)
        self.layout.addStretch(1)
        self.layout.addWidget(self.browseButton, 5)
        self.layout.addWidget(self.deleteButton, 1) 
        self.layout.addStretch(2)
        self.layout.addWidget(self.samplingMethodLabel,3)
        self.layout.addWidget(self.samplingMethod,7)
        self.layout.addStretch(2)
        self.layout.addWidget(self.samplingRateLabel,5)
        self.layout.addWidget(self.samplingRateInput,5)
        self.layout.addStretch(2)
        self.layout.addWidget(self.snrLabel,2)
        self.layout.addWidget(self.snrSlider,8)
        self.layout.addWidget(self.snrInput,5)

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

    def on_snr_changed(self, value):
        self.snrChanged.emit(value / 1.0) 

    def on_delete_clicked(self):
        self.deleteSignal.emit()