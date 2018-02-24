# -*- coding:utf8 -*-
import os
import signal
import struct
class Fork(object):
    def __init__(self,server):
        self.server = server
        self.isRun = True
        #signal.signal(signal.SIGKILL,self.gexit)
        self.run()
    def run(self):
        while self.isRun:
            con, addr = self.server.accept()
            self.runRequest(con)
        os._exit()
    def runRequest(self,con):
        lines = con.recv(10240)
        slen = len(lines)
        head = lines[0:4]
        hh = struct.unpack("4B", head)
        hlen = hh[1] + hh[2] * 256
        index = 4
        hs = []
        while index < hlen + 4:
            ll = struct.unpack("2B", lines[index:index + 2])
            hlenindex = ll[0] + ll[1] * 256
            index += 2
            name = lines[index:index + hlenindex]
            index += hlenindex
            hs.append(name)
        print(hs)
        con.sendall(bytes("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 2\r\n\r\nOK",encoding="utf8"))
        con.close()

