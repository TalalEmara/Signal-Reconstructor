import os

import pandas as pd
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QWidget, QHBoxLayout, QPushButton, QSlider, QComboBox, QDoubleSpinBox, \
    QFileDialog, QCheckBox

from Styles.ToolBarStyling import toolBarStyle, buttonStyle, buttonWhiteStyle, comboBoxStyle, sliderOnStyle,sliderOffStyle, TitleStyle, labelOffStyle,labelOnStyle, numberInputOffStyle,samplingRateInputOnStyle,DoubleInputOnStyle


class ToolBar(QWidget):
    dataLoaded = pyqtSignal(pd.DataFrame)
    methodChanged = pyqtSignal(str)
    deleteSignal = pyqtSignal()

    samplingRateChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(toolBarStyle)

        self.signalName = "Default Signal"
        self.signalData = []
        # self.signalfMax = 100

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

        self.samplingMethodLabel = QLabel("reconstruction method: ")
        self.samplingMethod = QComboBox()
        self.samplingMethod.setStyleSheet(comboBoxStyle)
        self.samplingMethod.addItem("Whittaker-Shannon (sinc)")
        self.samplingMethod.addItem("Linear")
        self.samplingMethod.addItem("Zero-Order Hold")
        self.samplingMethod.addItem("Cubic-Spline")
        self.samplingMethod.currentIndexChanged.connect(self.onMethodChanged)

        self.rowLayout = QHBoxLayout()
        self.rowLayout.addWidget(self.title, 1)
        self.rowLayout.addWidget(self.nameLabel, 1)
        self.rowLayout.addWidget(self.signalNameLabel, 1)
        self.rowLayout.addWidget(self.browseButton, 5)
        self.rowLayout.addWidget(self.clearButton, 3)
        self.rowLayout.addStretch(1)
        self.rowLayout.addWidget(self.samplingMethodLabel,1)
        self.rowLayout.addWidget(self.samplingMethod,15)
        self.rowLayout.addStretch(30)


        self.layout = QVBoxLayout()
        self.layout.addLayout(self.rowLayout)
        self.setLayout(self.layout)

    def loadSignal(self):
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
                print(data)
            except Exception as e:
                print(f"Error loading CSV file: {e}")


    def onMethodChanged(self, value):
        self.methodChanged.emit(self.samplingMethod.currentText())


    def on_delete_clicked(self):
        self.deleteSignal.emit()