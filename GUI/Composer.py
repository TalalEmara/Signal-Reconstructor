from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QComboBox, QDoubleSpinBox, QTableWidget, QVBoxLayout, QHBoxLayout, \
    QPushButton, QHeaderView,QTableWidgetItem, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal,QSize
from Styles.ComposerStyling import composerTitleStyle, comboBoxStyle, doubleSpinBoxStyle, buttonStyle, tableStyle,deleteButtonStyle
from PyQt5.QtGui import QIcon

class Composer(QWidget):
    valueAdded = pyqtSignal(float, float,str)
    valueUpdated = pyqtSignal(int, float, float, str)
    valueRemoved = pyqtSignal(float, float, str, int)

    def __init__(self):
        super().__init__()
        self.composerTitle = QLabel("Signal Mixer")
        self.composerTitle.setObjectName("composerTitle")
        self.composerTitle.setAlignment(Qt.AlignCenter)
        self.composerTitle.setStyleSheet(composerTitleStyle)

        self.functionType = QComboBox()
        self.functionType.setStyleSheet(comboBoxStyle)
        self.functionType.addItem('sin')
        self.functionType.addItem('cos')
        self.functionType.addItem('square')
        self.functionType.addItem('triangular')

        self.amplitudeLabel = QLabel("Amplitude")
        self.amplitudeInput = QDoubleSpinBox()
        self.amplitudeInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.amplitudeInput.setStyleSheet(doubleSpinBoxStyle)

        self.frequencyLabel = QLabel("Frequency")
        self.frequencyInput = QDoubleSpinBox()
        self.frequencyInput.setButtonSymbols(QDoubleSpinBox.NoButtons)
        self.frequencyInput.setRange(0, float('inf'))
        self.frequencyInput.setSuffix("Hz")
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
        if amplitude == 0 or frequency == 0:
            return
        signal_type = self.functionType.currentText()
        self.valueAdded.emit(amplitude, frequency,signal_type)
        self.add_to_table(signal_type, amplitude, frequency)

    def add_to_table(self, signal_type, amplitude, frequency):
        row = self.componentsTable.rowCount()
        self.componentsTable.insertRow(row)

        self.componentsTable.setItem(row, 0, QTableWidgetItem(signal_type))
        self.componentsTable.setItem(row, 1, QTableWidgetItem(str(amplitude)))
        self.componentsTable.setItem(row, 2, QTableWidgetItem(str(frequency)))

        delete_button = QPushButton("X")  # Create a button without a text label
        # delete_button.setIcon(QIcon("GUI/Styles/Icons/delete3.png"))
        # delete_button.setIconSize(QSize(20, 20))
        delete_button.setStyleSheet("""
        color: red;
        background-color: white;
        font-size: 14px;
        border: none;
        
        """)
        # delete_button.setFixedSize(30, 30)  # Set a fixed size for the button
        button_widget = QWidget()
        button_widget.setStyleSheet("""
        color = red;
        background-color:white;
        font-size:14px;
        border-color:white;
        
        """)
        button_layout = QHBoxLayout(button_widget)
        button_layout.addWidget(delete_button)
        button_layout.setAlignment(Qt.AlignCenter)  # Center the button
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove spacing around the button

        print(row, amplitude, frequency, signal_type)

        delete_button.clicked.connect(lambda _, btn=delete_button: self.remove_row_by_button(
            btn, amplitude=amplitude, frequency=frequency, signal_type=signal_type
        ))

        self.componentsTable.setCellWidget(row, 3, button_widget)

    def remove_row_by_button(self, button, amplitude, frequency, signal_type):
        # Get the row of the button clicked
        index = self.componentsTable.indexAt(button.parentWidget().pos())
        row = index.row()

        if row != -1:  # Ensure it's a valid row
            self.remove_from_table(row, amplitude, frequency, signal_type)

    def remove_from_table(self, row, amplitude, frequency, signal_type):
        # Additional code to handle removal logic here
        self.componentsTable.removeRow(row)
        self.valueRemoved.emit(amplitude, frequency, signal_type, self.componentsTable.rowCount())

        print(f"Row {row} removed with amplitude={amplitude}, frequency={frequency}, signal_type={signal_type}")

    def handle_table_edit(self, row, column):
        signal_type = self.componentsTable.item(row, 0).text()

        if self.componentsTable.item(row, 1):
            amplitude = float(self.componentsTable.item(row, 1).text())
        else:
            amplitude = amplitude

        if self.componentsTable.item(row, 2):
            frequency = float(self.componentsTable.item(row, 2).text())
        else:
            frequency = frequency

        self.valueUpdated.emit(row, amplitude, frequency, signal_type)

        self.update_delete_button(row, amplitude, frequency, signal_type)

    def update_delete_button(self, row, amplitude, frequency, signal_type):
        # Access the delete button in the specified row
        button_widget = self.componentsTable.cellWidget(row, 3)
        if button_widget:
            delete_button = button_widget.findChild(QPushButton)  # Get the delete button
            if delete_button:
                # Update the connection to pass the new values
                delete_button.clicked.disconnect()  # Disconnect previous connections
                delete_button.clicked.connect(lambda _: self.remove_row_by_button(
                    delete_button, amplitude=amplitude, frequency=frequency, signal_type=signal_type
                ))

    def clear_table(self):
        self.componentsTable.setRowCount(0)