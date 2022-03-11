import configparser
import socket


def read_settings(name: str) -> any:

    config = configparser.ConfigParser()
    config.read('settings.ini')
    
    for section in config.sections():
        if config[section]['hostname'] == socket.gethostname():
            section = config[section]
            break
    if section == None:
        raise Exception("can't find hostname in settings.ini")

    return section[name]