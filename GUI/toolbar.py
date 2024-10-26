from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, \
    QPushButton, QSlider, QLineEdit, QComboBox, QDoubleSpinBox

from Styles.ToolBarStyling import toolBarStyle, buttonStyle, comboBoxStyle, sliderStyle, numberInputStyle


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(toolBarStyle)

        self.signalName = "s"
        self.nameLabel = QLabel(f"name: {self.signalName}")
        self.browseButton = QPushButton("Browse")
        self.browseButton.setStyleSheet(buttonStyle)
        self.samplingMethodLabel = QLabel("sampling method: ")
        self.samplingMethod = QComboBox()
        self.samplingMethod.setStyleSheet(comboBoxStyle)
        self.samplingMethod.addItem("hshas")
        self.samplingMethod.addItem("aa")

        self.samplingRateLabel = QLabel("sampling rate: ")
        self.samplingRateInput = QDoubleSpinBox()

        self.snrLabel = QLabel("SNR: ")
        self.snrSlider = QSlider(Qt.Horizontal)
        self.snrSlider.setStyleSheet(sliderStyle)
        self.snrInput = QDoubleSpinBox()
        self.snrInput.setAlignment(Qt.AlignCenter)
        self.snrInput.setStyleSheet(numberInputStyle)

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.nameLabel,10)
        self.layout.addWidget(self.browseButton,5)
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