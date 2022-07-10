from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
import config, Display
import json
# open the settings file
settingsFile = open("settings/settings.json", "r")
# convert the json file into a dictionary
settings = json.load(settingsFile)

class OButton(QLabel):
    def __init__(self, parent, text, width, isOption, textType):
        super(OButton, self).__init__()
        self.parent = parent
        self.text = text
        self.type = textType
        self.isOption = isOption
        global selectedOption
        # we default to the word option so we preselect it when we create it
        if self.type == "words" and self.isOption == True: 
            self.setStyleSheet("""
                background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
                text-align: center;
                border: none;
            """)  
            self.setText("words");
        
        elif self.type == "time" and self.isOption == True:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0);
                color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                text-align: center;
                border: none;
            """)
            self.setText("time");

        # we default to 10 words so we select it when we create the 10 words suboption
        elif isOption == False and "words" in self.type and self.text == "10":
            self.setStyleSheet("""
                background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
                text-align: center;
                border: none;
            """)  
            config.selectedOption = self
            self.setText(self.text)

        else:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0);
                color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                text-align: center;
                border: none;
            """)
            self.setText(text);

        

        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        if isOption == True:
            font.setPointSize( config.optionButtonSize )
        else:
            font.setPointSize( config.subOptionButtonSize )
        self.setFont(font)
        # set the size
        self.setFixedSize(width, 30)
        # variable to track whether its selected or not
        self.selected = False
        self.setMouseTracking(True)

    def changeSelection(self, selection, suboptionSelection):
        # make all the buttons normal
        for i in range(0, len(config.options)):
            config.options[i].setStyleSheet("""
                background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                text-align: center;
                border: none;
            """)
        # do the same for the suboptions
        for i in range(0, len(config.subOptions)):
            config.subOptions[i].setStyleSheet("""
                background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                text-align: center;
                border: none;
            """)

        # make the selected option stand out
        selection.setStyleSheet("""
            background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
            color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
            text-align: center;
            border: none;
        """)
        if suboptionSelection != None:
            suboptionSelection.setStyleSheet("""
                background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
                text-align: center;
                border: none;
            """)
    
    def mousePressEvent(self, event):
        global selectedOption
        global numWords
        global numTime
        # if we click the currently selected one then nothing should happen
        if self == config.selectedOption and "ai" not in self.type:
            return
        # if we clicked an option button
        elif self.isOption == True:
            # set the restart button to say "restart"
            config.mainWin.restart.setText("Restart")
            # set the getting input to false
            config.gettingInput = False
            # choose the first suboption by default
            suboptionSelection = None
            # if we clicked the words option
            if self.type == "words":
                # make the time options invisible
                for i in range(4, len(config.subOptions)):
                    config.subOptions[i].setVisible(False)
                # show the word options
                for i in range(0, 4):
                    config.subOptions[i].setVisible(True)
                suboptionSelection = config.subOptions[0]
                # make the new selection stand out
                self.changeSelection(self, suboptionSelection)
                config.subOptions[0].selected = True
                config.selectedOption.selected = False
                config.selectedOption = config.subOptions[0]
                config.textbox.generatePassage()
            # if we clicked the time option
            elif self.type == "time":
                # set the restart button to say "restart"
                config.mainWin.restart.setText("Restart")
                # set the getting input to false
                config.gettingInput = False
                # make the time options visible
                for i in range(4, len(config.subOptions)):
                    config.subOptions[i].setVisible(True)
                # hide the word suboptions
                for i in range(0, 4):
                    config.subOptions[i].setVisible(False)
                suboptionSelection = config.subOptions[4]
                # make the new selection stand out
                self.changeSelection(self, suboptionSelection)
                config.subOptions[4].selected = True
                config.selectedOption.selected = False
                config.selectedOption = config.subOptions[4]
                config.textbox.generatePassage()
            # if we click the AI button
            else:
                # clear the inputText
                config.inputText = ""
                # hide all suboptions
                for i in range(0, len(config.subOptions)):
                    config.subOptions[i].setVisible(False)
                # make the new selection stand out
                self.changeSelection(self, None)
                config.selectedOption.selected = False
                self.selected = True
                config.selectedOption = self
                # set the getting input button to true
                config.gettingInput = True
                # set the restart button to say "generate"
                config.mainWin.restart.setText("Generate")
                # prompt the user to enter text on the textbox
                config.mainWin.textDisplay.clear()
                config.mainWin.textDisplay.setReadOnly(False)
                config.mainWin.textDisplay.setPlaceholderText(settings["aiPlaceholderText"])
                # set focus to the textbox
                config.mainWin.textDisplay.setFocus(True)
            
        # if we clicked a suboption
        elif self.isOption == False:
            # if it is a suboption for words
            if "words" in self.type:
                # set the number of words to the number of words in the suboption
                config.numWords = int(self.text)
                # make all the other word suboptions normal and make this one stand out
                for i in range(0, 4):
                    config.subOptions[i].setStyleSheet("""
                        background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                        color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                        text-align: center;
                        border: none;
                    """)
                # make the new selection stand out
                self.setStyleSheet("""
                    background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                    color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
                    text-align: center;
                    border: none;
                """)      
  
                self.selected = True
                config.selectedOption.selected = False
                config.selectedOption = self
                config.textbox.generatePassage()
            
            elif "time" in self.type:
                # set the time
                config.numTime = int(self.text)
                # make all the other word suboptions normal and make this one stand out
                for i in range(4, len(config.subOptions)):
                    config.subOptions[i].setStyleSheet("""
                        background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                        color: """ + settings["themes"][settings["selectedTheme"]]["accentColor"] + """;
                        text-align: center;
                        border: none;
                    """)
                # make the new selection stand out
                self.setStyleSheet("""
                    background-color: """ + settings["themes"][settings["selectedTheme"]]["backgroundColor"] + """;
                    color: """ + settings["themes"][settings["selectedTheme"]]["textHighlight"] + """;
                    text-align: center;
                    border: none;
                """)      
  
                self.selected = True
                config.selectedOption.selected = False
                config.selectedOption = self
                config.textbox.generatePassage()
            
            #*** this is where the ai stuff goes ***#
            else:
                print("ai suboptions")

    
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)    