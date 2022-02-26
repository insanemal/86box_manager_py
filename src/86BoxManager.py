#!/usr/bin/env python3

from mainw import Ui_MainWindow
from PyQt5 import QtCore, QtGui, QtWidgets
from os import path
import pickle

# Windows home + "AppData\Local\86BoxManPy\"
# Linux home + ".config/86BoxManPy/"
# Mac Todo

def newpickle(config_file,datadict):
    with open(config_file, 'wb') as handle:
        datadict["ConfigVersion"] = "1"
        datadict["ConfigPath"] = config_file
        pickle.dump(datadict, handle, protocol=pickle.HIGHEST_PROTOCOL)



def genConfPath():
    from pathlib import Path
    import platform
    home = str(Path.home())
    if platform.system() == "Linux":
        return path.join(home,'.config/86BoxManPy/')
    elif platform.system() == "Windows":
        return path.join(home, 'AppData\\Local\\86BoxManPy\\')
    elif platform.system == "Darwin":
        return "Not implemented"

if __name__ == "__main__":
    import sys
    from os import mkdir
    config_path = genConfPath()
    config_file = path.join(config_path, 'config.pickle')
    if not path.exists(config_path):
        mkdir(config_path)
    if path.exists(config_file):
        try:
            with open(config_file, 'rb') as handle:
                datadict = pickle.load(handle)
                datadict["ConfigPath"] = config_file
                print(datadict)

                if 'Version' not in datadict.keys():
                    if 'VMList' in datadict.keys():
                        ignore = datadict.pop('VMList')
                    datadict['Version'] = 1
        except EOFError as e:
            datadict = {}
            datadict['Version'] = 1
            newpickle(config_file, datadict)
    else:
        datadict = {}
        newpickle(config_file, datadict)
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow,datadict)
    MainWindow.show()
    sys.exit(app.exec_())
