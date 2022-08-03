from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QFont
import urllib.request
import config, Display

class OButton(QLabel):
    def __init__(self, parent, text, width, isOption, textType):
        super(OButton, self).__init__()
        self.parent = parent
        self.buttonText = text
        self.type = textType
        self.isOption = isOption
        global selectedOption
        # we default to the word option so we preselect it when we create it
        if self.type == "words" and self.isOption == True: 
            self.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.textHighlight + """;
                text-align: center;
                border: none;
            """)  
            self.setText("words");
        
        elif self.type == "time" and self.isOption == True:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0);
                color: """ + config.accentColor + """;
                text-align: center;
                border: none;
            """)
            self.setText("time");

        # we default to 10 words so we select it when we create the 10 words suboption
        elif isOption == False and "words" in self.type and self.buttonText == "10":
            self.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.textHighlight + """;
                text-align: center;
                border: none;
            """)  
            config.selectedOption = self
            self.setText(self.buttonText)

        else:
            self.setStyleSheet("""
                background-color: rgba(0,0,0,0);
                color: """ + config.accentColor + """;
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
        # get the width of the text
        textWidth = self.fontMetrics().width(self.text())
        # set the width to be the width of the text
        self.setFixedSize(textWidth + 5, 30)
        #self.setMinimumSize(1, 30)
        # variable to track whether its selected or not
        self.selected = False
        self.setMouseTracking(True)

    def changeSelection(self, selection, suboptionSelection):
        # make all the buttons normal
        for i in range(0, len(config.options)):
            config.options[i].setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.accentColor + """;
                text-align: center;
                border: none;
            """)
        # do the same for the suboptions
        for i in range(0, len(config.subOptions)):
            config.subOptions[i].setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.accentColor + """;
                text-align: center;
                border: none;
            """)

        # make the selected option stand out
        selection.setStyleSheet("""
            background-color: """ + config.backgroundColor + """;
            color: """ + config.textHighlight + """;
            text-align: center;
            border: none;
        """)
        if suboptionSelection != None:
            suboptionSelection.setStyleSheet("""
                background-color: """ + config.backgroundColor + """;
                color: """ + config.textHighlight + """;
                text-align: center;
                border: none;
            """)
    
    def mousePressEvent(self, event):
        global selectedOption
        global numWords
        global numTime
        # if we are not on index 0 of the stack then we want to switch to index 0
        justSwitched = False
        if config.mainWin.stack.currentIndex() != 2:
            justSwitched = True
            config.mainWin.stack.setCurrentIndex(2)
        # if the restart button is hidden from having no internet, just show it again
        config.mainWin.restart.setVisible(True)
        # if we click the currently selected one then nothing should happen
        if self == config.selectedOption and "ai" not in self.type and justSwitched == False:
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
                # check for internet connection since the AI generator requires internet
                if self.internetConnection() == True:                 
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
                    config.mainWin.textDisplay.setPlaceholderText(config.aiPlaceholderText)
                    # set focus to the textbox
                    config.mainWin.textDisplay.setFocus(True)
                # if no internet
                else:
                    # hide all suboptions
                    for i in range(0, len(config.subOptions)):
                        config.subOptions[i].setVisible(False)
                    # make the new selection stand out
                    self.changeSelection(self, None)
                    config.selectedOption.selected = False
                    self.selected = True
                    config.selectedOption = self
                    # just change the text to say "no internet connection"
                    config.mainWin.textDisplay.clear()
                    config.mainWin.textDisplay.setReadOnly(True)
                    config.mainWin.textDisplay.setPlaceholderText("No internet connection...")
                    # hide the restart button
                    config.mainWin.restart.setVisible(False)

        # if we clicked a suboption
        elif self.isOption == False:
            # if it is a suboption for words
            if "words" in self.type:
                # set the number of words to the number of words in the suboption
                config.numWords = int(self.buttonText)
                # make all the other word suboptions normal and make this one stand out
                for i in range(0, 4):
                    config.subOptions[i].setStyleSheet("""
                        background-color: """ + config.backgroundColor + """;
                        color: """ + config.accentColor + """;
                        text-align: center;
                        border: none;
                    """)
                # make the new selection stand out
                self.setStyleSheet("""
                    background-color: """ + config.backgroundColor + """;
                    color: """ + config.textHighlight + """;
                    text-align: center;
                    border: none;
                """)      
  
                self.selected = True
                config.selectedOption.selected = False
                config.selectedOption = self
                config.textbox.generatePassage()
            
            elif "time" in self.type:
                # set the time
                config.numTime = int(self.buttonText)
                # make all the other word suboptions normal and make this one stand out
                for i in range(4, len(config.subOptions)):
                    config.subOptions[i].setStyleSheet("""
                        background-color: """ + config.backgroundColor + """;
                        color: """ + config.accentColor + """;
                        text-align: center;
                        border: none;
                    """)
                # make the new selection stand out
                self.setStyleSheet("""
                    background-color: """ + config.backgroundColor + """;
                    color: """ + config.textHighlight + """;
                    text-align: center;
                    border: none;
                """)      
  
                self.selected = True
                config.selectedOption.selected = False
                config.selectedOption = self
                config.textbox.generatePassage()
            
            #*** this is where the ai stuff goes ***#
            else:
                return

    def internetConnection(self, host='http://google.com'):
                    try:
                        urllib.request.urlopen(host)
                        return True
                    except:
                        return False
    
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)    