# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_settingsWindow(object):
    def setupUi(self, settingsWindow,datadict):
        settingsWindow.setObjectName("settingsWindow")
        settingsWindow.setWindowModality(QtCore.Qt.ApplicationModal)
        settingsWindow.resize(680, 300)
        self.datadict = datadict
        self.tabWidget = QtWidgets.QTabWidget(settingsWindow)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 661, 241))
        self.tabWidget.setObjectName("tabWidget")
        self.generalTab = QtWidgets.QWidget()
        self.generalTab.setObjectName("generalTab")
        self.lineEdit = QtWidgets.QLineEdit(self.generalTab)
        self.lineEdit.setGeometry(QtCore.QRect(100, 40, 461, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.generalTab)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 70, 461, 31))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.browse86box = QtWidgets.QPushButton(self.generalTab)
        self.browse86box.setGeometry(QtCore.QRect(560, 40, 86, 31))
        self.browse86box.setObjectName("browse86box")
        self.browseVMstorage = QtWidgets.QPushButton(self.generalTab)
        self.browseVMstorage.setGeometry(QtCore.QRect(560, 70, 86, 31))
        self.browseVMstorage.setObjectName("browseVMstorage")
        self.browseRoms = QtWidgets.QPushButton(self.generalTab)
        self.browseRoms.setEnabled(False)
        self.browseRoms.setGeometry(QtCore.QRect(560, 130, 86, 31))
        self.browseRoms.setObjectName("browseRoms")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.generalTab)
        self.lineEdit_3.setEnabled(False)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 130, 461, 31))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_3 = QtWidgets.QLabel(self.generalTab)
        self.label_3.setGeometry(QtCore.QRect(10, 40, 101, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.generalTab)
        self.label_4.setGeometry(QtCore.QRect(10, 70, 91, 31))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.generalTab)
        self.label_5.setGeometry(QtCore.QRect(10, 130, 101, 31))
        self.label_5.setObjectName("label_5")
        self.romCheck = QtWidgets.QCheckBox(self.generalTab)
        self.romCheck.setGeometry(QtCore.QRect(100, 110, 211, 21))
        self.romCheck.setObjectName("romCheck")
        self.tabWidget.addTab(self.generalTab, "")
        self.advancedTab = QtWidgets.QWidget()
        self.advancedTab.setObjectName("advancedTab")
        self.checkBox = QtWidgets.QCheckBox(self.advancedTab)
        self.checkBox.setGeometry(QtCore.QRect(10, 10, 181, 20))
        self.checkBox.setObjectName("checkBox")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.advancedTab)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 40, 551, 29))
        self.lineEdit_4.setEnabled(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.logBrowse = QtWidgets.QPushButton(self.advancedTab)
        self.logBrowse.setGeometry(QtCore.QRect(560, 40, 86, 31))
        self.logBrowse.setObjectName("logBrowse")
        self.logBrowse.setEnabled(False)
        self.tabWidget.addTab(self.advancedTab, "")
        self.aboutTab = QtWidgets.QWidget()
        self.aboutTab.setObjectName("aboutTab")
        self.label = QtWidgets.QLabel(self.aboutTab)
        self.label.setGeometry(QtCore.QRect(40, 0, 311, 51))
        font = QtGui.QFont()
        font.setPointSize(19)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.aboutTab)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 631, 101))
        self.label_2.setObjectName("label_2")
        self.tabWidget.addTab(self.aboutTab, "")
        self.settingsOK = QtWidgets.QPushButton(settingsWindow)
        self.settingsOK.setGeometry(QtCore.QRect(490, 260, 86, 31))
        self.settingsOK.setDefault(True)
        self.settingsOK.setObjectName("settingsOK")
        self.settingsCancel = QtWidgets.QPushButton(settingsWindow)
        self.settingsCancel.setGeometry(QtCore.QRect(580, 260, 86, 31))
        self.settingsCancel.setObjectName("settingsCancel")
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

        self.retranslateUi(settingsWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(settingsWindow)
        self.romCheck.clicked.connect(self.romCheckClick)
        self.checkBox.clicked.connect(self.logCheckClick)
        self.browse86box.clicked.connect(self.browse86boxClick)
        self.browseVMstorage.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_2))
        self.browseRoms.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_3))
        self.logBrowse.clicked.connect(lambda: self.selectButtonDir(self.lineEdit_4))
        self.settingsCancel.clicked.connect(lambda: settingsWindow.close())
        self.settingsOK.clicked.connect(lambda: self.validateConfig(settingsWindow))

    def retranslateUi(self, settingsWindow):
        _translate = QtCore.QCoreApplication.translate
        settingsWindow.setWindowTitle(_translate("settingsWindow", "Settings"))
        self.browse86box.setText(_translate("settingsWindow", "Browse"))
        self.browseVMstorage.setText(_translate("settingsWindow", "Browse"))
        self.browseRoms.setText(_translate("settingsWindow", "Browse"))
        self.label_3.setText(_translate("settingsWindow", "86Box Path:"))
        self.label_4.setText(_translate("settingsWindow", "Path to VMs:"))
        self.label_5.setText(_translate("settingsWindow", "Rom Path:"))
        self.romCheck.setText(_translate("settingsWindow", "Override default rom path"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.generalTab), _translate("settingsWindow", "General"))
        self.checkBox.setText(_translate("settingsWindow", "Enable Logging to file"))
        self.logBrowse.setText(_translate("settingsWindow", "Browse"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.advancedTab), _translate("settingsWindow", "Advanced"))
        self.label.setText(_translate("settingsWindow", "86Box Manager Lite"))
        self.label_2.setText(_translate("settingsWindow", "<html><head/><body><p>A config manager for 86Box<br/><br/>Version 0.0.1<br/><br/>Copyright 2022 Malcolm Haak</p><p>Licenced under the &lt;insert licence here&gt;</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.aboutTab), _translate("settingsWindow", "About"))
        self.settingsOK.setText(_translate("settingsWindow", "Ok"))
        self.settingsCancel.setText(_translate("settingsWindow", "Cancel"))

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
            browse.setFilter("EXE files (*.exe)")
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
            config_file = self.datadict["ConfigPath"]
            with open(config_file, 'wb') as handle:
                pickle.dump(self.datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            window.close()
        else:
            dlg = QtWidgets.QMessageBox(window)
            dlg.setWindowTitle("Invalid path/File")
            dlg.setText("Please review the settings")
            button = dlg.exec()

