# -*- coding:utf8 -*-
import os
import signal
import socket
import fork
class MainFork(object):
    def __init__(self,conf):
        signal.signal(signal.SIGTERM, self.gexit)
        self.subpids = []
        self.conf = conf
        self.start()



    #
    def start(self):
        pidFile = self.conf.getPidFile()
        pid = os.getpid()
        f = open(pidFile, "w+")
        f.write(str(pid))
        f.close()
        self.run()
        signal.pause()

    def run(self):
        maxForx = self.conf.getFork()
        port = self.conf.getPort()
        sd = self.initSocket(port)
        for i in range(maxForx):
            pid = os.fork()
            if pid == 0:
                fork.Fork(sd)
                os._exit()
            else:
                self.subpids.append(pid)
    def initSocket(self,port):
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sd.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
        sd.bind(("127.0.0.1", port))
        print(port)
        sd.listen(0)
        return sd

    #
    def gexit(self,signum, frame):
        print("====")
        print(self.subpids)
        pidFile = self.conf.getPidFile()
        os.unlink(pidFile)
        for pid in self.subpids:
            print(pid)
            os.kill(pid,signal.SIGKILL)
