from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QLineEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, LoginButton, LoginInput, SignUp, GoogleButton

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
        self.title = QLabel("Sign In:")
        self.title.setFont(font)
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet("""
        QLabel {
            background-color: """ + config.backgroundColor + """;
            color: """ + config.accentColor + """;
        }
        """)
        # create a text area to enter their email/username
        self.emailLabel = LoginInput.LoginInput(self, "Email", 450, 60)
        # create a text area to enter their password
        self.passLabel = LoginInput.LoginInput(self, "Password", 450, 60)
        # create the error label
        self.errorLabel = QLabel("Incorrect email or password")
        self.errorLabel.setStyleSheet("""
            background-color: """ + config.backgroundColor + """;
            color: """ + config.backgroundColor + """;
        """)
        self.errorLabel.setFont(smallFont)
        self.errorLabel.setAlignment(Qt.AlignCenter)
        # create a button to sign in
        self.loginButton = LoginButton.LoginButton(self, "Login", self.passLabel.width(), self.passLabel.height())
        # create a layout for asking if they don't have an account
        self.smallLayout = QHBoxLayout()
        self.smallLayout.setSpacing(5)
        # add a label for if they don't have an account
        self.createAccountLabel = QLabel("Don't have an account?")
        self.createAccountLabel.setStyleSheet("""
            background-color: """ + config.backgroundColor + """;
            color: """ + config.accentColor + """;
        """)
        self.createAccountLabel.setFont(smallFont)
        # create a small button to sign up
        self.createAccountButton = SignUp.SignUpButton(self, "Sign Up", 60, 20)
        # add the labels to the small layout
        self.smallLayout.addStretch()
        self.smallLayout.addWidget(self.createAccountLabel)
        self.smallLayout.addWidget(self.createAccountButton)
        self.smallLayout.addStretch()

        # add the option to continue with google
        # create the button
        self.googleButton = GoogleButton.GoogleButton(self, "Continue with Google", self.passLabel.width(), self.passLabel.height())


        # add stretch 
        self.vLayout.addStretch(-1)
        # add the labels to the vertical layout
        self.vLayout.addWidget(self.title)
        self.vLayout.addSpacing(20)
        self.vLayout.addWidget(self.emailLabel)
        self.vLayout.addSpacing(30)
        self.vLayout.addWidget(self.passLabel)
        self.vLayout.addWidget(self.errorLabel)
        self.vLayout.addSpacing(20)
        self.vLayout.addWidget(self.loginButton)
        self.vLayout.addSpacing(20)
        self.vLayout.addLayout(self.smallLayout)
        self.vLayout.addSpacing(30)
        self.vLayout.addWidget(self.googleButton)
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
