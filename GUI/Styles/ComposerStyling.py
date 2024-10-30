
composerTitleStyle = """
    QLabel#composerTitle {
        font-family: "Samsung Sans";
        font-size: 30px;
        font-weight: 600;
        color: #2252A0;
        padding: 5px 0;
    }
"""

comboBoxStyle = """
    QComboBox {
        font-family: "Samsung Sans";
        font-size: 16px;
        color: #EFEFEF;  /* Text color for the combo box when closed */
        background-color: #2252A0;  /* Background color for the combo box */
        border: 1px solid #174082;
        border-radius: 5px;
        padding: 2px;
    }
    QComboBox::down-arrow {
        color: #EFEFEF;  /* Color of the dropdown arrow */
        width: 5px;
    }
    QComboBox QAbstractItemView {
        background-color: white;  /* Background color of the dropdown list */
        selection-background-color: #1A5EB8;  /* Background color when an item is selected */
        selection-color: white;  /* Text color when an item is selected */
        font-family: "Samsung Sans";
        font-size: 16px;
        color: #2252A0;  /* Text color for the items in the dropdown */
    }
    QComboBox QAbstractItemView::item {
        padding: 4px;  /* Padding for each item */
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
deleteButtonStyle = """
    QPushButton {
        background-color: white;  
        border-color: white;            
        outline: none;           
    }
    QPushButton:hover {
        background-color: #E3EEFF;  
    }
    QPushButton:pressed {
        background-color: #D0DAF0;  
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
        font-family: "Samsung Sans";
        font-size: 15px;
        alternate-background-color: #F2F7FF;  
    }
    QTableWidget::item {
        padding: 5px;
    }
    QTableWidget::item:selected {
        background-color: #1A5EB8; 
        color: #FFFFFF;
    }
    
    QHeaderView::section {
        background-color: #2252A0;
        color: #EFEFEF;
        padding: 6px;
        font-weight: 600;
        border: 1px solid #174082;
    }
     QTableWidget::item:focus {
        background-color: #D6E4FF;  
        color: #000000;             
        
    }

    QTableWidget QTableCornerButton::section {
        background-color: #2252A0;
        border: 1px solid #174082;
    }
    

    QTableWidget::item:hover {
        background-color: #E3EEFF; 
    }
    
    /* Scrollbar styling */
    QScrollBar:vertical {
        border: none;
        background: #D6D9E2;
        width: 10px;
        margin: 20px 0 20px 0;
    }
    QScrollBar::handle:vertical {
        background: #2252A0;
        min-height: 20px;
        border-radius: 5px;
    }
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        border: none;
        background: none;
        height: 0px;
    }
    QScrollBar::handle:vertical:hover {
        background: #1A5EB8;  
    }

    QTableWidget::item:nth-column(3) {
            background-color: none;
            border: none;
            
        }
"""
