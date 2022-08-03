from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit, QScrollArea
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, SettingsEntry, SettingsSave, ScrollBar

class SettingsPage(QScrollArea):
    def __init__(self, parent):
        super(SettingsPage, self).__init__()
        self.setWidgetResizable(True)
        # create a new scrollbar that looks nicer
        self.scrollbarV = ScrollBar.ScrollBar(self)
        self.scrollbarH = ScrollBar.ScrollBar(self)
        self.setVerticalScrollBar(self.scrollbarV)
        self.setHorizontalScrollBar(self.scrollbarH)
        self.widget = QWidget()
        # center the whole thing
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addStretch(-1)
        self.parent = parent
        # create a vertical layout
        self.layout = QVBoxLayout()
        # set the spacing
        self.layout.setSpacing(10)

        settings = config.settings.allKeys()

        # display all settings and store each settings entry in a dictionary
        self.entries = {}
        self.layout.addStretch(-1)
        for item in settings:
            if item != "themes" and item != "symbols":
                self.entries[item] = SettingsEntry.SettingsEntry(self, item)
                self.layout.addWidget(self.entries[item])
        
        # add save button to horizontal layout to center it
        self.horLayout = QHBoxLayout()
        self.horLayout.addStretch(-1)
        self.horLayout.addWidget(SettingsEntry.SettingsEntry(self, "save"))
        self.horLayout.addStretch(-1)
        
        # add the horizontal layout to the vertical layout
        self.layout.addStretch(-1)
        self.layout.addLayout(self.horLayout)
        self.layout.addStretch(-1)

        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addStretch(-1)

        print(self.parent.stack.width())
        print(self.width())
        # set the layout
        self.widget.setLayout(self.mainLayout)
        # set the widget of the scrollarea
        self.setWidget(self.widget)



        
