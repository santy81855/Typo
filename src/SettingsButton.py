from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog
from PyQt5.QtCore import Qt, QPoint, QDir, QProcess
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon
import config, RestartButton

class SettingsButton(QPushButton):
    def __init__(self, parent):
        super(SettingsButton, self).__init__()
        self.parent = parent
        self.setFixedSize(60, 30)
        self.setIcon(QIcon('images/settings_white.png'))
        self.setStyleSheet("""
            border: none;
            padding: 0px;
        """)
        self.clicked.connect(self.buttonPressed)
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        # hide all the options and suboptions
        for option in config.options:
            option.hide()
        for suboption in config.subOptions:
            suboption.hide()
        # move the stack to the settings page
        self.parent.stack.setCurrentIndex(4)
        # make the settings page big
        self.parent.settingsPage.setMinimumHeight(self.parent.height() - self.parent.snapButton.height() - 50)
        # hide the restart button
        self.parent.restart.hide()
        # hide the settings button
        self.hide()