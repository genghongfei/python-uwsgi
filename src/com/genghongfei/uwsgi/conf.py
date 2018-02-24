# -*- coding:utf8 -*-
import configparser
class Conf(object):
    def __init__(self,confFilePath):
        self.confFilePath = confFilePath
        config = configparser.ConfigParser()
        config.read_file(open(self.confFilePath))
        self.maxFork = config.getint('gapp','maxfork')
        self.pidFile = config.get('gapp', 'pidfile')
        self.port = config.getint('gapp', 'port')
    def getPidFile(self):
        return self.pidFile
    def getFork(self):
        return self.maxFork
    def getPort(self):
        return self.port

