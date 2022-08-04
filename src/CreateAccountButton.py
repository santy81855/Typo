from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config, FirebaseAuth, FirebaseDB

class CreateAccountButton(QPushButton):
    def __init__(self, parent, text, width, height):
        super(CreateAccountButton, self).__init__()
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
        passwordMatch = (loginPage.passLabel.text() == loginPage.passLabel2.text())
        passwordEmpty = (loginPage.passLabel.text() == "" or loginPage.passLabel2.text() == "")

        error = False
        if passwordMatch and passwordEmpty == False:
            loginPage.errorLabel2.setStyleSheet("""
                    background-color:"""+config.backgroundColor+""";
                    color: """+config.backgroundColor+""";
            """)
            loginPage.passLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.accentColor+""";
                border-radius: 5px;
            """)
            loginPage.passLabel2.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.accentColor+""";
                border-radius: 5px;
            """)

        # if the user did not input anything for the email
        if loginPage.emailLabel.text() == "":
            loginPage.emailLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            error = True
        else:
            loginPage.emailLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.accentColor+""";
                border-radius: 5px;
            """)
        if loginPage.firstName.text() == "":
            loginPage.firstName.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            error = True
        else:
            loginPage.firstName.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.accentColor+""";
                border-radius: 5px;
            """)
        if loginPage.lastName.text() == "":
            loginPage.lastName.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            error = True
        else:
            loginPage.lastName.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.accentColor+""";
                border-radius: 5px;
            """)
        if loginPage.username.text() == "":
            loginPage.username.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            error = True
        else:
            loginPage.username.setStyleSheet("""
                    background-color: white;
                    color: """+config.backgroundColor+""";
                    border: 2px solid """+config.accentColor+""";
                    border-radius: 5px;
                """)
        if passwordMatch == False or passwordEmpty == True:
            loginPage.passLabel.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            loginPage.passLabel2.setStyleSheet("""
                background-color: white;
                color: """+config.backgroundColor+""";
                border: 2px solid """+config.errorColor+""";
                border-radius: 5px;
            """)
            loginPage.errorLabel2.setStyleSheet("""
                    background-color:"""+config.backgroundColor+""";
                    color: """+config.errorColor+""";
            """)
            error = True

        if error == True:
            return

        # Query database to ensure this is a unique username
        uniqueUserName = FirebaseDB.get_user(loginPage.username.text())
        # if we get a result for this username it means it is taken
        if uniqueUserName is not None:
            loginPage.errorLabelUser.setStyleSheet("""
                background-color:"""+config.backgroundColor+""";
                color: """+config.errorColor+""";
            """)

        # only proceed if they have entered the same password in both fields
        if (passwordMatch and not passwordEmpty and uniqueUserName is None):
            success = FirebaseAuth.signup(loginPage.emailLabel.text(), loginPage.passLabel.text(), loginPage.firstName.text(), loginPage.lastName.text(), loginPage.username.text())
            # if they successfully create account, go to the main page
            if success:
                # go to the typing page
                config.mainWin.stack.setCurrentIndex(2)
                # show the settings button
                config.mainWin.settingsButton.setVisible(True)
            # if the signup fails, tell them
            else:
                loginPage.emailLabel.setStyleSheet("""
                    background-color: white;
                    color: """+config.backgroundColor+""";
                    border: 2px solid """+config.errorColor+""";
                    border-radius: 5px;
                """)
                loginPage.errorLabel.setStyleSheet("""
                    background-color:"""+config.backgroundColor+""";
                    color: """+config.errorColor+""";
                """)
        


        
        