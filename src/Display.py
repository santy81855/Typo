from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QPoint, QTimer
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
        global typingTimeStart

        # check the time 
        if "time" in config.selectedOption.text and config.typingTimeStart != 0:
            timeEnd = time.time()
            timePassed = timeEnd - config.typingTimeStart
            if timePassed > 5:
                print("times up buster")

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
            global allText
            global initialLine
            global timer
            # if it's the correct characted then pop it from the text, and replace it with the one we type
            if len(config.shortText) > 0 and event.text() == config.shortText[0]:
                # if this is the first character that is typed then we start the timer so we can count down from the time limit
                if "time" in config.selectedOption.text and len(config.typedText) == 0:
                    config.timer = QTimer(self)
                    

                # update the correct character count
                config.right += 1
                # remove the first character of shortText
                config.shortText = config.shortText[1:]
                # add the newly typed character to the typedText
                config.typedText = config.typedText + event.text()

                # check if we need to "scroll up"
                # get the cursor of the textEdit
                cursor = QTextCursor(self.document())
                # if there is a second line then we need to check if we are on the last character of this line
                validLine = cursor.block().layout().lineAt(1).isValid()
                if validLine:
                    # get the length of both the first and second line
                    firstLineLength = cursor.block().layout().lineAt(0).textLength()
                    secondLineLength = cursor.block().layout().lineAt(1).textLength()
                    lastchar = firstLineLength + secondLineLength
                
                # if we are on the last char of the second line
                if validLine == True and len(config.typedText) == lastchar:
                    # get the start of the first and second line
                    firstStart = 0
                    secondStart = cursor.block().layout().lineAt(1).textStart()
                    # get the text of the second line. this includes the space at the end of the line
                    firstLine = config.allText[secondStart:secondStart+secondLineLength]
                    restText = ""
                    # only add rest of the text if there is any text after the second line
                    if secondStart + secondLineLength < len(config.allText):
                        restText = config.allText[secondStart+secondLineLength:len(config.allText)]
                    # add the same number of characters to the end of the restText as you took from the first line
                    # Only display "numChars" characters of the text
                    global shortText
                    global curIndex
                    global typedText
                    config.typedText = ""
                    config.shortText = ""
                    tempString = ""
                    # if the remaining text is longer than numChars then we want to display "numChars" characters 
                    remainingText = len(config.curText) - config.curIndex
                    if remainingText > firstLineLength:
                        for i in range(config.curIndex, config.curIndex + firstLineLength):
                            tempString = tempString + config.curText[i]
                        # update the curIndex
                        config.curIndex += (firstLineLength - 1)
                        # if the last character is a space then the word is complete
                        if tempString[len(tempString) - 1] == " ":
                            # increase the curIndex by 1 to land on the first character of the next word
                            config.curIndex += 1
                        # otherwise we need to check if the character that comes directly after is a space
                        elif config.curText[config.curIndex + 1] == " ":
                            # add a space to the end of the shortText
                            tempString = tempString + " "
                            # increase the curIndex by 2 to land on the first letter of the next word
                            config.curIndex += 2
                        # otherwise it is just incomplete so we want to remove that incomplete word
                        else:
                            # update the curIndex
                            while config.curText[config.curIndex] != " ":
                                config.curIndex -= 1
                            # add one to the curIndex to land on the first letter of the next word
                            config.curIndex += 1
                            # remove incomplete word
                            tempString = tempString[0:len(tempString) - len(tempString.split(" ")[len(tempString.split(" ")) - 1]) - 1]
                            # add a space to the shortText
                            tempString = tempString + " "
                        
                    # if the remaining text is less than the numChars then we want to display all of the text
                    else:
                        tempString = config.curText[config.curIndex:config.curIndex + len(config.curText)]
                        # make the curIndex out of bounds so that we can check for completion
                        config.curIndex = len(config.curText)
                    print("."+firstLine+".")
                    print("."+restText+".")
                    print("."+tempString+".")
                    restText += tempString
                    # make the firstLine the typedtext
                    config.typedText = firstLine
                    # make the restText the shortText
                    config.shortText = restText
                    config.allText = firstLine + restText
                    # if the next character is just a space don't underline it
                    if len(config.shortText) >= 1:
                        if config.shortText[0] == " ":
                            self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + config.shortText[0] + config.shortText[1:])
                        # if it is not a space then underline it
                        else:
                            self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + '<u>' + config.shortText[0] + '</u>'+ config.shortText[1:])
                        # move the cursor to the right spot
                        for i in range(0, len(config.typedText)):                    
                            self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)
                    # if there is no more text
                    else:
                        print('complete')
                        return
                # we want to underline the next character, but only if there is text left to write
                elif len(config.shortText) >= 1:
                    # if the next character is just a space don't underline it
                    if config.shortText[0] == " ":
                        self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + config.shortText[0] + config.shortText[1:])
                    # if it is not a space then underline it
                    else:
                        self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + '<u>' + config.shortText[0] + '</u>'+ config.shortText[1:])
                    # move the cursor to the right spot
                    for i in range(0, len(config.typedText)):                    
                        self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)

                # *** this is where I need to add the "scrolling" to keep the person in the middle line *** #
                # if this was the last character in shortText then we want to update the text shown to include the next bit of text
                elif len(config.shortText) == 0 and config.curIndex < len(config.curText):
                    print("last character was just typed")
                    # Only display "numChars" characters of the text
                    global shortText
                    global curIndex
                    global typedText
                    config.typedText = ""
                    config.shortText = ""
                    # if the remaining text is longer than numChars then we want to display "numChars" characters 
                    remainingText = len(config.curText) - config.curIndex
                    if remainingText > config.numChars:
                        for i in range(config.curIndex, config.curIndex + config.numChars):
                            config.shortText = config.shortText + config.curText[i]
                        # update the curIndex
                        config.curIndex += (config.numChars - 1)
                        # if the last character is a space then the word is complete
                        if config.shortText[len(config.shortText) - 1] == " ":
                            # increase the curIndex by 1 to land on the first character of the next word
                            config.curIndex += 1
                        # otherwise we need to check if the character that comes directly after is a space
                        elif config.curText[config.curIndex + 1] == " ":
                            # add a space to the end of the shortText
                            config.shortText = config.shortText + " "
                            # increase the curIndex by 2 to land on the first letter of the next word
                            config.curIndex += 2
                        # otherwise it is just incomplete so we want to remove that incomplete word
                        else:
                            # update the curIndex
                            while config.curText[config.curIndex] != " ":
                                config.curIndex -= 1
                            # add one to the curIndex to land on the first letter of the next word
                            config.curIndex += 1
                            # remove incomplete word
                            config.shortText = config.shortText[0:len(config.shortText) - len(config.shortText.split(" ")[len(config.shortText.split(" ")) - 1]) - 1]
                            # add a space to the shortText
                            config.shortText = config.shortText + " "
                        
                    # if the remaining text is less than the numChars then we want to display all of the text
                    else:
                        config.shortText = config.curText[config.curIndex:config.curIndex + len(config.curText)]
                        # make the curIndex out of bounds so that we can check for completion
                        config.curIndex = len(config.curText)
                    # update the text shown
                    self.clear()
                    self.setText('<a style="color:{};">'.format(config.accentColor1) + config.shortText + '</a>')
                    self.moveCursor(QTextCursor.Start, QTextCursor.MoveAnchor)
                    return
                # if there is no more text to write then just end it #
                else:
                    self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>')
                    self.setReadOnly(True)
                    # reset the word per minute counter so that we are ready for the new one
                    config.timeStart = 0
                    # set the typedText back to nothing so that we can start over
                    config.typedText = ""
            # if there is no more text to write then just ignore
            elif len(config.shortText) == 0 and config.curIndex == len(config.curText):
                return
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
        global typedText
        global right
        global wrong
        global initialLine
        global typingTimeStart
        config.typedText = ""
        config.right = 0
        config.wrong = 0
        config.initialLine = True
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
            global content_list
            my_file = open("1000words.txt", "r")
            content = my_file.read()
            config.content_list = content.split("\n")
            my_file.close()
            text = ""
            # generate a list of words of length config.numWords
            for i in range(0, config.numWords):
                if i == 0:
                    text = text + str(random.choice(config.content_list))
                else:
                    text = text + ' ' + str(random.choice(config.content_list))
        
        elif "time" in config.selectedOption.text:
            global content_list
            # need to set the timer to 60 on whatever will display the time

            my_file = open("1000words.txt", "r")
            content = my_file.read()
            config.content_list = content.split("\n")
            my_file.close()
            text = ""
            # generate a crazy long list of words
            for i in range(0, 1000):
                if i == 0:
                    text = text + str(random.choice(config.content_list))
                else:
                    text = text + ' ' + str(random.choice(config.content_list))

        global curText
        global allText
        config.curText = text
        # Only display "numChars" characters of the text
        global shortText
        global curIndex
        config.curIndex = 0
        config.shortText = ""

        # if the text is long enough to warrant multiple lines then we want to display "numChars" characters 
        if len(config.curText) > config.numChars:
            for i in range(config.curIndex, config.curIndex + config.numChars):
                config.shortText = config.shortText + config.curText[i]
            # update the curIndex
            config.curIndex += (config.numChars - 1)
            # if the last character is a space then the word is complete
            if config.shortText[len(config.shortText) - 1] == " ":
                # increase the curIndex by 1 to land on the first character of the next word
                config.curIndex += 1
            # otherwise we need to check if the character that comes directly after is a space
            elif config.curText[config.curIndex + 1] == " ":
                # add a space to the end of the shortText
                config.shortText = config.shortText + " "
                # increase the curIndex by 2 to land on the first letter of the next word
                config.curIndex += 2
            # otherwise it is just incomplete so we want to remove that incomplete word
            else:
                # update the curIndex
                while config.curText[config.curIndex] != " ":
                    config.curIndex -= 1
                # add one to the curIndex to land on the first letter of the next word
                config.curIndex += 1
                # remove incomplete word
                config.shortText = config.shortText[0:len(config.shortText) - len(config.shortText.split(" ")[len(config.shortText.split(" ")) - 1]) - 1]
                # add a space to the shortText
                config.shortText = config.shortText + " "
            
        # if the remaining text is less than the numChars then we want to display all of the text
        else:
            config.shortText = config.curText[config.curIndex:config.curIndex + len(config.curText)]
            # make the curIndex out of bounds so that we can check for completion
            config.curIndex = len(config.curText)
        config.allText = config.shortText

        self.setText('<a style="color:{};">'.format(config.accentColor1) + config.shortText + '</a>')
        self.setReadOnly(False)
        

    
    