# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os
from addvm_ui import Ui_addVM

class addVMC(Ui_addVM):
    def setupWin(self, addVM, datadict):
        self.setupUi(addVM)
        self.datadict = datadict
        self.lineEdit_2.textChanged.connect(self.vmNameChange)
        self.importCheckbox.clicked.connect(self.importCheckboxClick)
        self.browseImport.clicked.connect(self.browseImportClick)
        self.cancelButton.clicked.connect(lambda: addVM.close())
        self.addButton.clicked.connect(lambda: self.addButtonClick(addVM))

    def importCheckboxClick(self):
        self.lineEdit.setEnabled(self.importCheckbox.isChecked())
        self.browseImport.setEnabled(self.importCheckbox.isChecked())

    def browseImportClick(self):
        import platform
        browse = QtWidgets.QFileDialog()
        browse.setFileMode(QtWidgets.QFileDialog.Directory)
        browse.setOption(QtWidgets.QFileDialog.ShowDirsOnly)
        if browse.exec_() == QtWidgets.QDialog.Accepted:
            filename = browse.selectedFiles()
            if filename:
                if os.path.exists(filename[0]):
                    config_file = os.path.join(filename[0], '86box.cfg')
                    if os.path.exists(config_file):
                        self.lineEdit.setText(filename[0])
                        self.vmPathLabel.setText(filename[0])
                    else:
                        dlg = QtWidgets.QMessageBox(window)
                        dlg.setWindowTitle("86box.cfg not found")
                        dlg.setText("No VM config detected please confirm path and try again")
                        button = dlg.exec()

    def vmNameChange(self):
        if not(self.importCheckbox.checkState()):
            if 'VMPath' in self.datadict.keys():
                vmpath = self.datadict['VMPath']
                self.vmPathLabel.setText(os.path.join(vmpath,self.lineEdit_2.text()))


    def addButtonClick(self,window):
        name=self.lineEdit_2.text().strip()
        if len(name) > 0:
            name=self.lineEdit_2.text()
            description = self.lineEdit_3.text()
            path = self.vmPathLabel.text()
            if not(self.importCheckbox.isChecked()):
                if not(os.path.exists(path)):
                    os.mkdir(path)
            if not('VMList' in self.datadict.keys()):
                self.datadict['VMList'] = {}
            self.datadict['VMList'][name] = (description,path)
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
                    ops.append(name)
                    ops.append('-S')
                    p = subprocess.Popen(ops)
                    p.wait()
            from util import saveConfig
            saveConfig(self.datadict)
            if self.startVMcheck.checkState():
                self.datadict['RunVM'] = name
            window.close()






