from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QDoubleSpinBox, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QHeaderView,QTableWidgetItem
from PyQt5.QtCore import Qt, pyqtSignal
from Styles.ComposerStyling import composerTitleStyle, comboBoxStyle, doubleSpinBoxStyle, buttonStyle, tableStyle


class Composer(QWidget):
    valueAdded = pyqtSignal(float, float,str)
    valueUpdated = pyqtSignal(int, float, float, str)
    def __init__(self):
        super().__init__()
        self.composerTitle = QLabel("Mixer")
        self.composerTitle.setObjectName("composerTitle")  
        self.composerTitle.setStyleSheet(composerTitleStyle)

        self.functionType = QComboBox()
        self.functionType.setStyleSheet(comboBoxStyle) 
        self.functionType.addItem('sin')
        self.functionType.addItem('cos')
        self.functionType.addItem('square')
        self.functionType.addItem('triangular')

        self.amplitudeLabel = QLabel("Amplitude")
        self.amplitudeInput = QDoubleSpinBox()
        self.amplitudeInput.setStyleSheet(doubleSpinBoxStyle)

        self.frequencyLabel = QLabel("Frequency")
        self.frequencyInput = QDoubleSpinBox()
        self.frequencyInput.setStyleSheet(doubleSpinBoxStyle)

        self.addButton = QPushButton("Add")
        self.addButton.setStyleSheet(buttonStyle) 

        self.componentsTable = QTableWidget()
        self.componentsTable.setColumnCount(4)
        self.componentsTable.setHorizontalHeaderLabels(["Type", "Amplitude", "Frequency", ""])
        self.componentsTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.componentsTable.setStyleSheet(tableStyle)
        
        self.header = self.componentsTable.horizontalHeader()
        self.header.setSectionResizeMode(0, QHeaderView.Stretch)
        self.header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.header.setSectionResizeMode(3, QHeaderView.Fixed)


        self.componentsTable.setColumnWidth(3,50)


        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.composerTitle)

        self.addComponentLayout = QHBoxLayout()
        self.addComponentLayout.addWidget(self.functionType)
        self.addComponentLayout.addWidget(self.amplitudeLabel)
        self.addComponentLayout.addWidget(self.amplitudeInput)
        self.addComponentLayout.addWidget(self.frequencyLabel)
        self.addComponentLayout.addWidget(self.frequencyInput)
        self.addComponentLayout.addWidget(self.addButton)

        self.mainLayout.addLayout(self.addComponentLayout)
        self.mainLayout.addWidget(self.componentsTable)

        self.setLayout(self.mainLayout)

        self.addButton.clicked.connect(self.emit_values)
        self.componentsTable.cellChanged.connect(self.handle_table_edit)

    def emit_values(self):
        amplitude = self.amplitudeInput.value()
        frequency = self.frequencyInput.value()
        signal_type = self.functionType.currentText()
        self.valueAdded.emit(amplitude, frequency,signal_type)
        self.add_to_table(signal_type, amplitude, frequency) 

    def add_to_table(self, signal_type, amplitude, frequency):
        row = self.componentsTable.rowCount()
        self.componentsTable.insertRow(row)

        self.componentsTable.setItem(row, 0, QTableWidgetItem(signal_type))
        self.componentsTable.setItem(row, 1, QTableWidgetItem(str(amplitude)))
        self.componentsTable.setItem(row, 2, QTableWidgetItem(str(frequency)))
    
    def handle_table_edit(self, row, column):
        try:
            signal_type = self.componentsTable.item(row, 0).text()
            amplitude = float(self.componentsTable.item(row, 1).text())
            frequency = float(self.componentsTable.item(row, 2).text())
            self.valueUpdated.emit(row, amplitude, frequency, signal_type)
        except ValueError:
            
            pass