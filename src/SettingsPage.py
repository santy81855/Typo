from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, SettingsEntry, SettingsSave
import json

class SettingsPage(QWidget):
    def __init__(self, parent):
        super(SettingsPage, self).__init__()
        self.parent = parent
        # create a vertical layout
        self.layout = QHBoxLayout()
        # set the spacing
        self.layout.setSpacing(10)
        # set the layout
        self.setLayout(self.layout)
        # split the page into left and right
        self.left = QVBoxLayout()
        self.left.setSpacing(0)
        self.right = QVBoxLayout()

        settings = config.settings.allKeys()

        # display all settings and store each settings entry in a dictionary
        self.entries = {}
        self.left.addStretch(-1)
        for item in settings:
            if item != "themes" and item != "symbols":
                self.entries[item] = SettingsEntry.SettingsEntry(self, item)
                self.left.addWidget(self.entries[item])
        self.left.addStretch(-1)
        self.right.addWidget(SettingsEntry.SettingsEntry(self, "save"))
        

        # add the left and right layouts to the main layout
        self.layout.addLayout(self.left)
        self.layout.addLayout(self.right)



        
