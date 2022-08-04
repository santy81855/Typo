from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QPoint, QTimer
from PyQt5 import QtMultimedia
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QFontMetrics
import config, ScrollBar, FirebaseDB
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
            color: """+config.accentColor+""";
            border: none;
            selection-background-color: """+config.backgroundColor+""";
            selection-color: """+config.accentColor+""";
            margin-left: """+marginStr+""";
            margin-right: """+marginStr+""";
            margin-top: """+marginStr+""";
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
    
    def timerEnd(self):
        global timeCount
        global wpm
        config.timeCount += 1
        # calculate the wpm
        chars = len(config.totalTypedText)
        minutes = config.timeCount / 60
        config.wpm = chars / config.avgWordLen / minutes
        if config.timeCount == config.numTime and config.selectedOption.type == "time": 
            config.timeCount = 0
            # update the wpm label
            config.mainWin.results.wpmLabel.setText("WPM:\n" + str(round(config.wpm, 2)))
            accuracy = config.right / (config.right + config.wrong) * 100
            # update the accuracy label
            config.mainWin.results.accuracyLabel.setText("Accuracy:\n" + str(round(accuracy, 2)) + "%")
            # add this result to the results list
            self.addResultDB()
            # switch to the results page on the stacked widget
            config.mainWin.stack.setCurrentIndex(3)

    def keyPressEvent(self, event):           
        global typedText
        global right
        global wrong
        global timeStart
        global timeEnd
        global typingTimeStart
        global inputText
        global gettingInput

        # get past all the modifiers
        if event.key() == 16777220 and config.gettingInput == False: # enter
            return
        elif event.key() == 16777220 and config.gettingInput == True: # enter
            # set the getting input to false
            config.gettingInput = False
            # get the text from the textbox
            config.inputText = self.toPlainText()
            # change the button back from "generate" to "restart"
            config.mainWin.restart.setText("Restart")
            # clear the textbox
            self.clear()
            # generate a new passage
            self.generatePassage()
            # set focus to the textbox
            self.setFocus(True)
            return
        elif event.key() == 16777219 and config.gettingInput == True: # backspace
            config.inputText = config.inputText[:-1]
            return QTextEdit.keyPressEvent(self, event)
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
        elif config.gettingInput == True:
            config.inputText += event.text()
            self.setText('<a style="color:{};">'.format(config.accentColor) + config.inputText + '</a>')
            for i in range(0, len(config.inputText)):
                self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)
        else: # normal keys
            global allText
            global initialLine
            global timer
            global totalTypedText
            # if it's the correct characted then pop it from the text, and replace it with the one we type
            if len(config.shortText) > 0 and event.text() == config.shortText[0]:
                config.totalTypedText += event.text()
                # if this is the first character that is typed then we start the timer so we can count down from the time limit and keep track of the wpm
                if len(config.typedText) == 0:
                    config.timer = QTimer(self)
                    milliseconds = 1000
                    # the timer will call the timerEnd function when it reaches its end
                    config.timer.timeout.connect(self.timerEnd)
                    # start the timer and have it count every second so we have a function that can update a potential timer
                    config.timer.start(milliseconds)
                    

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
                    # if the remaining text is longer than a line length then we want to display a line length of characters 
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
                            if "center" in config.textAlign:
                                self.setAlignment(Qt.AlignCenter)
                            elif "left" in config.textAlign:
                                self.setAlignment(Qt.AlignLeft)
                            elif "right" in config.textAlign:
                                self.setAlignment(Qt.AlignRight)
                        # if it is not a space then underline it
                        else:
                            self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + '<u>' + config.shortText[0] + '</u>'+ config.shortText[1:])
                            if "center" in config.textAlign:
                                self.setAlignment(Qt.AlignCenter)
                            elif "left" in config.textAlign:
                                self.setAlignment(Qt.AlignLeft)
                            elif "right" in config.textAlign:
                                self.setAlignment(Qt.AlignRight)
                        # move the cursor to the right spot
                        for i in range(0, len(config.typedText)):                    
                            self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)
                    # if there is no more text
                    else:
                        # update the wpm label
                        config.mainWin.results.wpmLabel.setText("WPM:\n" + str(round(config.wpm, 2)))
                        accuracy = config.right / (config.right + config.wrong) * 100
                        # update the accuracy label
                        config.mainWin.results.accuracyLabel.setText("Accuracy:\n" + str(round(accuracy, 2)) + "%")
                        # update the wpm label
                        config.mainWin.results.wpmLabel.setText("WPM:\n" + str(round(config.wpm, 2)))
                        accuracy = config.right / (config.right + config.wrong) * 100
                        # update the accuracy label
                        config.mainWin.results.accuracyLabel.setText("Accuracy:\n" + str(round(accuracy, 2)) + "%")
                        # add this result to the results list
                        self.addResultDB()
                        # switch to the results page on the stacked widget
                        config.mainWin.stack.setCurrentIndex(3)
                        return
                # we want to underline the next character, but only if there is text left to write
                elif len(config.shortText) >= 1:
                    # if the next character is just a space don't underline it
                    if config.shortText[0] == " ":
                        self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + config.shortText[0] + config.shortText[1:])
                        if "center" in config.textAlign:
                            self.setAlignment(Qt.AlignCenter)
                        elif "left" in config.textAlign:
                            self.setAlignment(Qt.AlignLeft)
                        elif "right" in config.textAlign:
                            self.setAlignment(Qt.AlignRight)
                    # if it is not a space then underline it
                    else:
                        self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>' + '<u>' + config.shortText[0] + '</u>'+ config.shortText[1:])
                        if "center" in config.textAlign:
                            self.setAlignment(Qt.AlignCenter)
                        elif "left" in config.textAlign:
                            self.setAlignment(Qt.AlignLeft)
                        elif "right" in config.textAlign:
                            self.setAlignment(Qt.AlignRight)
                    # move the cursor to the right spot
                    for i in range(0, len(config.typedText)):                    
                        self.moveCursor(QTextCursor.Right, QTextCursor.MoveAnchor)

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
                    self.setText('<a style="color:{};">'.format(config.accentColor) + config.shortText + '</a>')
                    if "center" in config.textAlign:
                        self.setAlignment(Qt.AlignCenter)
                    elif "left" in config.textAlign:
                        self.setAlignment(Qt.AlignLeft)
                    elif "right" in config.textAlign:
                        self.setAlignment(Qt.AlignRight)
                    self.moveCursor(QTextCursor.Start, QTextCursor.MoveAnchor)
                    return
                # if there is no more text to write then just end it #
                else:
                    # update the wpm label
                    config.mainWin.results.wpmLabel.setText("WPM:\n" + str(round(config.wpm, 2)))
                    accuracy = config.right / (config.right + config.wrong) * 100
                    # update the accuracy label
                    config.mainWin.results.accuracyLabel.setText("Accuracy:\n" + str(round(accuracy, 2)) + "%")
                    # add this result to the results list
                    self.addResultDB()
                    # switch to the results page on the stacked widget
                    config.mainWin.stack.setCurrentIndex(3)
                    self.setText('<a style="color:{};">'.format(config.textHighlight) + config.typedText + '</a>')
                    if "center" in config.textAlign:
                        self.setAlignment(Qt.AlignCenter)
                    elif "left" in config.textAlign:
                        self.setAlignment(Qt.AlignLeft)
                    elif "right" in config.textAlign:
                        self.setAlignment(Qt.AlignRight)
                    self.setReadOnly(True)
                    # reset the word per minute counter so that we are ready for the new one
                    config.timeStart = 0
                    # set the typedText back to nothing so that we can start over
                    config.typedText = ""
            # if there is no more text to write then just ignore
            elif len(config.shortText) == 0 and config.curIndex == len(config.curText):
                return
            else:
                print("wrong")
                config.wrong += 1
                
        # accuracy
        #print(config.right / (config.wrong + config.right))
    
    def addResultDB(self):
        # get the date
        from datetime import date
        today = date.today()
        accuracy = config.right / (config.right + config.wrong) * 100
        # add this result to the results list
        data = {'type': config.selectedOption.type, 'length': config.selectedOption.buttonText, 'wpm': config.wpm, 'accuracy' : accuracy, 'date' : today.strftime("%Y-%m-%d")}
        FirebaseDB.update_user_results(config.settings.value('username'), data) 

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
        global timer
        global timeCount
        global wpm
        global inputText
        global totalTypedText
        # reset total typed text
        config.totalTypedText = ""
        # reset the wpm
        config.wpm = 0
        # reset the timer if it has been created already
        if config.timer != None:
            config.timer.stop()
        # reset the counter for the timer
        config.timeCount = 0
        config.typedText = ""
        config.right = 0
        config.wrong = 0
        config.initialLine = True
        if "ai" in config.selectedOption.type:
            r = requests.post(
                "https://api.deepai.org/api/text-generator",
                data={
                    'text': config.inputText,
                },
                headers={'api-key': 'f6550bae-e6ba-4f9e-8b71-14fa364eb51f'}
            )
            # clear input text
            config.inputText = ""
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
            # now that we have the text, let's limit it to 100 words so they don't have to type forever
            if len(text.split(" ")) > 100:
                text = text.split(" ")[0:100]
                text = " ".join(text)

        elif "words" in config.selectedOption.type:
            text = ""
            content_list = config.content_list
            # generate a list of words of length config.numWords
            for i in range(0, config.numWords):
                if i == 0:
                    text = text + str(random.choice(content_list))
                else:
                    text = text + ' ' + str(random.choice(content_list))
        
        elif "time" in config.selectedOption.type:
            text = ""
            content_list = config.content_list
            # generate a crazy long list of words
            for i in range(0, 1000):
                if i == 0:
                    text = text + str(random.choice(content_list))
                else:
                    text = text + ' ' + str(random.choice(content_list))
        # get the length of one line and multiply it by 3 to get numChars
        self.getNumChars(text)

        # adjust the length of the text to be numChars long and set it
        self.adjustTextLength(text)

    def getNumChars(self, text):
        global numChars

        self.setText('<a style="color:{};">'.format(config.backgroundColor) + text + '</a>')
        # get the cursor of the textEdit
        cursor = QTextCursor(self.document())
        # now get how many lines there are
        numLines = cursor.block().layout().lineCount()

        if numLines > 0:
            lineLen = cursor.block().layout().lineAt(0).textLength()
            config.numChars = lineLen * 3
        
    def adjustTextLength(self, text):        
        global curText
        global allText
        global curText
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

        # set the shorttext
        self.setText('<a style="color:{};">'.format(config.accentColor) + config.shortText + '</a>')
        if "center" in config.textAlign:
            self.setAlignment(Qt.AlignCenter)
        elif "left" in config.textAlign:
            self.setAlignment(Qt.AlignLeft)
        elif "right" in config.textAlign:
            self.setAlignment(Qt.AlignRight)
        self.setReadOnly(False)
    