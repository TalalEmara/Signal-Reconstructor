# Styles/ComposerStyling.py

composerTitleStyle = """
    QLabel#composerTitle {
        font-family: "Samsung Sans";
        font-size: 18px;
        font-weight: 600;
        color: #2252A0;
        padding: 5px 0;
    }
"""

comboBoxStyle = """
    QComboBox {
        color: #EFEFEF;
        background-color: #2252A0;
        border: 2px solid #174082;
        border-radius: 5px;
        padding: 5px;
    }
    QComboBox::down-arrow {
        color: #EFEFEF;
        width: 8px;
        height: 8px;
    }
    QComboBox QAbstractItemView {
        selection-background-color: #2252A0;
        selection-color: #FFFFFF;
    }
"""

doubleSpinBoxStyle = """
    QDoubleSpinBox {
        color: #2252A0;
        background-color: #FFFFFF;
        border: 2px solid #2252A0;
        border-radius: 5px;
        padding: 2px;
    }
"""

buttonStyle = """
    QPushButton {
        padding: 4px 8px;
        color: #EFEFEF;
        background-color: #2252A0;
        border: 2px solid #174082;
        border-radius: 5px;
    }
    QPushButton:hover {
        background-color: #1A5EB8;
        border-color: #1A5EB8;
    }
    QPushButton:pressed {
        background-color: #174082;
        border-color: #174082;
    }
"""

tableStyle = """
    QTableWidget {
        background-color: #FFFFFF;
        color: #2252A0;
        border: 1px solid #2252A0;
        gridline-color: #2252A0;
        selection-background-color: #1A5EB8;
        selection-color: #FFFFFF;
    }
    QHeaderView::section {
        background-color: #2252A0;
        color: #EFEFEF;
        padding: 4px;
        font-weight: 500;
        border: 1px solid #174082;
    }
"""
