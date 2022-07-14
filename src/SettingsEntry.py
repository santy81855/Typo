from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QComboBox
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, BrowseButton, SettingsTextLabel, SettingsSave
import json
# open the settings file
settingsFile = open("settings/settings.json", "r")
# convert the json file into a dictionary
settings = json.load(settingsFile)

class SettingsEntry(QWidget):
    def __init__(self, parent, key):
        super(SettingsEntry, self).__init__()
        self.parent = parent
        self.key = key
        self.setMouseTracking(True)
        # create a horizontal layout
        self.layout = QHBoxLayout()
        # set the spacing
        self.layout.setSpacing(10)
        # add a stretch to the layout
        #self.layout.addStretch(-1)
        # set the layout
        self.setLayout(self.layout)
        # add a label for the key
        self.label = QLabel("")
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        self.label.setFont(font)
        # edit the stylesheet
        self.label.setStyleSheet("""
            background-color: """+config.backgroundColor+""";
            color: """+config.accentColor+""";
            border: none;
        """)

        if key in settings:
            # get the type of the setting
            settingType = type(settings[key])
            # get the content of the setting
            content = str(settings[key])

        # if the content is a string then we just need a QplainTextEdits
        # although wordlist is a string, we want a qfiledialog
        if "wordlist" in key.lower():
            # set the label text
            self.label.setText("Word List: ")
            # create a qlabel for the path
            self.pathLabel = QLabel(content.split("/")[-1])
            # set the font 
            self.pathLabel.setFont(font)
            # make it bigger
            self.pathLabel.setFixedHeight(50)
            self.pathLabel.setFixedWidth(320)
            # make the background white 
            self.pathLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.textHighlight+""";
            """)

            # create a browse button
            self.browseButton = BrowseButton.BrowseButton(self, "Browse")
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.pathLabel)
            self.layout.addWidget(self.browseButton)

        elif "opacity" in key.lower():
            self.label.setText("Opacity: ")
            self.textEdit = SettingsTextLabel.SettingsTextLabel(self, 80, 50, "opacity")
            self.textEdit.setPlaceholderText(content)

            self.textEdit.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.textHighlight+""";
                text-align: center;
            """)
            self.textEdit.setFont(font)
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.textEdit)
        
        elif "infobar" in key.lower():
            self.label.setText("Bottom Bar: (requires restart)")
            self.textEdit = SettingsTextLabel.SettingsTextLabel(self, 60, 40, "infobar")
            if settings[key] == True:
                self.textEdit.setText("On")
            else:
                self.textEdit.setText("Off")
            self.textEdit.setAlignment(Qt.AlignCenter)
            self.textEdit.setFont(font)
            self.textEdit.setStyleSheet("""
                background-color:"""+config.textHighlight+""";
                color: """+config.backgroundColor+""";
                border-radius: 5px;
                text-align: center;
            """)
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.textEdit)
        
        elif "aiplaceholdertext" in key.lower():
            # since the placeholder text can be a bit wordy we can make it a vertical layout
            self.vertLayout = QVBoxLayout()
            self.vertLayout.setSpacing(5)
            self.label.setText("AI Placeholder Text: ")
            self.textEdit = SettingsTextLabel.SettingsTextLabel(self, 400, 100, "aiplaceholdertext")
            self.textEdit.setPlaceholderText(content)
            self.textEdit.setFont(font)
            self.textEdit.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.textHighlight+""";
                text-align: center;
            """)
            self.vertLayout.addWidget(self.label)
            self.vertLayout.addWidget(self.textEdit)
            self.layout.addLayout(self.vertLayout)
        
        elif "textalign" in key.lower():
            self.label.setText("Align Text Center: ")
            self.textEdit = SettingsTextLabel.SettingsTextLabel(self, 60, 40, "textalign")
            self.textEdit.setText("On")
            self.textEdit.setAlignment(Qt.AlignCenter)
            self.textEdit.setFont(font)
            self.textEdit.setStyleSheet("""
                background-color:"""+config.textHighlight+""";
                color: """+config.backgroundColor+""";
                border-radius: 5px;
                text-align: center;
            """)
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.textEdit)
        
        elif "selectedtheme" in key.lower():
            self.label.setText("Selected Theme: (requires restart)")
            # create the dropdown menu
            self.themeDropdown = QComboBox()
            # set the size of the month select dropdown menu
            self.themeDropdown.setFixedHeight(50)
            self.themeDropdown.setFixedWidth(300)
            self.themeDropdown.setFont(font)
            # add the months to the combobox
            self.themeDropdown.addItem('Select a theme: ')
            # for every theme available in the json we will add a new item to the dropdown
            for theme in settings["themes"]:
                self.themeDropdown.addItem(theme)
            self.themeDropdown.setStyleSheet("""
                text-align:center;
                border: 2px solid """+config.textHighlight+""";
                color: black;
                background-color: white;
            """)
            
            self.layout.addWidget(self.label)
            self.layout.addWidget(self.themeDropdown)
        
        elif "save" in key.lower():
            # add a button to save the settings
            self.save = SettingsSave.SettingsSave(self)
            # place the button in a horizontal layout
            self.hor = QHBoxLayout()
            self.hor.addStretch(-1)
            self.hor.addWidget(self.save)
            self.hor.addStretch(-1)
            # add the horizontal layout to the layout
            self.layout.addLayout(self.hor)

        # add stretch to center settings
        self.layout.addStretch(-1)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)