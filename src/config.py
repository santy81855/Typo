import json
import os
# module to copy a file into another directory
import shutil
# module to get the appdata folder
from appdirs import *
# The name that appears at the top of the title bar
appName = "Typo"
appAuthor = "Santy"
# get the user data directory
userDataPath = user_data_dir(appName, appAuthor)
userDataPath += "/settings"
userDataPath = userDataPath.replace('Local', 'LocalLow')
# make the settings folder if it doesn't exist
if not os.path.exists(userDataPath):
    os.makedirs(userDataPath)
# add the settings file if it doesn't exist
if not os.path.exists(userDataPath + "/settings.json"):
    shutil.copy2("settings/settings.json", userDataPath)
# add the settings file to the path
userDataPath += "/settings.json"

# open the settings file
settingsFile = open(userDataPath, "r")
# convert the json file into a dictionary
settings = json.load(settingsFile)
# set the variables that can be changed by the user
# Opacity of the window
if settings["opacity"] > 1 or settings["opacity"] < 0:
    settings["opacity"] = 0.98
else:
    opacity = settings["opacity"]
# infobar
infoBar = settings["infoBar"]
# variable that can easily change the placeholder text for the ai input box
if settings["aiPlaceholderText"] == "":
    aiPlaceholderText = "Type any text here, and a passage will be generated!"
else:
    aiPlaceholderText = settings["aiPlaceholderText"]
# variable to change text alignment
textAlign = settings["textAlign"]
# list of words
content_list = []
if settings["wordList"] == "":
    my_file = open("words/1000words.txt", "r")
else:
    my_file = open(settings["wordList"], "r")
content = my_file.read()
content_list = content.split("\n")
my_file.close()
# variables for what can show up in the passage
symbols = settings["symbols"]
closeButtonHoverColor = settings["closeButtonHoverColor"]

# get the selected theme
selectedTheme = settings["selectedTheme"]

# get the variables in the theme
backgroundColor = settings["themes"][settings["selectedTheme"]]["backgroundColor"]
accentColor = settings["themes"][settings["selectedTheme"]]["accentColor"]
textHighlight = settings["themes"][settings["selectedTheme"]]["textHighlight"]


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

def reloadSettings():
    # make the file not read only
    import os
    from stat import S_IRWXO
    os.chmod("settings/settings.json", S_IRWXO)

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
    
    closeApp = False
    # open the settings file
    settingsFile = open(userDataPath, "r")
    # convert the json file into a dictionary
    settings = json.load(settingsFile)

    # set the variables that can be changed by the user
    # Opacity of the window
    if settings["opacity"] > 1 or settings["opacity"] < 0:
        settings["opacity"] = 0.98
    else:
        opacity = settings["opacity"]
    # whether they have an info bar at the bottom or not
    if infoBar != settings["infoBar"]:
        closeApp = True
    infoBar = settings["infoBar"]
    # variable that can easily change the placeholder text for the ai input box
    aiPlaceholderText = settings["aiPlaceholderText"]
    # variable to change text alignment
    if settings["textAlign"] == "":
        textAlign = "Center"
    else:
        textAlign = settings["textAlign"]
    # list of words
    content_list = []
    if settings["wordList"] == "":
        my_file = open("words/1000words.txt", "r")
    else:
        my_file = open(settings["wordList"], "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    # variables for what can show up in the passage
    symbols = settings["symbols"]
    closeButtonHoverColor = settings["closeButtonHoverColor"]

    if selectedTheme != settings["selectedTheme"]:
        closeApp = True
    # get the selected theme
    selectedTheme = settings["selectedTheme"]

    # get the variables in the theme
    backgroundColor = settings["themes"][settings["selectedTheme"]]["backgroundColor"]
    accentColor = settings["themes"][settings["selectedTheme"]]["accentColor"]
    textHighlight = settings["themes"][settings["selectedTheme"]]["textHighlight"]

    # close the app if they changed either the theme or the infobar
    if closeApp:
        application.quit()