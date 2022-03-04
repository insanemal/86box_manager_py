# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import os
from util import saveConfig
from settings_ui import Ui_settingsWindow


class settingsWindow(Ui_settingsWindow):
    def setupWin(self, settingsWindow,datadict):
        self.setupUi(settingsWindow)
        self.datadict = datadict
        if '86BoxPath' in datadict.keys():
            self.lineEdit.setText(datadict['86BoxPath'])
        if 'VMPath' in datadict.keys():
            self.lineEdit_2.setText(datadict['VMPath'])
        if 'RomOverride' in datadict.keys():
            state = datadict['RomOverride']
            self.romCheck.setChecked(state)
            self.lineEdit_3.setEnabled(state)
            self.browseRoms.setEnabled(state)
            if state:
                if 'RomPath' in datadict.keys():
                    self.lineEdit_3.setText(datadict['RomPath'])
        if 'LogEnable' in datadict.keys():
            state = datadict['LogEnable']
            self.checkBox.setChecked(state)
            self.lineEdit_4.setEnabled(state)
            self.logBrowse.setEnabled(state)

        self.romCheck.clicked.connect(self.romCheckClick)
        self.checkBox.clicked.connect(self.logCheckClick)
        self.browse86box.clicked.connect(self.browse86boxClick)
        self.browseVMstorage.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_2))
        self.browseRoms.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_3))
        self.logBrowse.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_4))
        self.settingsCancel.clicked.connect(lambda: settingsWindow.close())
        self.settingsOK.clicked.connect(lambda: self.validateConfig(settingsWindow))

    def logCheckClick(self):
        self.lineEdit_4.setEnabled(self.checkBox.isChecked())
        self.logBrowse.setEnabled(self.checkBox.isChecked())

    def romCheckClick(self):
        self.lineEdit_3.setEnabled(self.romCheck.isChecked())
        self.browseRoms.setEnabled(self.romCheck.isChecked())

    def browse86boxClick(self):
        import platform
        browse = QtWidgets.QFileDialog()
        browse.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        if platform.system() == "Windows":
            browse.setNameFilters(["EXE files (*.exe)"])
            browse.selectNameFilter("EXE files (*.exe)")
        if browse.exec_() == QtWidgets.QDialog.Accepted:
            filename = browse.selectedFiles()
            if filename:
                if os.path.exists(filename[0]):
                    self.lineEdit.setText(filename[0])

    def selectButtonDir(self,textbox):
        import platform
        browse = QtWidgets.QFileDialog()
        browse.setFileMode(QtWidgets.QFileDialog.Directory)
        browse.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if browse.exec_() == QtWidgets.QDialog.Accepted:
            filename = browse.selectedFiles()
            if filename:
                if os.path.exists(filename[0]):
                    textbox.setText(filename[0])

    def validateConfig(self,window):
        import pickle
        error = False
        if not os.path.exists(self.lineEdit.text()):
            error = True
            self.lineEdit.setStyleSheet("background-color: rgb(255, 0, 0)")
        if not os.path.exists(self.lineEdit_2.text()):
            error = True
            self.lineEdit_2.setStyleSheet("background-color: rgb(255, 0, 0)")
        if self.romCheck.isChecked():
            if not(os.path.exists(self.lineEdit_3.text())):
                error = True
                self.lineEdit_3.setStyleSheet("background-color: rgb(255, 0, 0)")
        if self.checkBox.isChecked():
            if not(os.path.exists(self.lineEdit_4.text())):
                error = True
                self.lineEdit_4.setStyleSheet("background-color: rgb(255, 0, 0)")
        if not(error):
            self.datadict["86BoxPath"] = self.lineEdit.text()
            self.datadict["VMPath"] = self.lineEdit_2.text()
            self.datadict['RomOverride'] = self.romCheck.isChecked()
            if self.romCheck.isChecked():
                self.datadict["RomPath"] = self.lineEdit_3.text()
            self.datadict['LogEnable'] = self.checkBox.isChecked()
            if self.checkBox.isChecked():
                self.datadict["LogPath"] = self.lineEdit_4.text()
            saveConfig(self.datadict)
            window.close()
        else:
            dlg = QtWidgets.QMessageBox(window)
            dlg.setWindowTitle("Invalid path/File")
            dlg.setText("Please review the settings")
            button = dlg.exec()

