from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QApplication, QLabel, QDesktopWidget, QWidget, QPushButton, QFrame, QTextEdit
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QCursor, QFont
import config
import requests

class Passage(QTextEdit):
    def __init__(self, parent):
        super(Passage, self).__init__()
        self.parent = parent
        self.setStyleSheet("""
        QTextEdit
        {
            background-color: """+config.backgroundColor+""";
            color: """+config.accentColor1+""";
            border: none;
        }
        """)
        self.setMouseTracking(True)
        self.generatePassage()

    def mouseMoveEvent(self, event):
        QApplication.setOverrideCursor(Qt.IBeamCursor)

    def generatePassage(self):
        r = requests.post(
            "https://api.deepai.org/api/text-generator",
            data={
                'text': 'hello how are you',
            },
            headers={'api-key': 'f6550bae-e6ba-4f9e-8b71-14fa364eb51f'}
        )
        text = ""
        check = False
        for i in range(0, len(r.text)):
            if r.text[i] == "p" and r.text[i + 1] == "u" and r.text[i + 2] == "t":
                index = i + 6
                while r.text[index] != '}':
                    text = text + r.text[index]
                    index += 1
                break

        self.setText(text)