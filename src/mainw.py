# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork, Qt
from addvm import addVMC
from settings import settingsWindow
import subprocess
from main_ui import Ui_MainWindow
from edit import editVMiW

class MainWin(Ui_MainWindow):
    def setupWin(self, MainWindow,datadict):
        self.setupUi(MainWindow)
        self.window = MainWindow
        self.datadict = datadict
        self.runningVM = {}
        self.window = MainWindow
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
        self.editButton.clicked.connect(self.editButtonClicked)

    def sendMessage(self,name,message):
        if name in self.runningVM.keys():
            block = QtCore.QByteArray()
            out = QtCore.QTextStream(block, QtCore.QIODevice.WriteOnly)
            out << message + "\n"
            out.flush()
            print(block)
            if 'client' in self.runningVM[name].keys():
                self.runningVM[name]['client'].write(block)
                self.runningVM[name]['client'].flush()

    def errorBox(self,window,title,message):
        dlg = QtWidgets.QMessageBox(window)
        dlg.setWindowTitle(title)
        dlg.setText(message)
        results = dlg.exec()

    def editButtonClicked(self):
        items = self.vmTable.selectedItems()
        if len(items) >0:
            name = items[0].text()
            if not(name in self.runningVM.keys()):
                editDialog = QtWidgets.QDialog()
                edit = editVMiW()
                edit.setupWin(editDialog, self.datadict, name, self.runningVM)
                editDialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                editDialog.exec_()
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
                        server = QtNetwork.QLocalServer()
                        socketName = name+str(os.getpid())
                        server.listen(socketName)
                        server.newConnection.connect(lambda: self.socketConnect(name))
                        new_env = os.environ
                        new_env["86BOX_MANAGER_SOCKET"] = socketName
                        self.runningVM[name] = {'process':subprocess.Popen(ops, env=new_env),'server': server}


    def socketConnect(self,name):
        import time
        print("Socket connected:"+name)
        self.runningVM[name]['client'] = self.runningVM[name]['server'].nextPendingConnection()
        print(self.runningVM[name]['client'])
        self.runningVM[name]['client'].disconnected.connect(self.runningVM[name]['client'].deleteLater)

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
                server = QtNetwork.QLocalServer()
                socketName = name+str(os.getpid())
                server.listen(socketName)
                server.newConnection.connect(lambda: self.socketConnect(name))
                new_env = os.environ
                new_env["86BOX_MANAGER_SOCKET"] = socketName
                self.runningVM[name] = {'process':subprocess.Popen(ops, env=new_env),'server': server}

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
                from util import saveConfig
                saveConfig(self.datadict)

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
        import os
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
                            ops.append('-L')
                            log_path = os.path.join(self.datadict['LogPath'],name+'.log')
                            ops.append(log_path)
                    ops.append('-P')
                    ops.append(path)
                    ops.append('-V')
                    ops.append(name)
                    server = QtNetwork.QLocalServer()
                    socketName = name+str(os.getpid())
                    if server.listen(socketName):
                        server.newConnection.connect(lambda: self.socketConnect(name))
                    new_env = os.environ
                    new_env["86BOX_MANAGER_SOCKET"] = socketName
                    self.runningVM[name] = {'process':subprocess.Popen(ops, env=new_env),'server': server}


    def timerFire(self):
        stopped = []
        if len(self.runningVM) > 0 :
            for name in self.runningVM:
                process = self.runningVM[name]['process']
                if not(process.poll() == None):
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




