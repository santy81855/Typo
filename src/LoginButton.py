from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir, QPropertyAnimation, QRect
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config, FirebaseAuth, FirebaseDB

class LoginButton(QPushButton):
    def __init__(self, parent, text, width, height):
        super(LoginButton, self).__init__()
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
        loginPage = self.parent
        if loginPage.emailLabel.text() == "":
            user = None
        else:
            # check if they put in their username rather than email
            user = FirebaseDB.get_user(loginPage.emailLabel.text())
        if user is not None:
            success = FirebaseAuth.signin(user['email'], loginPage.passLabel.text())
        else:
            success = FirebaseAuth.signin(loginPage.emailLabel.text(), loginPage.passLabel.text())
        # if they log in successfully go to the main page
        if success:
            # show all the options buttons
            config.mainWin.showOptions()
            # show the restart button
            config.mainWin.restart.setVisible(True)
            # show the settings button
            config.mainWin.settingsButton.setVisible(True)
            # show the profile button
            config.mainWin.profileButton.setVisible(True)
            config.mainWin.stack.setCurrentIndex(2)
        # if the login fails, tell them
        else:
            loginPage.emailLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            loginPage.passLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            loginPage.errorLabel.setStyleSheet("""
                background-color:"""+config.backgroundColor+""";
                color: """+config.errorColor+""";
            """)
        


        
        