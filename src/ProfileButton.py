from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QPlainTextEdit, QScrollArea, QFileDialog, QComboBox
from PyQt5.QtCore import Qt, QPoint, QDir, QProcess
from PyQt5.QtGui import QCursor, QFont, QTextCursor, QIcon, QPixmap
import config, RestartButton

class ProfileButton(QPushButton):
    def __init__(self, parent):
        super(ProfileButton, self).__init__()
        self.parent = parent
        self.setFixedSize(60, 30)
        pixmap = QPixmap("images/profileIcon.png");
        profileIcon = QIcon(pixmap);
        self.setIcon(profileIcon)
        
        self.setStyleSheet("""
            border: none;
            padding: 0px;
        """)
        self.setMouseTracking(True)
        self.clicked.connect(self.buttonPressed)

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.PointingHandCursor)

    def buttonPressed(self):
        # switch to the profile page
        config.mainWin.stack.setCurrentIndex(5)
        # hide the profile button
        config.mainWin.profileButton.setVisible(False)