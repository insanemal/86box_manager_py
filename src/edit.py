# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from edit_ui import Ui_editVM
import sys
from util import errorBox, saveConfig


class editVMiW(Ui_editVM):
    def setupWin(self, editVM, datadict, name, runningVM):
        self.setupUi(editVM)
        self.runningVM = runningVM
        self.datadict = datadict
        self.changed = False
        self.window = editVM
        self.vmName.setText(name)
        (description, path) = self.datadict['VMList'][name]
        self.vmname = name
        self.vmDescription.setText(description)
        self.vmPath.setText(path)
        self.vmName.textChanged.connect(self.setChanged)
        self.vmPath.textChanged.connect(self.setChanged)
        self.vmDescription.textChanged.connect(self.setChanged)
        self.editButton.clicked.connect(self.editButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

    def setChanged(self):
        self.changed = True

    def editButtonClicked(self):
        import os
        if self.changed:
            newName = self.vmName.text()
            newDesc = self.vmDescription.text()
            newPath = self.vmPath.text()
            if not(self.vmname in self.runningVM.keys()):
                if self.vmname in self.datadict['VMList'].keys():
                    nope,nope1 = self.datadict['VMList'].pop(self.vmname)
                if os.path.exists(newPath):
                    self.datadict['VMList'][newName] = (newDesc, newPath)
                    saveConfig(self.datadict)
                    if self.configureCheck.isChecked():
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
                            ops.append(newName)
                            ops.append('-S')
                            p = subprocess.Popen(ops)
                            p.wait()
                    if self.startVMcheck.checkState():
                        self.datadict['RunVM'] = newName
                else:
                    errorBox(self, self.window, "Error", "Path doesn't exist.")
            else:
                errorBox(self, self.window, "Error", "VM Still running. Cannot Edit")

        self.window.close()

    def cancelButtonClicked(self):
        self.window.close()

    def pathBrowseClicked(self):
        browse = QtWidgets.QFileDialog()
        browse.setFileMode(QtWidgets.QFileDialog.Directory)
        browse.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if browse.exec_() == QtWidgets.QDialog.Accepted:
            filename = browse.selectedFiles()
            if filename:
                if os.path.exists(filename[0]):
                    self.vmPath.setText(filename[0])
