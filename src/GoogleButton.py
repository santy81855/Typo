from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir, QSize
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon, QPixmap
import config

class GoogleButton(QPushButton):
    def __init__(self, parent, text, width, height):
        super(GoogleButton, self).__init__()
        self.parent = parent
        self.setFixedSize(width, height)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        self.setFont(font)
        self.setText(text)
        pixmap = QPixmap("images/GoogleLogo.png");
        buttonIcon = QIcon(pixmap);
        self.setIcon(buttonIcon)
        self.setIconSize(QSize(30, 30))
        self.setStyleSheet("""
            background-color: """+config.googleButtonBackground+""";
            color: """+config.backgroundColor+""";
            border-radius: 5px;
        """)
        self.clicked.connect(self.buttonPressed)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        print("google")