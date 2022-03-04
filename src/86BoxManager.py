#!/usr/bin/env python3

from mainw import MainWin
from PyQt5 import QtCore, QtGui, QtWidgets
from util import loadOrNew
import sys
# Windows home + "AppData\Local\86BoxManPy\"
# Linux home + ".config/86BoxManPy/"
# Mac home + "Library/Application Support/86BoxManPy/86BoxManPy/"

if __name__ == "__main__":
    datadict = loadOrNew()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.ui = MainWin()
    MainWindow.ui.setupWin(MainWindow,datadict)
    MainWindow.show()
    sys.exit(app.exec_())
