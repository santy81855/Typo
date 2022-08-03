from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QLineEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config

class LoginInput(QLineEdit):
    def __init__(self, parent, text, width, height):
        super(LoginInput, self).__init__()
        self.parent = parent
        self.setFixedSize(width, height)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 15 )
        self.setFont(font)
        # edit the stylesheet
        self.setStyleSheet("""
            background-color: white;
            color: """+config.backgroundColor+""";
            border: 2px solid """+config.textHighlight+""";
            border-radius: 5px;
        """)
        self.setPlaceholderText(text)
        # make the password input hidden
        if ("pass" in text.lower()):
            self.setEchoMode(QLineEdit.Password)

        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.IBeamCursor)

    def buttonPressed(self):
        print("hello")