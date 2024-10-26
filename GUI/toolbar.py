from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QAction, QVBoxLayout, QWidget, QHBoxLayout, QSplitter, \
    QPushButton, QSlider, QLineEdit, QComboBox


class ToolBar(QWidget):
    def __init__(self):
        super().__init__()

        self.signalName = "s"
        self.nameLabel = QLabel(f"name: {self.signalName}")
        self.browseButton = QPushButton("Browse")
        self.samplingMethodLabel = QLabel("sampling method: ")
        self.samplingMethod = QComboBox()
        self.samplingRateLabel = QLabel("sampling rate: ")
        self.samplingRateInput = QLineEdit()

        self.snrLabel = QLabel("SNR: ")
        self.snrSlider = QSlider(Qt.Horizontal)
        self.snrInput = QLineEdit()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.nameLabel)
        self.layout.addWidget(self.browseButton)
        self.layout.addWidget(self.samplingMethodLabel)
        self.layout.addWidget(self.samplingMethod)
        self.layout.addWidget(self.samplingRateLabel)
        self.layout.addWidget(self.samplingRateInput)
        self.layout.addWidget(self.snrLabel)
        self.layout.addWidget(self.snrSlider)
        self.layout.addWidget(self.snrInput)

        self.setLayout(self.layout)