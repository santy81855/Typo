from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont, QTextCursor
import config, RestartButton

class ResultsPage(QWidget):
    def __init__(self, parent):
        super(ResultsPage, self).__init__()
        self.parent = parent
        # create a vertical layout
        self.vLayout = QVBoxLayout()
        # set the spacing
        self.vLayout.setSpacing(50)
        # create a Label to display wpm
        self.wpmLabel = QLabel("WPM")
        self.wpmLabel.setFont(QFont("Arial", 30))
        self.wpmLabel.setAlignment(Qt.AlignCenter)
        self.wpmLabel.setStyleSheet("""
        QLabel {
            background-color: """ + config.backgroundColor + """;
            color: """ + config.accentColor + """;
        }
        """)
        # create a Label to display accuracy
        self.accuracyLabel = QLabel("Accuracy")
        self.accuracyLabel.setFont(QFont("Arial", 30))
        self.accuracyLabel.setAlignment(Qt.AlignCenter)
        self.accuracyLabel.setStyleSheet("""
        QLabel {
            background-color: """ + config.backgroundColor + """;
            color: """ + config.accentColor + """;
        }
        """)
        # add stretch 
        self.vLayout.addStretch(-1)
        # add the labels to the vertical layout
        self.vLayout.addWidget(self.wpmLabel)
        self.vLayout.addWidget(self.accuracyLabel)
        # create a horizontal layout
        self.hLayout = QHBoxLayout()
        # set the spacing
        self.hLayout.setSpacing(0)
        # add stretch
        self.hLayout.addStretch(-1)
        # create a restart button
        self.restart = RestartButton.RestartButton(config.mainWin, "Restart")
        # add the restart button to the horizontal layout
        self.hLayout.addWidget(self.restart)
        # add stretch
        self.hLayout.addStretch(-1)
        # add the horizontal layout to the vertical layout
        self.vLayout.addLayout(self.hLayout)
        # add stretch
        self.vLayout.addStretch(-1)
        # set the layout
        self.setLayout(self.vLayout)
