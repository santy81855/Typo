import json
import os
# module to copy a file into another directory
import shutil
# module to get the appdata folder
from appdirs import *
# The name that appears at the top of the title bar
appName = "Typo"
appAuthor = "Santy"

class theme:
    def __init__(self, name, backgroundColor, accentColor, textHighlight):
        self.name = name
        self.backgroundColor = backgroundColor
        self.accentColor = accentColor
        self.textHighlight = textHighlight

# check if the settings have been stored, and if not store the default settings
from PyQt5.QtCore import QSettings, QStandardPaths
#print(str(QStandardPaths.writableLocation(QStandardPaths.AppDataLocation)))
settings = QSettings(appAuthor, appName)
# store all the settings as default values if they haven't been set yet
if settings.contains("user") == False:
    settings.setValue("user", "")
if settings.contains("username") == False:
    settings.setValue("username", "")
if settings.contains("opacity") == False:
    settings.setValue("opacity", 0.98)
if settings.contains("infoBar") == False:
    settings.setValue("infoBar", "False")
if settings.contains("aiPlaceholderText") == False:
    settings.setValue("aiPlaceholderText", "Type any text here, and a passage will be generated!")
if settings.contains("textAlign") == False:
    settings.setValue("textAlign", "Center")
if settings.contains("wordList") == False:
    settings.setValue("wordList", "words/1000words.txt")
if settings.contains("closeButtonHoverColor") == False:
    settings.setValue("closeButtonHoverColor", "#990000")
if settings.contains("selectedTheme") == False:
    settings.setValue("selectedTheme", "Forest")
if settings.contains("symbols") == False:
    settings.setValue("symbols", "False")
# create a dictionary of theme objects
themes = {}
# add the themes to the dictionary
themes["Nord"] = theme("Nord", "#3B4252", "#8FBCBB", "#D08770")
themes["Forest"] = theme("Forest", "#121e26", "#f4efeb", "#8FBCBB")
themes["Baby"] = theme("Baby", "#9df9ef", "#a28089", "#ffa8B6")
themes["Desert"] = theme("Desert", "#2d545e", "#e1b382", "#c89666")
themes["Light"] = theme("Light", "#F1F1F1", "#0F3D3E", "#395B64")
# add the themes to the settings
settings.setValue("themes", themes)


# set the variables that can be changed by the user
# Opacity of the window
if float(settings.value("opacity")) > 1 or float(settings.value("opacity")) < 0:
    settings.setValue("opacity", 0.98)
    opacity = 0.98
else:
    opacity = float(settings.value("opacity"))
# infobar
if settings.value("infoBar") == "True":
    infoBar = True
else:
    infoBar = False
# variable that can easily change the placeholder text for the ai input box
if settings.value("aiPlaceholderText") == "":
    aiPlaceholderText = "Type any text here, and a passage will be generated!"
else:
    aiPlaceholderText = settings.value("aiPlaceholderText")
# variable to change text alignment
textAlign = settings.value("textAlign")
# list of words
content_list = []
if settings.value("wordList") == "":
    my_file = open("words/1000words.txt", "r")
else:
    my_file = open(settings.value("wordList"), "r")
content = my_file.read()
content_list = content.split("\n")
my_file.close()
# variables for what can show up in the 
if settings.value("symbols") == "True":
    symbols = True
else:
    symbols = False
closeButtonHoverColor = settings.value("closeButtonHoverColor")

# get the selected theme
selectedTheme = settings.value("selectedTheme")

# get the variables in the theme
backgroundColor = settings.value("themes")[selectedTheme].backgroundColor
accentColor = settings.value("themes")[selectedTheme].accentColor
textHighlight = settings.value("themes")[selectedTheme].textHighlight


# unchangeable settings

