import json


def createV1Config():
    v1 = {}
    v1["Version"] = 1
    v1["ConfigPath"] = ""
    v1["VMList"] = {}
    v1["86BoxPath"] = ""
    v1["VMPath"] = ""
    v1["RomOverride"] = False
    v1["RomPath"] = ""
    v1["LogEnable"] = False
    v1["LogPath"] = ""
    return v1

def createConfig():
    return createV1Config()


def genConfPath():
    from pathlib import Path
    from os import path
    import platform
    home = str(Path.home())
    if platform.system() == "Linux":
        return path.join(home,'.config/86BoxManPy/')
    elif platform.system() == "Windows":
        return path.join(home, 'AppData\\Local\\86BoxManPy\\')
    elif platform.system == "Darwin":
        return path.join(home, 'Library/Application Support/86BoxManPy/86BoxManPy/')

def saveConfig(config):
    with open(config['ConfigPath'], 'w') as handle:
        json.dump(config, handle)

def loadOrNew():
    from os import path
    import sys
    from os import mkdir
    config_path = genConfPath()
    config_file = path.join(config_path, 'config.json')
    if not path.exists(config_path):
        mkdir(config_path)
    if path.exists(config_file):
        try:
            with open(config_file) as handle:
                datadict = json.load(handle)
                datadict["ConfigPath"] = config_file
                # If later versions exist put convertion code here

        except EOFError as e:
            datadict = createConfig()
            datadict["ConfigPath"] = config_file
            saveConfig(datadict)
    else:
        datadict = createConfig()
        datadict["ConfigPath"] = config_file
        saveConfig(datadict)
    return datadict

