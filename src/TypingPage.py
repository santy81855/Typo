from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QLineEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, LogOutButton

class TypingPage(QWidget):
    def __init__(self, parent):
        super(TypingPage, self).__init__()
        self.parent = parent
        # create the main layout to be horizontal so everything is centered
        self.layout = QVBoxLayout()
        # set the spacing
        self.layout.setSpacing(0)
        self.setLayout(self.layout)
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
