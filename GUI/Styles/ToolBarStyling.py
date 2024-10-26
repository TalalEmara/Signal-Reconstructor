toolBarStyle = """
    QWidget{
        font-family: "Samsung Sans";
        font-size: 16px;
        font-weight: 500;
    
        color: #2252A0;
    
    }
"""
buttonStyle = """
    QPushButton {
        padding: 2px 2px;
        color: #EFEFEF;
        background-color: #2252A0;
        border: 3px solid #174082;
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

comboBoxStyle = """
    QComboBox{
        color: #EFEFEF;
        background-color: #2252A0;
        border: 1px solid #174082;
        border-radius: 5px;  
    }
    QComboBox::down-arrow {
    color:#EFEFEF;
    width:5px;
    }
    
    QComboBox QAbstractItemView {
    selection-background-color: #2252A0; 
    selection-color: white;      
}

"""
sliderStyle = """
QSlider::handle {
            background-color: #2252A0;
            width: 5px;
            height: 7px;
            border-radius: 5px;
        }
        """

numberInputStyle = """
    QDoubleSpinBox{
        color: #2252A0;
        padding:2px;
        border: 2px solid #2252A0;
        border-radius: 5px;  
    }
    QDoubleSpinBox::up-button {
    }
    
    QDoubleSpinBox::down-button {
        background-color: #2252A0; /* Background color of the down button */
        border: none;               /* No border */
}
"""