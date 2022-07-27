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
        # set the opacity
        try:
            opacity = float(config.mainWin.settingsPage.entries["opacity"].textEdit.toPlainText())
        except Exception as ex:
            opacity = 0.98
        
        config.settings.setValue("opacity", opacity)
        # infobar
        if config.mainWin.settingsPage.entries["infoBar"].textEdit.toPlainText() == "On":
            config.settings.setValue("infoBar", "True")
        else:
            config.settings.setValue("infoBar", "False")
        # aiplaceholder text
        if config.mainWin.settingsPage.entries["aiPlaceholderText"].textEdit.toPlainText() == "":
            config.settings.setValue("aiPlaceholderText", "Type any text here, and a passage will be generated!")
        else:
            config.settings.setValue("aiPlaceholderText", config.mainWin.settingsPage.entries["aiPlaceholderText"].textEdit.toPlainText())
        # text align
        if config.mainWin.settingsPage.entries["textAlign"].textEdit.toPlainText() == "On":
            config.settings.setValue("textAlign", "center")
        else:
            config.settings.setValue("textAlign", "left")
        # selected theme
        if "select a theme" not in config.mainWin.settingsPage.entries["selectedTheme"].themeDropdown.currentText().lower():
            config.settings.setValue("selectedTheme", config.mainWin.settingsPage.entries["selectedTheme"].themeDropdown.currentText())

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