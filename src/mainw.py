# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from addvm import Ui_addVM
from settings import Ui_settingsWindow
import subprocess

class Ui_MainWindow(object):
    def setupUi(self, MainWindow,datadict):
        self.datadict = datadict
        self.runningVM = {}
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 510)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerFire)
        self.timer.setSingleShot(False)
        self.timer.setInterval(100)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setGeometry(QtCore.QRect(10, 10, 41, 31))
        self.addButton.setObjectName("addButton")
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setGeometry(QtCore.QRect(50, 10, 41, 31))
        self.editButton.setObjectName("editButton")
        self.editButton.setEnabled = False
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setGeometry(QtCore.QRect(90, 10, 61, 31))
        self.removeButton.setObjectName("removeButton")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(170, 10, 86, 31))
        self.startButton.setObjectName("startButton")
        self.configButton = QtWidgets.QPushButton(self.centralwidget)
        self.configButton.setGeometry(QtCore.QRect(260, 10, 86, 31))
        self.configButton.setObjectName("configButton")
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setGeometry(QtCore.QRect(580, 10, 86, 31))
        self.settingsButton.setObjectName("settingsButton")
        self.vmTable = QtWidgets.QTableWidget(self.centralwidget)
        self.vmTable.setGeometry(QtCore.QRect(10, 50, 661, 441))
        self.vmTable.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.vmTable.setRowCount(0)
        self.vmTable.setColumnCount(4)
        self.vmTable.setObjectName("vmTable")
        item = QtWidgets.QTableWidgetItem()
        self.vmTable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.vmTable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.vmTable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.vmTable.setHorizontalHeaderItem(3, item)
        self.vmTable.horizontalHeader().setCascadingSectionResizes(False)
        self.vmTable.horizontalHeader().setStretchLastSection(True)
        self.vmTable.verticalHeader().setVisible(False)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.timer.start()
        self.addButton.clicked.connect(lambda: self.addButtonfunc(self.datadict))
        self.settingsButton.clicked.connect(lambda: self.settingsButtonClicked(self.datadict))
        self.configButton.clicked.connect(self.configButtonClicked)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "86Box Manager Lite"))
        self.addButton.setText(_translate("MainWindow", "Add"))
        self.editButton.setText(_translate("MainWindow", "Edit"))
        self.removeButton.setText(_translate("MainWindow", "Remove"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.configButton.setText(_translate("MainWindow", "Configure"))
        self.settingsButton.setText(_translate("MainWindow", "Settings"))
        item = self.vmTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Name"))
        item = self.vmTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Status"))
        item = self.vmTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Description"))
        item = self.vmTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Path"))

    def addButtonfunc(self, datadict):
        AddDialog = QtWidgets.QDialog()
        ui = Ui_addVM()
        ui.setupUi(AddDialog, datadict)
        AddDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        AddDialog.exec_()
        if 'RunVM' in self.datadict.keys():
            name = self.datadict.pop('RunVM')
            desc,path = self.datadict['VMList'][name]
            if '86BoxPath' in self.datadict.keys():
                ops=[]
                ops.append(self.datadict['86BoxPath'])
                if 'RomOverride' in self.datadict.keys():
                    if self.datadict['RomOverride']:
                        ops.append('-R')
                        ops.append(self.datadict['RomPath'])
                if 'LogEnable' in self.datadict.keys():
                    if self.datadict['LogEnable']:
                        import os
                        ops.append('-L')
                        log_path = os.path.join(self.datadict['LogPath'],name+'.log')
                        ops.append(log_path)
                ops.append('-P')
                ops.append(path)
                ops.append('-V')
                ops.append(name)
                self.runningVM[name] = subprocess.Popen(ops)

    def removeButtonClicked(self):
        items = self.vmTable.selectedItems()
        if len(items) > 0:
            name = items[0].text()
            if name not in self.runningVM.keys():
                desc,path = self.datadict['VMList'][name]
                import shutil
                import os
                ignore = self.datadict['VMList'].pop(name)
                if os.path.exists(path):
                    shutil.rmtree(path)
                import pickle
                config_file = self.datadict["ConfigPath"]
                with open(config_file, 'wb') as handle:
                    pickle.dump(self.datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def settingsButtonClicked(self, datadict):
        SettingsDialog = QtWidgets.QDialog()
        ui = Ui_settingsWindow()
        ui.setupUi(SettingsDialog, datadict)
        SettingsDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        SettingsDialog.exec_()

    def configButtonClicked(self):
        items = self.vmTable.selectedItems()
        if len(items) > 0:
            name = items[0].text()
            if name not in self.runningVM.keys():
                desc,path = self.datadict['VMList'][name]
                if '86BoxPath' in self.datadict.keys():
                    import subprocess
                    ops = []
                    ops.append(self.datadict['86BoxPath'])
                    if 'RomOverride' in self.datadict.keys():
                        if self.datadict['RomOverride']:
                            ops.append('-R')
                            ops.append(self.datadict['RomPath'])
                    ops.append('-P')
                    ops.append(path)
                    ops.append('-V')
                    ops.append(name)
                    ops.append('-S')
                    p = subprocess.Popen(ops)
                    p.wait()

    def startButtonClicked(self):
        items = self.vmTable.selectedItems()
        if len(items) > 0:
            name = items[0].text()
            if name not in self.runningVM.keys():
                desc,path = self.datadict['VMList'][name]
                if '86BoxPath' in self.datadict.keys():
                    import subprocess
                    ops = []
                    ops.append(self.datadict['86BoxPath'])
                    if 'RomOverride' in self.datadict.keys():
                        if self.datadict['RomOverride']:
                            ops.append('-R')
                            ops.append(self.datadict['RomPath'])
                    if 'LogEnable' in self.datadict.keys():
                        if self.datadict['LogEnable']:
                            import os
                            ops.append('-L')
                            log_path = os.path.join(self.datadict['LogPath'],name+'.log')
                            ops.append(log_path)
                    ops.append('-P')
                    ops.append(path)
                    ops.append('-V')
                    ops.append(name)
                    self.runningVM[name] = subprocess.Popen(ops)


    def timerFire(self):
        stopped = []
        if len(self.runningVM) > 0 :
            for name in self.runningVM:
                if not(self.runningVM[name].poll() == None):
                    stopped.append(name)
        if len(stopped)  > 0:
            for vm in stopped:
                ignore = self.runningVM.pop(vm)
        if 'VMList' in self.datadict.keys():
            if len(self.datadict['VMList']) > 0:
                self.vmTable.setRowCount(len(self.datadict['VMList']))
                rowc=0
                for name in self.datadict['VMList']:
                    desc,path = self.datadict['VMList'][name]
                    if name in self.runningVM.keys():
                        stat = "Running"
                    else:
                        stat  = "Stopped"
                    self.vmTable.setItem(rowc, 0, QtWidgets.QTableWidgetItem(name))
                    self.vmTable.setItem(rowc, 2, QtWidgets.QTableWidgetItem(desc))
                    self.vmTable.setItem(rowc, 1, QtWidgets.QTableWidgetItem(stat))
                    self.vmTable.setItem(rowc, 3, QtWidgets.QTableWidgetItem(path))
                    rowc +=1
            if self.vmTable.rowCount() > len(self.datadict['VMList']):
                self.vmTable.setRowCount(len(self.datadict['VMList']))




