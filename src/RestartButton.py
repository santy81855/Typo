from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
import config, Display

class RestartButton(QPushButton):
    def __init__(self, parent, text):
        super(RestartButton, self).__init__()
        self.parent = parent
        self.text = text
        self.setText(self.text)
        self.setStyleSheet("""
            background-color: """+config.accentColor+""";
            color: """+config.backgroundColor+""";
            border-radius: 10px;
            text-align: center;
        """)
        
        self.setFixedSize(200, 80)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 25 )
        self.setFont(font)
        self.setMouseTracking(True)
        self.pressed.connect(self.restart)
    
    def restart(self):
        global gettingInput
        global inputText
        # if we are not on index 0 of the stack then we want to switch to index 0
        if config.mainWin.stack.currentIndex() != 0:
            config.mainWin.stack.setCurrentIndex(0)
        if "ai" not in config.selectedOption.type.lower():
            self.parent.textDisplay.generatePassage()
            config.mainWin.textDisplay.setFocus(True)
        else:
            if config.gettingInput == True:
                self.setText("Restart")
                config.inputText = config.mainWin.textDisplay.toPlainText()
                self.parent.textDisplay.generatePassage()
                config.mainWin.textDisplay.setFocus(True)
                config.gettingInput = False
            else:
                # clear the input text
                config.inputText = ""
                self.setText("Generate")
                # prompt the user to enter text on the textbox
                config.mainWin.textDisplay.clear()
                config.mainWin.textDisplay.setReadOnly(False)
                config.mainWin.textDisplay.setPlaceholderText(config.aiPlaceholderText)
                config.mainWin.textDisplay.setFocus(True)
                config.gettingInput = True
    
    def mouseMoveEvent(self, event):
        # if the mouse is over the button, make it a hand cursor
        QApplication.setOverrideCursor(Qt.PointingHandCursor)