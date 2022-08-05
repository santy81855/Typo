import sys
from PyQt5 import QtGui, QtCore, QtMultimedia
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QShortcut, QApplication, QGraphicsDropShadowEffect, QLabel, QDesktopWidget, QFrame, QStackedWidget, QPushButton, QScrollArea, QWidget, QSizePolicy
from PyQt5.QtCore import Qt, QPoint, QSettings
from PyQt5.QtGui import QColor, QCursor, QKeySequence, QFont
import config, TitleBar, Snap, SnapButton, Display, OptionButton, Results, RestartButton, SettingsPage, SettingsButton, Login, SignUpPage, ProfileButton, ProfileTab, TypingPage
from platform import system
operatingSystem = system()

# Windows
if operatingSystem == 'Windows':
    # to get the working monitor size
    from win32api import GetMonitorInfo, MonitorFromPoint
    # to get the scaling aware
    import ctypes
    # this sets the appID
    myappid = config.appName
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # to be scaling aware
    user32 = ctypes.windll.user32 
    user32.SetProcessDPIAware()

# macOS
elif operatingSystem == 'Darwin':
    print('mac')

# linux
elif operatingSystem == 'Linux':
    print('linux')

class MainWindow(QFrame):
    def __init__(self):
        super(MainWindow, self).__init__()
        # store the main window widget so we can access all these variables from other files
        global mainWin
        config.mainWin = self
        # set the window to be opaque to begin with
        self.setWindowOpacity(1.0)
        # we need to account for windows since it can have a taskbar taking up screen space
        if operatingSystem == 'Windows':
            # get the current working resolution to account for things like the taskbar being displayed on windows
            monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
            working_resolution = monitor_info.get("Work")
            workingWidth = working_resolution[2]
            workingHeight = working_resolution[3]
        else:
            # if now windows then assume there is no taskbar
            resolution = config.application.desktop().screenGeometry()
            workingWidth = resolution.width()
            workingHeight = resolution.height()
        # start the window on the middle of the screen
        self.setGeometry(int(workingWidth/7), 0, int(workingWidth - (2 * workingWidth / 7)), int(workingHeight))
        # vertical layout 
        self.layout = QVBoxLayout()
        self.layout.setSpacing(10)
        # add the title bar
        self.titlebarWidget = TitleBar.MyBar(self)
        self.layout.addWidget(self.titlebarWidget)
        # add drop shadow under the title bar
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setBlurRadius(8)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(2)
        self.shadow.setColor(QColor("black"))
        # add a drop shadow before the next thing
        self.dropShadow = QLabel("")
        self.dropShadow.setStyleSheet("""
            background-color: """+config.backgroundColor+""";
            border: none;
                                        """)
        self.dropShadow.setFixedHeight(1)
        self.dropShadow.setGraphicsEffect(self.shadow)
        self.layout.addWidget(self.dropShadow)
        # add a stretch to the vertical layout to keep the title bar at the top
        #self.layout.addStretch(-1)

        #-----------------------------------------ADD YOUR WIDGETS HERE-------------------------------------------------------#
        # add the settings button
        self.settingsButton = SettingsButton.SettingsButton(self)
        # add the profile button
        self.profileButton = ProfileButton.ProfileButton(self)
        # create hor layout 
        self.settingsHorLayout = QHBoxLayout()
        self.settingsHorLayout.setSpacing(0)
        # add a stretch to the horizontal layout
        self.settingsHorLayout.addStretch(-1)
        # add the settings button to the horizontal layout
        self.settingsHorLayout.addWidget(self.settingsButton)
        # add the profile button to the horizontal layout
        self.settingsHorLayout.addWidget(self.profileButton)
        # add the hor layout to the main layout
        self.layout.addLayout(self.settingsHorLayout)

        # create the typing page
        self.typingPage = TypingPage.TypingPage(self)
        
        global options
        global subOptions
        # add horizontal layout to display the options
        self.optionsLayout = QHBoxLayout()
        self.optionsLayout.setSpacing(10)
        # stretch on the left
        self.optionsLayout.addStretch(-1)
        # create button for words
        self.words = OptionButton.OButton(self, "10", 80, True, "words")
        # create button for time
        self.time = OptionButton.OButton(self, "15", 65, True, "time")
        # craete button for AI generated passage
        self.generated = OptionButton.OButton(self, "AI", 35, True, "ai")
        # add the buttons to the options arr
        config.options = [self.words, self.time, self.generated]
        # add the buttons to the horizontal layout
        self.optionsLayout.addWidget(self.words)
        self.optionsLayout.addWidget(self.time)
        self.optionsLayout.addWidget(self.generated)
        # stretch on the right
        self.optionsLayout.addStretch(-1)
        # add the hor layout to the typing page layout
        self.typingPage.layout.addLayout(self.optionsLayout)

        # add 3 horizontal layouts to display the suboptions for each of the 3 options
        self.subOptionsWordsLayout = QHBoxLayout()
        self.subOptionsWordsLayout.setSpacing(10)
        self.subOptionsAILayout = QHBoxLayout()
        self.subOptionsAILayout.setSpacing(10)

        # create all the suboptions buttons
        self.words1 = OptionButton.OButton(self, "10", 35, False, "words")
        self.words2 = OptionButton.OButton(self, "25", 35, False, "words")
        self.words3 = OptionButton.OButton(self, "50", 35, False, "words")
        self.words4 = OptionButton.OButton(self, "100", 35, False, "words")
        # add the word suboptions to the horizontal layout
        self.subOptionsWordsLayout.addStretch(-1)
        self.subOptionsWordsLayout.addWidget(self.words1)
        self.subOptionsWordsLayout.addWidget(self.words2)
        self.subOptionsWordsLayout.addWidget(self.words3)
        self.subOptionsWordsLayout.addWidget(self.words4)

        self.time1 = OptionButton.OButton(self, "15", 35, False, "time")
        self.time2 = OptionButton.OButton(self, "30", 35, False, "time")
        self.time3 = OptionButton.OButton(self, "60", 35, False, "time")
        self.time4 = OptionButton.OButton(self, "120", 35, False, "time")
        # add time to the horizontal layout
        self.subOptionsWordsLayout.addWidget(self.time1)
        self.subOptionsWordsLayout.addWidget(self.time2)
        self.subOptionsWordsLayout.addWidget(self.time3)
        self.subOptionsWordsLayout.addWidget(self.time4)

        self.subOptionsWordsLayout.addStretch(-1)

        # add the horizontal layout to the typing page layout
        self.typingPage.layout.addLayout(self.subOptionsWordsLayout)

        # add the suboptions to the suboptions arr
        config.subOptions = [self.words1, self.words2, self.words3, self.words4, self.time1, self.time2, self.time3, self.time4]

        # make the time suboptions invisible since we start with words by default
        for i in range(4, len(config.subOptions)):
            config.subOptions[i].setVisible(False)

        # create a stack widget to hold the text box and results 
        self.stack = QStackedWidget()
        # remove the border around the stack widget
        self.stack.setStyleSheet("""
            border: none;
        """)
        # create a login page
        self.loginPage = Login.LoginPage(self)
        self.stack.addWidget(self.loginPage)
        # create a signup page
        self.signupPage = SignUpPage.SignUpPage(self)
        self.stack.addWidget(self.signupPage)
        # create the main text area
        self.textDisplay = Display.Passage(self)
        # add the text area to the typing page layout
        self.typingPage.layout.addStretch()
        self.typingPage.layout.addWidget(self.textDisplay)
        self.typingPage.layout.addStretch()
        # add the typing page to the stack widget
        self.stack.addWidget(self.typingPage)
        # add the results page to the stack widget
        self.results = Results.ResultsPage(self)
        self.stack.addWidget(self.results)
        
        # create the settings page
        self.settingsPage = SettingsPage.SettingsPage(self)
        
        # add the settings page to the stack widget
        self.stack.addWidget(self.settingsPage)
        #self.stack.setCurrentIndex(2)

        # add a profile page
        self.profilePage = ProfileTab.ProfileTab(self)
        self.stack.addWidget(self.profilePage)
        
        # add the stack widget to the main layout
        self.layout.addWidget(self.stack)

        # create a restart button
        self.restart = RestartButton.RestartButton(self, "Restart")
        # add the restart button to the typing page layout
        self.typingPage.layout.addWidget(self.restart)
        self.typingPage.layout.setAlignment(self.restart, Qt.AlignHCenter)
        # add a stretch to the typing page
        self.typingPage.layout.addStretch(-1)
        
        #---------------------------------------------------------------------------------------------------------------------#

        # add the infobar at the bottom
        self.infobarlayout = QHBoxLayout()
        # add a stretch to the infobar to center the snap button
        self.infobarlayout.addStretch(-1)
        # left, top, right, bottom
        self.infobarlayout.setContentsMargins(0, 0, 0, 0)
        self.infobarlayout.setSpacing(0)
        # create a button to go in the middle for snapping the window
        self.snapButton = SnapButton.SnapButton(self)
        # create a widget for the snapping options
        self.snapWidget = Snap.SnapBox(self)
        # add the snapbutton to theh infobar
        self.infobarlayout.addWidget(self.snapButton)
        # add a stretch
        self.infobarlayout.addStretch(1)
        # add another drop shadown
        self.shadow2 = QGraphicsDropShadowEffect()
        self.shadow2.setBlurRadius(8)
        self.shadow2.setXOffset(0)
        self.shadow2.setYOffset(-3)
        self.shadow2.setColor(QColor("black"))
        # add a drop shadow2 before the next thing
        self.dropshadow2 = QLabel("")
        self.dropshadow2.setStyleSheet("""
            background-color: """+config.backgroundColor+""";
            border: none;
            padding-top: 200px;
        
                                        """)
        self.dropshadow2.setFixedHeight(1)
        self.dropshadow2.setGraphicsEffect(self.shadow2)
        # hide infoBar if its false
        if config.infoBar == True:
            self.addInfoBar()
        
        # set the layout for the main window
        self.setLayout(self.layout)
        
        # the min height and width will be 500 x 500
        self.setMinimumSize(config.minSize, config.minSize)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.pressing = False
        self.movingPosition = False
        self.resizingWindow = False
        self.start = QPoint(0, 0)
        self.setStyleSheet("""
            background-color:"""+config.backgroundColor+""";
            border-style: solid;
            border-width: 1px;
            border-color:"""+config.accentColor+""";
                          """)
        # set the margins for the main window
        self.layout.setContentsMargins(config.MARGIN,config.MARGIN,config.MARGIN,config.MARGIN)
        # flags for starting location of resizing window
        self.left = False
        self.right = False
        self.bottom = False
        self.top = False
        self.bl = False
        self.br = False
        self.tl = False
        self.tr = False
        self.top = False
        self.setMouseTracking(True)
        # function to make it opaque if unfocused and blur if focused
        config.application.focusChanged.connect(self.on_focusChanged)
        # shortcuts to snap the window to left, right, up, down, and corners
        self.shortcut_snapLeft = QShortcut(QKeySequence('Ctrl+Alt+Left'), self)
        self.shortcut_snapLeft.activated.connect(lambda: self.snapWin("left"))
        self.shortcut_snapRight = QShortcut(QKeySequence('Ctrl+Alt+Right'), self)
        self.shortcut_snapRight.activated.connect(lambda: self.snapWin("right"))
        self.shortcut_snapTop = QShortcut(QKeySequence('Ctrl+Alt+Up'), self)
        self.shortcut_snapTop.activated.connect(lambda: self.snapWin("top"))
        self.shortcut_snapBottom = QShortcut(QKeySequence('Ctrl+Alt+Down'), self)
        self.shortcut_snapBottom.activated.connect(lambda: self.snapWin("bottom"))
        # display the login page if the user is not logged in
        if config.settings.value("user") == "":
            # show the login page
            self.stack.setCurrentIndex(0)
            # hide the profile button
            self.profileButton.setVisible(False)
            # hide the settings button if on the login page
            self.settingsButton.setVisible(False)
            # set the login qlineedit to be focused
            config.mainWin.loginPage.emailLabel.setFocus(True)
        # display the main text area if the user is logged in
        else:
            # display text area
            self.stack.setCurrentIndex(2)
            # set focus to the textbox
            self.textDisplay.setFocus()

    def addInfoBar(self):
        # add the infobar
        self.infoBar = QWidget()
        self.infoBar.setStyleSheet("""
            background-color:"""+config.backgroundColor+""";
            border: none;
        """)
        self.infoBar.setFixedHeight(20)
        self.infoBar.setLayout(self.infobarlayout)
        self.layout.addWidget(self.dropshadow2)
        # add the infobar to the main layout
        self.layout.addWidget(self.infoBar)

    def addBar(self):
        self.infoBar.setVisible(True)
        self.dropshadow2.setVisible(True)

    def removeBar(self):
        self.infoBar.setVisible(False)
        self.dropshadow2.setVisible(False)
    
    def snapWin(self, direction):
        global rightDown
        global leftDown
        global upDown
        global downDown
        global isMaximized
        
        # start with this so that we can maximize and restore over and over with the up button
        self.showNormal()
        config.isMaximized = False
        # get the current working resolution to account for things like the taskbar
        if operatingSystem == 'Windows':
            # get the current working resolution to account for things like the taskbar being displayed on windows
            monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
            working_resolution = monitor_info.get("Work")
            workingWidth = working_resolution[2]
            workingHeight = working_resolution[3]
        else:
            # if now windows then assume there is no taskbar
            resolution = config.application.desktop().screenGeometry()
            workingWidth = resolution.width()
            workingHeight = resolution.height()
        # determine if the taskbar is present by comparing the normal height to the working height
        isTaskbar = True
        difference = 100000
        for i in range(0, QDesktopWidget().screenCount()):
            if workingHeight == QDesktopWidget().screenGeometry(i).height():
                isTaskbar = False
                break
            # store the smallest difference to determine the correct difference due to the taskbar
            elif abs(QDesktopWidget().screenGeometry(i).height() - workingHeight) < difference:
                difference = QDesktopWidget().screenGeometry(i).height() - workingHeight
        
        # if the taskbar is present then use the working height
        if isTaskbar == True:
            workingWidth = QDesktopWidget().screenGeometry(self).width()
            workingHeight = QDesktopWidget().screenGeometry(self).height() - difference
        # if the taskbar is not present then just use the normal width and height
        else:
            workingWidth = QDesktopWidget().screenGeometry(self).width()
            workingHeight = QDesktopWidget().screenGeometry(self).height()
        
        monitor = QDesktopWidget().screenGeometry(self)

        # variables to store the inital position of the window
        startx = self.pos().x()
        starty = self.pos().y()

        self.move(monitor.left(), monitor.top())

        if direction == "place":
            #print(config.mainWin.pos().x())
            self.setGeometry(self.pos().x() + startx, self.pos().y() + starty, self.width(), self.height())
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False

        # middle window from right
        if direction == "left" and config.rightDown == True:
            self.setGeometry(int(monitor.left() + workingWidth/4), int(monitor.top()), int(workingWidth/2), int(workingHeight))
            # set the m all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # middle window from left
        elif direction == "right" and config.leftDown == True:
            self.setGeometry(int(monitor.left() + workingWidth/4), int(monitor.top()), int(workingWidth/2), int(workingHeight))
            # set the m all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap the window right
        elif direction == "right" and config.downDown == False and config.upDown == False:
            self.setGeometry(int(monitor.left() + workingWidth/2), int(monitor.top()), int(workingWidth/2), int(workingHeight))
            # set the right to true and the others to false
            config.rightDown = True
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap bottom right from bottom
        elif direction == "right" and config.downDown == True and config.upDown == False:
            self.setGeometry(int(monitor.left() + workingWidth/2), int(monitor.top() + workingHeight/2), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap bottom right from right
        elif direction == "bottom" and config.leftDown == False and config.rightDown == True:
            self.setGeometry(int(monitor.left() + workingWidth/2), int(monitor.top() + workingHeight/2), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False

        # snap bottom left from bottom
        elif direction == "left" and config.downDown == True and config.upDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top() + workingHeight/2), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap bottom left from left
        elif direction == "bottom" and config.leftDown == True and config.rightDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top() + workingHeight/2), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap top left from top
        elif direction == "left" and config.downDown == False and config.upDown == True:
            self.setGeometry(int(monitor.left()), int(monitor.top()), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # maximize
        elif direction == "top" and config.upDown == True:
            # click the max button
            self.setGeometry(int(monitor.left()), int(monitor.top()), int(workingWidth), int(workingHeight))
            config.isMaximized = True
            #self.layout.itemAt(0).widget().btn_max_clicked()
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap top left from left
        elif direction == "top" and config.leftDown == True and config.rightDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top()), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap top right from top
        elif direction == "right" and config.downDown == False and config.upDown == True:
            self.setGeometry(int(monitor.left() + workingWidth / 2), int(monitor.top()), int(workingWidth/2), int(workingHeight/2))
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False
        
        # snap top right from right
        elif direction == "top" and config.leftDown == False and config.rightDown == True:
            self.setGeometry(int(monitor.left() + workingWidth / 2), int(monitor.top()), int(workingWidth/2), int(workingHeight/2))   
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False

        # snap left
        elif direction == "left" and config.downDown == False and config.upDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top()), int(workingWidth/2), int(workingHeight))
            # set left to true and others to false
            config.leftDown = True
            config.rightDown = False
            config.downDown = False
            config.upDown = False

        # snap up
        elif direction == "top" and config.leftDown == False and config.rightDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top()), int(workingWidth), int(workingHeight / 2))
            # set up to True and all others to false
            config.upDown = True
            config.leftDown = False
            config.rightDown = False
            config.downDown = False
        
        # minimize
        elif direction == "bottom" and config.downDown == True:
            # click the min button
            self.layout.itemAt(0).widget().btn_min_clicked()
            # set all to false
            config.rightDown = False
            config.leftDown = False
            config.downDown = False
            config.upDown = False

        # snap down
        elif direction == "bottom" and config.leftDown == False and config.rightDown == False:
            self.setGeometry(int(monitor.left()), int(monitor.top() + workingHeight / 2), int(workingWidth), int(workingHeight / 2))
            # set Down to True and all others to false
            config.downDown = True
            config.upDown = False
            config.leftDown = False
            config.rightDown = False     
        
        mainPosition = config.mainWin.mapToGlobal(QPoint(0,config.mainWin.height()))
        self.snapWidget.hide()
        config.isSnapWidget = False

        # if resizing then change margins of the textDisplay
        # calculate margins
        if self.height() < config.tooSmall or self.width() < config.tooSmall:
            margin = 0
        else:
            margin = self.width() * 0.08
        marginStr = str(margin) + "px"
        self.textDisplay.setStyleSheet("""
        QTextEdit
        {
            background-color: """+config.backgroundColor+""";
            color: """+config.accentColor+""";
            border: none;
            selection-background-color: """+config.backgroundColor+""";
            selection-color: """+config.accentColor+""";
            margin-left: """+marginStr+""";
            margin-right: """+marginStr+""";
            margin-top: """+marginStr+"""
        }
        """)

        # if snapping we need to change the textDisplay
        self.textDisplay.generatePassage()
        # if snapping we need to change the scroll area size
        if config.infoBar == True:
            self.settingsPage.setMinimumHeight(self.height() - self.snapButton.height() - 100)
        else:
            self.settingsPage.setMinimumHeight(self.height() - self.snapButton.height() - 250)
    
    def on_focusChanged(self, old, new):
        # set the opacity to 1 if not focused
        if self.isActiveWindow():
            self.setWindowOpacity(config.opacity)
        else:
            self.setWindowOpacity(1.0)

    def mousePressEvent(self, event):
        pos = event.pos()
        # set pressing to true
        self.pressing = True
        if config.isMaximized == False:
            # if they clicked on the edge then we need to change pressing to true and resizingWindow to
            # true and we need to change the cursor shape.
            # top left
            if pos.x() <= 8 and pos.y() <= 8:
                self.resizingWindow = True
                self.start = event.pos()
                self.tl = True
            # top right
            elif pos.x() >= self.width() - 8 and pos.y() <= 8:
                self.resizingWindow = True
                self.start = event.pos()
                self.tr = True
            # top
            elif pos.y() <= 8 and pos.x() > 8 and pos.x() < self.width() - 8:
                self.resizingWindow = True
                self.start = event.pos().y()
                self.top = True     
            elif pos.y() >= self.height() - 8 and pos.x() <= 8 and pos.y() > 8:
                self.resizingWindow = True
                self.start = event.pos()
                self.bl = True
            elif pos.x() <= 8 and pos.y() > 8:
                self.resizingWindow = True
                self.start = event.pos().x()
                self.left = True   
            elif pos.x() >= self.width() - 8 and pos.y() >= self.height() - 8:
                self.resizingWindow = True
                self.start = event.pos()
                self.br = True    
            elif pos.x() >= self.width() - 8 and pos.y() > 8:
                self.resizingWindow = True
                self.start = event.pos().x()
                self.right = True              
            elif pos.x() > 8 and pos.x() < self.width() - 8 and pos.y() >= self.height() - 8:
                self.resizingWindow = True
                self.start = event.pos().y()
                self.bottom = True       
  
    def mouseMoveEvent(self, event):
        self.snapWidget.hide()
        config.isSnapWidget = False
        pos = event.pos()
        QApplication.setOverrideCursor(Qt.ArrowCursor)
        if config.isMaximized == False:
            # top left
            if pos.x() <= 10 and pos.y() <= 10:
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            # top right
            elif pos.x() >= self.width() - 8 and pos.y() <= 8:
                QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            # top
            elif pos.y() <= 5 and pos.x() > 5 and pos.x() < self.width() - 5:
                QApplication.setOverrideCursor(Qt.SizeVerCursor)
            # bottom left
            elif pos.y() >= self.height() - 8 and pos.x() <= 8:
                QApplication.setOverrideCursor(Qt.SizeBDiagCursor)
            # bottom right
            elif pos.x() >= self.width() - 8 and pos.y() >= self.height() - 8:
                QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
            # bottom
            elif pos.x() > 0 and pos.x() < self.width() - 8 and pos.y() >= self.height() - 8:
                QApplication.setOverrideCursor(Qt.SizeVerCursor)
            # left
            elif pos.x() <= 5 and pos.y() > 5:
                QApplication.setOverrideCursor(Qt.SizeHorCursor)
            # right
            elif pos.x() >= self.width() - 5 and pos.y() > 5:
                QApplication.setOverrideCursor(Qt.SizeHorCursor)
            else:
                QApplication.setOverrideCursor(Qt.ArrowCursor)
        # if they are resizing
        # need to subtract the movement from the width/height 
        # but also need to account for if they are resizing horizontally from the left or
        # vertically from the top because we need to shift the window to the right/down the same amount
        if self.pressing and self.resizingWindow:
            # if resizing then change margins of the textDisplay
            # calculate margins
            if self.height() < config.tooSmall or self.width() < config.tooSmall:
                margin = 0
            else:
                margin = self.width() * 0.08
            marginStr = str(margin) + "px"
            self.textDisplay.setStyleSheet("""
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
            # resize from the top
            if self.top == True:
                # resize from the top
                if self.height() - event.pos().y() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y() + event.pos().y(), self.width(), self.height() - event.pos().y())
            # resize from the top left
            if self.tl == True:
                # move both dimensions if both boundaries are okay
                if self.width() - event.pos().x() >= config.minSize and self.height() - event.pos().y() >= config.minSize:
                    self.setGeometry(self.pos().x() + event.pos().x(), self.pos().y() + event.pos().y(), self.width() - event.pos().x(), self.height() - event.pos().y())
                # move only top if width is already at its smallest
                elif self.height() - event.pos().y() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y() + event.pos().y(), self.width(), self.height() - event.pos().y())
                # move only left if height is at its smallest
                elif self.width() - event.pos().x() > config.minSize:
                    self.setGeometry(self.pos().x() + event.pos().x(), self.pos().y(), self.width() - event.pos().x(), self.height())
            
            # resize top right
            if self.tr == True:
                pos = event.pos().x() 
                # top right
                if self.height() - event.pos().y() >= config.minSize and self.width() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y() + event.pos().y(), pos, self.height() - event.pos().y())

                # resize from the top
                elif self.height() - event.pos().y() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y() + event.pos().y(), self.width(), self.height() - event.pos().y())
                elif self.width() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y(), pos, self.height()) 

            # resize from the left to the right
            if self.left == True:
                # resize from the left
                if self.width() - event.pos().x() > config.minSize:
                    self.setGeometry(self.pos().x() + event.pos().x(), self.pos().y(), self.width() - event.pos().x(), self.height())
            # resize from the right
            if self.right == True:
                pos = event.pos().x()
                if self.width() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y(), pos, self.height()) 
            # resize from the bottom
            if self.bottom == True:
                pos = event.pos().y()
                if self.height() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y(), self.width(), pos) 
            # resize from the bottom right
            if self.br == True:
                pos = event.pos()
                if self.height() >= config.minSize and self.width() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y(), pos.x(), pos.y()) 
            # resize from the bottom left
            if self.bl == True:
                pos = event.pos().y()
                if self.width() - event.pos().x() > config.minSize and self.height() >= config.minSize:
                    self.setGeometry(self.pos().x() + event.pos().x(), self.pos().y(), self.width() - event.pos().x(), pos)
                elif self.height() >= config.minSize:
                    self.setGeometry(self.pos().x(), self.pos().y(), self.width(), pos) 
                elif self.width() - event.pos().x() > config.minSize:
                    self.setGeometry(self.pos().x() + event.pos().x(), self.pos().y(), self.width() - event.pos().x(), self.height())
            # if resizing we need to change the scroll area size
            self.settingsPage.setMinimumHeight(self.height() - self.snapButton.height() - 100)
            
    # if the mouse button is released then set 'pressing' as false
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.RightButton:
            return
        self.pressing = False
        self.movingPosition = False
        if self.resizingWindow == True:
            self.textDisplay.generatePassage()
        self.resizingWindow = False
        self.left = False
        self.right = False
        self.bottom = False
        self.bl = False
        self.br = False
        self.tr = False
        self.tl = False
        self.top = False