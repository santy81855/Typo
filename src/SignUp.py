from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config

class SignUpButton(QPushButton):
    def __init__(self, parent, text, width, height):
        super(SignUpButton, self).__init__()
        self.text = text
        self.parent = parent
        self.setFixedSize(width, height)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 10 )
        font.setUnderline(True)
        self.setFont(font)
        self.setText(text)
        self.setStyleSheet("""
            background-color: """+config.backgroundColor+""";
            color: """+config.textHighlight+""";
            border-radius: 5px;
        """)
        self.clicked.connect(self.buttonPressed)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        # if its the sign-up button take them to sign up page
        if "up" in self.text.lower():
            # snap in place
            config.mainWin.snapWin("place")
            # change the stack to the signup page
            config.mainWin.stack.setCurrentIndex(1)
        # if it's the signin button take them to log in page
        else:
            # change the stack to the login page
            config.mainWin.stack.setCurrentIndex(0)