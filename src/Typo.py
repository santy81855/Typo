from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui
import sys
import config
import MainWindow

def createMain():
    # create the main window widget and display it
    mw = MainWindow.MainWindow()
    mw.show()

def mainFunction():
    config.application = QApplication(sys.argv)
    # configure the QSettings
    config.application.setOrganizationName(config.appAuthor)
    config.application.setApplicationName(config.appName)
    # set the logo
    config.application.setWindowIcon(QtGui.QIcon(config.logoName))   
    # find the resolution of the monitor the user is on
    screen_resolution = config.application.desktop().screenGeometry()
    width, height = screen_resolution.width(), screen_resolution.height()
    key = str(width) + "x" + str(height)
    startingLocation = []
    if key not in config.res:
        startingLocation = [500, 500]
    else:
        startingLocation = config.res[key]
    
    createMain()

    sys.exit(config.application.exec_())

if __name__ == "__main__":
    mainFunction()