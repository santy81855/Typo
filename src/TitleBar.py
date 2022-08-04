from PyQt5.QtWidgets import QHBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor
import config
from platform import system
operatingSystem = system()

# Windows
if operatingSystem == 'Windows':
    # to get the working monitor size
    from win32api import GetMonitorInfo, MonitorFromPoint

class MyBar(QWidget):
    def __init__(self, parent):
        super(MyBar, self).__init__()
        global titleBar
        btn_size = 35
        config.titleBar = self
        # make the main window the parent
        self.parent = parent
        # create the layout to store the titlebar and buttons horizontally
        self.layout = QHBoxLayout()
        # allow for 8 pixels at the right so we can resize right and top right
        # also 8 margin at the top so that the buttons don't get in the way of resizing
        # left, top, right, bottom
        # add left margin to account for 3 corner buttons so the title is centered
        self.layout.setContentsMargins((btn_size+25)*3,0,0,0)
        self.layout.setSpacing(0)
        self.title = QLabel(config.appName)
        self.title.setMouseTracking(True)

        self.btn_close = QPushButton("x")
        self.btn_close.clicked.connect(self.btn_close_clicked)
        # make the corner buttons more rectangular in the horizontal way
        self.btn_close.setFixedSize(btn_size+25,btn_size)
        self.btn_close.setStyleSheet("""
            QPushButton
            {
            background-color: """+config.backgroundColor+"""; 
            border:none;
            color:"""+config.accentColor+""";
            font: 14pt "Consolas";
            }
            QPushButton::hover
            {
                background-color :"""+config.closeButtonHoverColor+""";
                color: """+config.accentColor+""";
            }
                                """)
        self.btn_close.setMouseTracking(True)

        self.btn_min = QPushButton("-")
        self.btn_min.clicked.connect(self.btn_min_clicked)
        self.btn_min.setFixedSize(btn_size+25, btn_size)
        self.btn_min.setStyleSheet("""
            QPushButton
            {
            background-color: """+config.backgroundColor+"""; 
            border:none;
            color:"""+config.accentColor+""";
            font: 14pt "Consolas";
            }
            QPushButton::hover
            {
                background-color : """+config.accentColor+""";
                color: """+config.backgroundColor+""";
            }
                                """)
        self.btn_min.setMouseTracking(True)
        self.btn_max = QPushButton("+")
        self.btn_max.clicked.connect(self.btn_max_clicked)
        self.btn_max.setFixedSize(btn_size+25, btn_size)
        self.btn_max.setStyleSheet("""
            QPushButton
            {
            background-color: """+config.backgroundColor+"""; 
            border:none;
            color:"""+config.accentColor+""";
            font: 14pt "Consolas";
            }
            QPushButton::hover
            {
                background-color : """+config.accentColor+""";
                color: """+config.backgroundColor+""";
            }
                                """)
        self.btn_max.setMouseTracking(True)
        # give the title bar a height
        self.title.setFixedHeight(btn_size)
        self.title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.btn_min)
        self.layout.addWidget(self.btn_max)
        self.layout.addWidget(self.btn_close)

        self.title.setStyleSheet("""
            background-color: """+config.backgroundColor+""";
            border:none;
            color : """+config.accentColor+""";
            font: 14pt "Consolas";
            """)
        self.setLayout(self.layout)

        self.start = QPoint(0, 0)
        # flags for resizing or dragging window
        self.pressing = False
        self.movingPosition = False
        self.resizingWindow = False
        self.setMouseTracking(True)
        
        # variable to track right click
        self.rightpressing = False
    
    # close the main window when the close button in the menu bar is pressed
    def btn_close_clicked(self):
        self.parent.close()

    def btn_max_clicked(self):
        global isMaximized
        monitor = QDesktopWidget().screenGeometry(self.parent)
    
        # if it is clicked while we are currently maximized, then it means we need to revert to
        # lastPosition
        if config.isMaximized:
            #self.parent.move(monitor.left(), monitor.top())
            self.parent.showNormal()
            config.isMaximized = False
        # if it is not maximized
        else:
            # if the maximize button is pressed on the menubar, it should call the maximize function of
            # the parent window. It is a standard function, so it is not written in this code
            #self.parent.move(monitor.left(), monitor.top())
            self.parent.showMaximized()
            # toggle isMax so we know the state
            config.isMaximized = True

    def btn_min_clicked(self):
        # same with the show minimized
        self.parent.showMinimized()
    
    def mouseDoubleClickEvent(self, event):
        # only a left double click will max and restore
        if event.button() == 1:
            self.btn_max_clicked()
    
    def mousePressEvent(self, event):
        if event.button() == Qt.RightButton:
            self.rightpressing = True
        pos = event.pos()
        self.pressing = True
        if config.isMaximized == False:
            self.movingPosition = True
            self.start = self.mapToGlobal(event.pos())

    def mouseMoveEvent(self, event):
        if config.isSnapWidget == True:
            self.parent.snapWidget.hide()
            config.isSnapWidget = False
        pos = event.pos()
        # top left
        if pos.x() <= 3 and pos.y() <= 3:
            QApplication.setOverrideCursor(Qt.SizeFDiagCursor)
        
        else:
            QApplication.setOverrideCursor(Qt.ArrowCursor)
        if config.isMaximized == False:
            # moving the window
            if self.pressing and self.movingPosition:
                config.rightDown = False
                config.leftDown = False
                config.downDown = False
                config.upDown = False
                self.end = self.mapToGlobal(event.pos())
                self.movement = self.end-self.start
                self.parent.setGeometry(self.mapToGlobal(self.movement).x()-6,
                                    self.mapToGlobal(self.movement).y()-6,
                                    self.parent.width(),
                                    self.parent.height())
                self.start = self.end

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.RightButton:
            self.rightpressing = False
            self.pressing = False
            self.movingPosition = False
            # get the global positionn
            globalpos = QCursor()
            # get the current working resolution to account for things like the taskbar being displayed on windows
            if operatingSystem == 'Windows':
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
                workingWidth = QDesktopWidget().screenGeometry(self.parent).width()
                workingHeight = QDesktopWidget().screenGeometry(self.parent).height() - difference
            # if the taskbar is not present then just use the normal width and height
            else:
                workingWidth = QDesktopWidget().screenGeometry(self.parent).width()
                workingHeight = QDesktopWidget().screenGeometry(self.parent).height()
            
            leftLimit = workingWidth / 2
            rightLimit = workingWidth
            x = globalpos.pos().x()
            # if x is negative just reverse it
            if x < 0:
                x = workingWidth - abs(x)
            # if the mouse is in the left half then snap it left
            if x < leftLimit:
                self.parent.snapWin("left")
                #self.parent.setGeometry(0, 0, workingWidth/2, workingHeight)
                #config.leftDown = True
            # otherwise snap it to the right
            else:
                self.parent.snapWin("right")
                #self.parent.setGeometry(workingWidth / 2, 0, workingWidth/2, workingHeight)                            
                #config.rightDown = True
        else:
            self.pressing = False
            self.movingPosition = False
