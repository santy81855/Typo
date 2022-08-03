from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QLineEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, LogOutButton

class ProfileTab(QWidget):
    def __init__(self, parent):
        super(ProfileTab, self).__init__()
        self.parent = parent
        # create the main layout to be horizontal so everything is centered
        self.layout = QHBoxLayout()
        # set the spacing
        self.layout.setSpacing(0)
        # create a vertical layout
        self.vLayout = QVBoxLayout()
        # set the spacing
        self.vLayout.setSpacing(0)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        # create font for typed text
        typedFont = QFont()
        typedFont.setFamily("Serif")
        typedFont.setFixedPitch( True )
        typedFont.setPointSize( 15 )
        # "don't have an account" font
        smallFont = QFont()
        smallFont.setFamily("Serif")
        smallFont.setFixedPitch( True )
        smallFont.setItalic(True)
        smallFont.setPointSize( 10 )
        # create a title label 
        self.title = QLabel("Hello, {}!:".format(config.settings.value("username")))
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
        QLabel {
            background-color: """ + config.backgroundColor + """;
            color: """ + config.accentColor + """;
        }
        """)

        # create a button to sign in
        self.loginButton = LogOutButton.LogOutButton(self, "Logout", 60, 30)

        # add stretch 
        self.vLayout.addStretch(-1)
        # add the labels to the vertical layout
        self.vLayout.addWidget(self.title)
        self.vLayout.addSpacing(20)
        self.vLayout.addWidget(self.loginButton)

        # add stretch
        self.vLayout.addStretch(-1)
        # add a stretch to main layout
        self.layout.addStretch(-1)
        # add the vertical layout to the main layout
        self.layout.addLayout(self.vLayout)
        # add a stretch to main layout
        self.layout.addStretch(-1)
        # set the layout
        self.setLayout(self.layout)
        self.setMouseTracking(True)
    
    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.ArrowCursor)