# The logo for the taskbar
logoName = "logo.ico"
# make the resolution global variables
screen_resolution = 0
width = 0
height = 0
key = ''
res = {}
res["1920x1080"] = [1920/2, 0] # full hd
res["2560x1440"] = [2560/2, 0] # wqhd
res["3440x1440"] = [3440/2, 0] # ultrawide
res["3840x2160"] = [3840/2, 0] # 4k
focused = False # variable to track if the gui is focused so it knows to track typing or not
# variable for the minimum resolution (minSize x minSize)
minSize = 500
# variable to track what the smallest screen size is that still needs a margin
tooSmall = 800
# variable to track the margins used on the main layout
MARGIN = 5
# variable to store the scroll bar width
scrollBarWidth = 12
# variable to allow going back to previous size after maximizing
isMaximized = False
# number of characters to display
numChars = 200
# font size for option buttons
optionButtonSize = 20
# font size for suboption buttons
subOptionButtonSize = 15
# variable to track if we are currently getting input for teh AI passage
gettingInput = False
# store the input text
inputText = ""
# options arr
options = []
# suboptions arr
subOptions = []
# variables to store the mainwindow and title bar
application = None
mainWin = None
titleBar = None
textbox = None
# store the full passage
curText = ""
# store the text that is displayed
shortText = ""
# store all the text that has been typed for a given passage
totalTypedText = ""
# store the text that is currently being typed
typedText = ""
# all the text currently being displayed
allText = ""
# store the index of the last character in the shorttext
curIndex = 0
# variable to track if they are typing the first line of text
initialLine = True
# track the time for wpm counter
timeStart = 0
# track time for the typing counter
typingTimeStart = 0
# store the timer
timer = None
# what type of passage
aiPassage = False
words1000 = True
numWords = 10
numTime = 15
# variable to track the time
timeCount = 0
# variable to track the wpm
wpm = 0
# variable that calibrates the wpm
avgWordLen = 5
# store the number of correct and incorrect key presses
right = 0
wrong = 0
punctuation = "!'(), -.:;?@"
# variable to be able to snap to sides and corners
leftDown = False
upDown = False
downDown = False
rightDown = False
# variablee to track if the snap widget is up
isSnapWidget = False
# variable to track which main option is selected
selectedOption = None
# set the font size
fontSize = 30
# number of items in main vertical layout with infoBar
numLayoutItems = 10
# background color for the google login button
googleButtonBackground = "#76A7FA"
errorColor = "#FF3131"
profileIconColor = "#ffffff"

def reloadSettings():
    global opacity
    global infoBar
    global aiPlaceholderText
    global textAlign
    global content_list
    global symbols
    global closeButtonHoverColor
    global backgroundColor
    global accentColor
    global textHighlight
    global selectedTheme
    global application
    global mainWin

    closeApp = False

    # set the variables that can be changed by the user
    # Opacity of the window
    if float(settings.value("opacity")) > 1 or float(settings.value("opacity")) < 0:
        settings.setValue("opacity", 0.98)
        opacity = 0.98
    else:
        opacity = float(settings.value("opacity"))
    # infobar
    if settings.value("infoBar") == "True":
        value = True
    else:
        value = False
    if infoBar != value:
        closeApp = True
    infoBar = value
    # variable that can easily change the placeholder text for the ai input box
    if settings.value("aiPlaceholderText") == "":
        aiPlaceholderText = "Type any text here, and a passage will be generated!"
    else:
        aiPlaceholderText = settings.value("aiPlaceholderText")
    # variable to change text alignment
    textAlign = settings.value("textAlign")
    # list of words
    content_list = []
    if settings.value("wordList") == "":
        my_file = open("words/1000words.txt", "r")
    else:
        my_file = open(settings.value("wordList"), "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    # variables for what can show up in the passage
    if settings.value("symbols") == "True":
        value = True
    else:
        value = False
    symbols = value
    closeButtonHoverColor = settings.value("closeButtonHoverColor")
    if selectedTheme != settings.value("selectedTheme"):
        closeApp = True
    # get the selected theme
    selectedTheme = settings.value("selectedTheme")

    # get the variables in the theme
    backgroundColor = settings.value("themes")[selectedTheme].backgroundColor
    accentColor = settings.value("themes")[selectedTheme].accentColor
    textHighlight = settings.value("themes")[selectedTheme].textHighlight

    # close the app if they changed either the theme or the infobar
    if closeApp:
        #application.quit() 
        mainWin.close()
        import Typo
        Typo.createMain()