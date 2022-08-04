from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config, FirebaseAuth

class LogOutButton(QPushButton):
    def __init__(self, parent, text, width, height):
        super(LogOutButton, self).__init__()
        self.parent = parent
        self.setFixedSize(width, height)
        # create the font
        font = QFont()
        font.setFamily("Serif")
        font.setFixedPitch( True )
        font.setPointSize( 20 )
        self.setFont(font)
        self.setText(text)
        self.setStyleSheet("""
            background-color: """+config.textHighlight+""";
            color: """+config.backgroundColor+""";
            border-radius: 5px;
        """)
        self.clicked.connect(self.buttonPressed)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        # if used as the logout button
        if "out" in self.text().lower():
            # hide the profile button
            config.mainWin.profileButton.setVisible(False)
            config.settings.setValue("user", "")
            config.settings.setValue("username", "")
            config.mainWin.stack.setCurrentIndex(0)
        # if used as the back button right next to the log out button
        else:
            # go to typing page
            config.mainWin.stack.setCurrentIndex(2)
            # show the profile button
            config.mainWin.profileButton.setVisible(True)
            # show the settings button
            config.mainWin.settingsButton.setVisible(True)
            


        
        