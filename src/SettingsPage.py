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
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        font.setBold( True )
        # center the whole thing
        self.mainLayout = QHBoxLayout()
        self.mainLayout.addStretch(-1)
        self.parent = parent
        # create a vertical layout
        self.layout = QVBoxLayout()
        # set the spacing
        self.layout.setSpacing(10)

        # add a title to the settings page
        self.title = QLabel("Settings")
        self.title.setStyleSheet("color: "+config.accentColor+";")
        self.title.setFont(font)
        # add save button to horizontal layout to center it
        self.titleLayout = QHBoxLayout()
        self.titleLayout.addStretch(-1)
        self.titleLayout.addWidget(self.title)
        self.titleLayout.addStretch(-1)
        self.layout.addLayout(self.titleLayout)

        settings = config.settings.allKeys()

        # display all settings and store each settings entry in a dictionary
        self.entries = {}
        self.layout.addStretch(-1)
        for item in settings:
            if item != "themes" and item != "symbols":
                self.entries[item] = SettingsEntry.SettingsEntry(self, item)
                self.layout.addWidget(self.entries[item])
        
        #self.saveButton = SettingsEntry.SettingsEntry(self, "save")
        self.saveButton = SettingsSave.SettingsSave(self, "Save")
        self.backButton = SettingsSave.SettingsSave(self, "Back")

        # add bothe buttons to a holrizontal layout
        self.horLayout = QHBoxLayout()
        self.horLayout.setSpacing(10)
        self.horLayout.addStretch(-1)
        self.horLayout.addWidget(self.backButton)
        self.horLayout.addWidget(self.saveButton)
        self.horLayout.addStretch(-1)
        
        # add the button layout to the main layout
        self.layout.addStretch(-1)
        self.layout.addLayout(self.horLayout)
        #self.layout.setAlignment(self.saveButton, Qt.AlignHCenter)
        self.layout.addStretch(-1)

        self.mainLayout.addLayout(self.layout)
        self.mainLayout.addStretch(-1)

        # set the layout
        self.widget.setLayout(self.mainLayout)
        # set the widget of the scrollarea
        self.setWidget(self.widget)



        
