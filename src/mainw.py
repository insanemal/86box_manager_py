# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from addvm import addVMC
from settings import settingsWindow
import subprocess
from main_ui import Ui_MainWindow

class MainWin(Ui_MainWindow):
    def setupWin(self, MainWindow,datadict):
        self.setupUi(MainWindow)
        self.window = MainWindow
        self.datadict = datadict
        self.runningVM = {}
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.timerFire)
        self.timer.setSingleShot(False)
        self.timer.setInterval(100)
        self.timer.start()
        self.addButton.clicked.connect(lambda: self.addButtonfunc(self.datadict))
        self.settingsButton.clicked.connect(lambda: self.settingsButtonClicked(self.datadict))
        self.configButton.clicked.connect(self.configButtonClicked)
        self.startButton.clicked.connect(self.startButtonClicked)
        self.removeButton.clicked.connect(self.removeButtonClicked)

    def errorBox(self,window,title,message):
        dlg = QtWidgets.QMessageBox(window)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        results = dlg.exec()


    def addButtonfunc(self, datadict):
        import os
        if not(os.path.exists(datadict['86BoxPath'])):
            self.errorBox(self.window,'Invalid 86Box path','Please review the settings and define a 86Box path')
            return
        elif not(os.path.exists(datadict['VMPath'])):
            self.errorBox(self.window,'Invalid VM storage path','Please review the settings and define a path to VM storage')
            return
        elif datadict['RomOverride']:
            if not(os.path.exists(datadict['RomPath'])):
                self.errorBox(self.window,'Invalid Rom storage path','Please review the settings and define a path to Rom Storage')
                return
        AddDialog = QtWidgets.QDialog()
        ui = addVMC()
        ui.setupWin(AddDialog, datadict)
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
        ui = settingsWindow()
        ui.setupWin(SettingsDialog, datadict)
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




