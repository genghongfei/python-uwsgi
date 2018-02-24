# -*- coding:utf8 -*-
import os
import sys
import signal
import conf
import mainfork
class GApp(object):
    #
    def __init__(self):
        confFilePath = os.path.dirname(__file__) + "/gapp.ini"
        self.conf = conf.Conf(confFilePath)
        if len(sys.argv) > 1:
            if sys.argv[1] == 'stop':
                self.stop()
            elif sys.argv[1] == 'restart':
                self.restart()
            else:
                self.start()
        else:
            self.start()
    #
    def start(self):
        pidFile = self.conf.getPidFile()
        if os.path.exists(pidFile):
            print("Running")
        else:
            pid = os.fork()
            if pid == 0:
                mainfork.MainFork(self.conf)
        print("start")
    #
    def stop(self):
        pidFile = self.conf.getPidFile()
        if os.path.exists(pidFile):
            f = open(pidFile)
            pid = int(f.readline().strip())
            f.close()
            try:
                #signal.
                os.kill(pid,signal.SIGTERM)
            except:
                print("exit")
        print("STOP")
    #
    def restart(self):
        self.stop()
        self.start()

if __name__ == '__main__':
    gapp = GApp()