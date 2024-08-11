# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/main.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(680, 510)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 17, -1)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addButton = QtWidgets.QPushButton(self.centralwidget)
        self.addButton.setObjectName("addButton")
        self.horizontalLayout.addWidget(self.addButton)
        self.editButton = QtWidgets.QPushButton(self.centralwidget)
        self.editButton.setObjectName("editButton")
        self.horizontalLayout.addWidget(self.editButton)
        self.removeButton = QtWidgets.QPushButton(self.centralwidget)
        self.removeButton.setObjectName("removeButton")
        self.horizontalLayout.addWidget(self.removeButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(-1, -1, 17, -1)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout_2.addWidget(self.startButton)
        self.configButton = QtWidgets.QPushButton(self.centralwidget)
        self.configButton.setObjectName("configButton")
        self.horizontalLayout_2.addWidget(self.configButton)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.settingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.settingsButton.setObjectName("settingsButton")
        self.horizontalLayout_3.addWidget(self.settingsButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.vmTable = QtWidgets.QTableWidget(self.centralwidget)
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
        self.verticalLayout.addWidget(self.vmTable)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

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
