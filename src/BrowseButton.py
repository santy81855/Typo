from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, RestartButton

class BrowseButton(QPushButton):
    def __init__(self, parent, text):
        super(BrowseButton, self).__init__()
        self.parent = parent
        self.text = text
        # create the browse button
        self.setText(text)
        self.clicked.connect(self.pressedBrowse)
        # set the size of the browse button
        self.setFixedHeight(50)
        self.setFixedWidth(100)
        #border: none;
        #vertical-align: top;
        #text-align:center;
        self.setStyleSheet("""
            text-align:center;
            border-radius: 5px;
            color: """+config.backgroundColor+""";
            background-color: """+ config.textHighlight +""";
        """)
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 15 )
        self.setFont(font)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        # make the cursor pointing hand
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    
    def pressedBrowse(self):
        # open the directory to the /words folder so they can select one of the default ones
        fileName=QFileDialog.getOpenFileName(self, 'open file', QDir.currentPath() + "/words", 'TXT files (*.txt)')
        # display only the last part of the path
        self.parent.pathLabel.setText(fileName[0].split("/")[-1])

        # open the settings file
        with open("settings/settings.json", "r") as settingsFile:
            # convert the json file into a dictionary
            settings = json.load(settingsFile)
        
        # change the path of the wordlist
        if fileName[0] != "":
            settings[self.parent.key] = fileName[0]
        
        # finish editing the file
        with open("settings/settings.json", "w") as settingsFile:
            json.dump(settings, settingsFile, indent=4)
        
        # close the file
        settingsFile.close()

        # reload the settings in the config file
        config.reloadSettings()

        # generate a new passage
        config.mainWin.textDisplay.generatePassage()
        