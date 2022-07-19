from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config
import json

class SettingsSave(QPushButton):
    def __init__(self, parent):
        super(SettingsSave, self).__init__()
        self.parent = parent
        self.setFixedSize(100, 50)
        self.setText("Save")
        self.setStyleSheet("""
            background-color: """+config.textHighlight+""";
            color: """+config.backgroundColor+""";
            border-radius: 5px;
        """)
        self.clicked.connect(self.buttonPressed)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        # make the file not read only
        import os
        from stat import S_IRWXO
        os.chmod("settings/settings.json", S_IRWXO)
        # store all the changes in the settings file
        # open the settings file
        with open("settings/settings.json", "r") as settingsFile:
            # convert the json file into a dictionary
            settings = json.load(settingsFile)
        
        # set the opacity
        try:
            opacity = float(config.mainWin.settingsPage.entries["opacity"].textEdit.toPlainText())
        except Exception as ex:
            opacity = 0.98
        
        settings["opacity"] = opacity
        # infobar
        if config.mainWin.settingsPage.entries["infoBar"].textEdit.toPlainText() == "On":
            settings["infoBar"] = True
        else:
            settings["infoBar"] = False
        # aiplaceholder text
        if config.mainWin.settingsPage.entries["aiPlaceholderText"].textEdit.toPlainText() == "":
            settings["aiPlaceholderText"] = "Type any text here, and a passage will be generated!"
        else:
            settings["aiPlaceholderText"] = config.mainWin.settingsPage.entries["aiPlaceholderText"].textEdit.toPlainText()
        # text align
        if config.mainWin.settingsPage.entries["textAlign"].textEdit.toPlainText() == "On":
            settings["textAlign"] = "center"
        else:
            settings["textAlign"] = "left"
        # selected theme
        if "select a theme" not in config.mainWin.settingsPage.entries["selectedTheme"].themeDropdown.currentText().lower():
            settings["selectedTheme"] = config.mainWin.settingsPage.entries["selectedTheme"].themeDropdown.currentText()
        
        
        # finish editing the file
        with open("settings/settings.json", "w") as settingsFile:
            json.dump(settings, settingsFile, indent=4)
        
        # close the file
        settingsFile.close()

        # reload the settings in the config file
        config.reloadSettings()

        # show the selected options and suboptions
        optionType = None
        for suboption in config.subOptions:
            if suboption == config.selectedOption:
                optionType = suboption.type
        if optionType == None:
            # show the ai
            for option in config.options:
                option.show()
        else:
            for suboption in config.subOptions:
                if suboption.type == optionType:
                    suboption.show()
            for option in config.options:
                option.show()
        
        # move the stack to the typing page
        config.mainWin.stack.setCurrentIndex(0)
        # show the restart button
        config.mainWin.restart.show()
        # show the settings button
        config.mainWin.settingsButton.show()