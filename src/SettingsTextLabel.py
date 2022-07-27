from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, RestartButton
import string

class SettingsTextLabel(QTextEdit):
    def __init__(self, parent, width, height, text):
        super(SettingsTextLabel, self).__init__()
        self.parent = parent
        self.width = width
        self.height = height
        self.text = text
        self.isButton = False
        self.isNumber = False
        if self.text == "infobar" or self.text == "textalign":
            self.isButton = True
            self.setReadOnly(True)
        if self.text == "opacity":
            self.isNumber = True
        self.setFixedSize(width, height)
        self.setMouseTracking(True)
    
    def keyPressEvent(self, event):
        # if being used as a button
        if self.isNumber == True:
            # only accept numbers
            if event.text().isdigit() == False and event.text() != "." and event.key() != 16777219: # allow backspace and periods
                return
            elif len(self.toPlainText()) == 4 and event.key() != 16777219: # if we have 4 digits and we are not backspacing
                return
            else:
                return QTextEdit.keyPressEvent(self, event)
        else:
            return QTextEdit.keyPressEvent(self, event)

    def mouseMoveEvent(self, event):
        # if this is the infobar then use this as a butten
        if self.isButton:
            QApplication.setOverrideCursor(Qt.PointingHandCursor)
        else:
            # make the cursor I beam if it is used as a text box
            QApplication.setOverrideCursor(Qt.IBeamCursor)

    def mouseDoubleClickEvent(self, event):
        if self.isButton:
            return
        else:
            return QTextEdit.mouseDoubleClickEvent(self,event)

    
    def mousePressEvent(self, event):
        # if this is being used as a button for the infobar
        if self.width == 60 and self.height == 40:
            # when we press it we want to alternate the text between on/off
            if self.toPlainText().lower() == "on":
                self.setText("Off")
            else:
                self.setText("On")
            self.setAlignment(Qt.AlignCenter)
