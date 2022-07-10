import sys
from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QScrollBar, QApplication
import config
import json
# open the settings file
settingsFile = open("settings/settings.json", "r")
# convert the json file into a dictionary
settings = json.load(settingsFile)

class ScrollBar(QScrollBar):
    def __init__(self, parent):
        super(ScrollBar, self).__init__()
        self.parent = parent
        self.setMouseTracking(True)
        self.setTracking(True)
        #self.setMinimumWidth(14)
        #self.setMaximumWidth(14)
        self.setStyleSheet("""
        QScrollBar::vertical
        {
            border:none;
            width: """ + str(config.scrollBarWidth) + """px;
        }
        QScrollBar::horizontal
        {
            border:none;
            height: """ + str(config.scrollBarWidth) + """px;
        }
        QScrollBar::add-line:vertical
        {
            border:none;
            background:none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::sub-line:vertical
        {
            border:none;
            background:none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::add-line:horizontal
        {
            border:none;
            background:none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::sub-line:horizontal
        {
            border:none;
            background:none;
            width: 0px;
            height: 0px;
        }
        QScrollBar::handle:vertical
        {
            background-color:"""+str(settings["themes"][settings["selectedTheme"]]["backgroundColor"])+"""; 
            border:none;  
        }
        QScrollBar::handle:horizontal
        {
            background-color:"""+str(settings["themes"][settings["selectedTheme"]]["backgroundColor"])+"""; 
            border:none;  
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical 
        {
            background: none;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:horizontal
        {
            background: none;
        }
                            """)
        #3B4252
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)