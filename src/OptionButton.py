from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
import config, Display

class OButton(QLabel):
    def __init__(self, parent, text, width):
        super(OButton, self).__init__()
        self.parent = parent
        self.text = text
        self.setText(text);
        if "words" in text:
            self.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.textHighlight + """;
                text-align: center;
                border: none;
            """)  
        else:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0);
                color: """ + config.accentColor1 + """;
                text-align: center;
                border: none;
            """)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        self.setFont(font)
        # set the size
        self.setFixedSize(width, 30)
        # variable to track whether its selected or not
        self.selected = False
        self.setMouseTracking(True)
    
    def mousePressEvent(self, event):
        # if we click the currently selected one then nothing should happen
        if self == config.selectedOption:
            return
        else:
            # make the currently selected option normal color
            config.selectedOption.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.accentColor1 + """;
                text-align: center;
                border: none;
            """)
            # make the new selection stand out
            self.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.textHighlight + """;
                text-align: center;
                border: none;
            """)            
            self.selected = True
            config.selectedOption.selected = False
            config.selectedOption = self
            config.textbox.generatePassage()
    
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)    