# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets
import os

class Ui_addVM(object):
    def setupUi(self, addVM, datadict):
        addVM.setObjectName("addVM")
        addVM.setWindowModality(QtCore.Qt.ApplicationModal)
        addVM.resize(580, 250)
        self.datadict = datadict
        self.importCheckbox = QtWidgets.QCheckBox(addVM)
        self.importCheckbox.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.importCheckbox.setObjectName("importCheckbox")
        self.lineEdit = QtWidgets.QLineEdit(addVM)
        self.lineEdit.setEnabled(False)
        self.lineEdit.setGeometry(QtCore.QRect(10, 40, 481, 29))
        self.lineEdit.setObjectName("lineEdit")
        self.browseImport = QtWidgets.QPushButton(addVM)
        self.browseImport.setEnabled(False)
        self.browseImport.setGeometry(QtCore.QRect(490, 40, 86, 31))
        self.browseImport.setObjectName("browseImport")
        self.lineEdit_2 = QtWidgets.QLineEdit(addVM)
        self.lineEdit_2.setGeometry(QtCore.QRect(100, 80, 471, 29))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_3 = QtWidgets.QLineEdit(addVM)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 110, 471, 29))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.nameLabel = QtWidgets.QLabel(addVM)
        self.nameLabel.setGeometry(QtCore.QRect(10, 80, 71, 31))
        self.nameLabel.setObjectName("nameLabel")
        self.descriptionLabel = QtWidgets.QLabel(addVM)
        self.descriptionLabel.setGeometry(QtCore.QRect(10, 114, 91, 21))
        self.descriptionLabel.setObjectName("descriptionLabel")
        self.label_3 = QtWidgets.QLabel(addVM)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 63, 21))
        self.label_3.setObjectName("label_3")
        self.vmPathLabel = QtWidgets.QLabel(addVM)
        self.vmPathLabel.setGeometry(QtCore.QRect(60, 150, 511, 21))
        self.vmPathLabel.setObjectName("vmPathLabel")
        self.startVMcheck = QtWidgets.QCheckBox(addVM)
        self.startVMcheck.setGeometry(QtCore.QRect(10, 180, 151, 20))
        self.startVMcheck.setObjectName("startVMcheck")
        self.configureCheck = QtWidgets.QCheckBox(addVM)
        self.configureCheck.setGeometry(QtCore.QRect(170, 180, 181, 20))
        self.configureCheck.setObjectName("configureCheck")
        self.addButton = QtWidgets.QPushButton(addVM)
        self.addButton.setGeometry(QtCore.QRect(400, 210, 86, 31))
        self.addButton.setDefault(True)
        self.addButton.setObjectName("addButton")
        self.cancelButton = QtWidgets.QPushButton(addVM)
        self.cancelButton.setGeometry(QtCore.QRect(490, 210, 86, 31))
        self.cancelButton.setObjectName("cancelButton")

        self.retranslateUi(addVM)
        QtCore.QMetaObject.connectSlotsByName(addVM)

        self.lineEdit_2.textChanged.connect(self.vmNameChange)
        self.importCheckbox.clicked.connect(self.importCheckboxClick)
        self.browseImport.clicked.connect(self.browseImportClick)
        self.cancelButton.clicked.connect(lambda: addVM.close())
        self.addButton.clicked.connect(lambda: self.addButtonClick(addVM))

    def retranslateUi(self, addVM):
        _translate = QtCore.QCoreApplication.translate
        addVM.setWindowTitle(_translate("addVM", "Add VM"))
        self.importCheckbox.setText(_translate("addVM", "Import VM"))
        self.browseImport.setText(_translate("addVM", "Browse"))
        self.nameLabel.setText(_translate("addVM", "Name:"))
        self.descriptionLabel.setText(_translate("addVM", "Description:"))
        self.label_3.setText(_translate("addVM", "Path:"))
        self.vmPathLabel.setText(_translate("addVM", "         "))
        self.startVMcheck.setText(_translate("addVM", "Start this VM now"))
        self.configureCheck.setText(_translate("addVM", "Configure this VM now"))
        self.addButton.setText(_translate("addVM", "Add"))
        self.cancelButton.setText(_translate("addVM", "Cancel"))

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
            import pickle
            config_file = self.datadict["ConfigPath"]
            with open(config_file, 'wb') as handle:
                pickle.dump(self.datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)
            if self.startVMcheck.checkState():
                self.datadict['RunVM'] = name
        window.close()






