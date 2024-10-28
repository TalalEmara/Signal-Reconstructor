toolBarStyle = """
    QWidget{
        font-family: "Samsung Sans";
        font-size: 16px;
        font-weight: 500;
    
        color: #2252A0;
        
        
    
    }
"""
TitleStyle = """
    QLabel {
        font-family: "Samsung Sans";
        font-size: 34px;
        font-weight: bold;
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
buttonWhiteStyle = """
    QPushButton {
    padding: 4px 8px;
    color: #2252A0;
    background-color: #EFEFEF;
    border: 2px solid #2252A0;
    border-radius: 5px;  
}

    QPushButton:hover {
    background-color: #2B6FC1; 
    border-color: #2B6FC1;
    color: #FFFFFF;
}

    QPushButton:pressed {
    background-color: #1A4A87; 
    border-color: #1A4A87;
    color: #FFFFFF;
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
    
"""