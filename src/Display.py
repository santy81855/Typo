from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5 import QtMultimedia
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QFontMetrics
import config, ScrollBar
import requests
import time
import random

class Passage(QTextEdit):
    def __init__(self, parent):
        super(Passage, self).__init__()
        self.parent = parent
        config.textbox = self
        # calculate margins
        margin = self.parent.width() * 0.08
        marginStr = str(margin) + "px"
        self.setStyleSheet("""
        QTextEdit
        {
            background-color: """+config.backgroundColor+""";
            color: """+config.accentColor1+""";
            border: none;
            selection-background-color: """+config.backgroundColor+""";
            selection-color: """+config.accentColor1+""";
            margin-left: """+marginStr+""";
            margin-right: """+marginStr+""";
            margin-top: """+marginStr+""";
            margin-bottom: """+marginStr+""";
        }
        """)
        
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( config.fontSize )
        self.font = font
        self.setFont(font)
        self.setMouseTracking(True)
        self.generatePassage()
        # create a new scrollbar that looks nicer
        self.scrollbar = ScrollBar.ScrollBar(self)
        self.setVerticalScrollBar(self.scrollbar)

    def keyPressEvent(self, event):           
        global typedText
        global right
        global wrong
        global timeStart
        global timeEnd
        # get past all the modifiers
        if event.key() == 16777248 or event.key() == 16777249: # shift
            return
        elif event.key() == 16777220: # enter
            return
        elif event.key() == 16777216: # control
            return
        elif event.key() == 16777251: # alt
            return
        elif event.key() == 16777250: # super
            return
        elif event.key() == 16777238 or event.key() == 16777239: # pgup & pgdn
            return
        elif event.key() == 16777232 or event.key() == 16777233: # home & end
            return
        elif event.key() == 16777223: # delete
            return
        elif event.key() == 16777219: # backspace
            return
        elif event.key() == 16777234 or event.key() == 16777235 or event.key() == 16777236 or event.key() == 16777237: # arrows
            return 
        else: # normal keys
            if len(config.curText) == 0:
                return
            # if it's the correct character then pop it from the text, and replace it with the one we type
            elif event.text() == config.curText[0]:
                # if this is the first character that is typed then we start the timer so we can count down from the time limit
                if len(config.typedText) == 0:
                    config.typingTimeStart = time.time()
                config.right += 1
                config.curText = config.curText[1:]
                config.typedText = config.typedText + event.text()
                # we want to underline the next character, but only if there is text left to write
                if len(config.curText) >= 1:
                    # if the next character is just a space don't underline it
                    if config.curText[0] == " ":
                        self.setText('<b style="color:{};">'.format(config.textHighlight) + config.typedText + '</b>' + config.curText[0] + config.curText[1:])
                    # if it is not a space then underline it
                    else:
                        self.setText('<b style="color:{};">'.format(config.textHighlight) + config.typedText + '</b>' + '<u>' + config.curText[0] + '</u>'+ config.curText[1:])
                
                # if there is no more text to write then just end it #
                else:
                    self.setText('<b style="color:{};">'.format(config.textHighlight) + config.typedText + '</b>')
                    self.setReadOnly(True)
                    # reset the word per minute counter so that we are ready for the new one
                    config.timeStart = 0
                    # set the typedText back to nothing so that we can start over
                    config.typedText = ""

                # move the cursor to the right spot
                for i in range(0, len(config.typedText)):                    
                    self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)
                # if this is the first character then we want to start tracking the time
                if len(config.typedText) == 1:
                    config.timeStart = time.time()
                # otherwise we just calculate the wpm
                else:
                    self.getWPM()
            else:
                config.wrong += 1
                self.getWPM()
                
        # accuracy
        #print(config.right / (config.wrong + config.right))

    def getWPM(self):
        chars = len(config.typedText)
        timePassed = time.time() - config.timeStart
        minutes = timePassed / 60
        wpm = chars / config.avgWordLen / minutes
        print(wpm)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.IBeamCursor)

    def mousePressEvent(self, event):
        self.setFocus()
    
    def mouseReleaseEvent(self, event):
        return

    def mouseDoubleClickEvent(self, event):
        return

    def generatePassage(self):
        if "AI" in config.selectedOption.text:
            r = requests.post(
                "https://api.deepai.org/api/text-generator",
                data={
                    'text': 'And half of my heart has always been yours',
                },
                headers={'api-key': 'f6550bae-e6ba-4f9e-8b71-14fa364eb51f'}
            )
            text = ""
            check = False
            for i in range(0, len(r.text)):
                if r.text[i] == "p" and r.text[i + 1] == "u" and r.text[i + 2] == "t":
                    index = i + 6
                    while r.text[index] != '}':
                        if r.text[index] == '\\' and r.text[index + 1] == 'n' and r.text[index + 2] == '\\' and r.text[index + 3] == 'n':
                            text = text + ' '
                            index += 4
                            continue
                        elif r.text[index] == '\\' and r.text[index + 1] == 'n':
                            text = text + ' '
                            index += 2
                            continue
                        # if we don't want symbols and the character is not alphanumeric then we skip it
                        if config.symbols == False and r.text[index].isalnum() == False and r.text[index] not in config.punctuation:
                            index += 1
                            continue
                        text = text + r.text[index]
                        index += 1
                    break

        elif "words" in config.selectedOption.text:
            my_file = open("1000words.txt", "r")
            content = my_file.read()
            content_list = content.split("\n")
            my_file.close()
            text = ""
            # generate a list of words of length config.numWords
            for i in range(0, config.numWords):
                if i == 0:
                    text = text + str(random.choice(content_list))
                else:
                    text = text + ' ' + str(random.choice(content_list))
        
        elif "time" in config.selectedOption.text:
            # need to set the timer to 60 on whatever will display the time

            my_file = open("1000words.txt", "r")
            content = my_file.read()
            content_list = content.split("\n")
            my_file.close()
            text = ""
            # generate a crazy long list of words
            for i in range(0, 1000):
                if i == 0:
                    text = text + str(random.choice(content_list))
                else:
                    text = text + ' ' + str(random.choice(content_list))

        global curText
        config.curText = text
        # Only display "numChars" characters of the text
        global shortText
        config.shortText = ""
        # if the text is long enough to warrant multiple lines then we want to display "numChars" characters 
        if len(config.curText) > config.numChars:
            for i in range(0, config.numChars):
                config.shortText = config.shortText + config.curText[i]
            # if we end on an incomplete word then we remove that incomplete word
            lastWord = ""
            startIndex = len(config.shortText) - 1
            # get the start index of the last word
            while config.shortText[startIndex] != " ":
                startIndex -= 1
            startIndex += 1
            # store the last word in the shortText variable
            while startIndex < len(config.shortText):
                lastWord = lastWord + config.shortText[startIndex]
                startIndex += 1
            # if the last word is incomplete then we remove it
            if lastWord not in content_list:
                config.shortText = config.shortText[0:len(config.shortText) - len(lastWord)]
            # if the last character is a space remove it
            if config.shortText[len(config.shortText) - 1] == " ":
                config.shortText = config.shortText[:-1]
        # otherwise the short text can just be the normal text
        else:
            config.shortText = config.curText

        print(config.shortText)
        self.setText(config.shortText)
        

    
    