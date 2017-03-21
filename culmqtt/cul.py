# -*- coding: utf-8 -*-
import os
import select
import time


def read_from_fd(fd):
    result = b""
    while not result.endswith(b"\n"):
        result += os.read(fd, 1)
    return result


class CUL(object):
    
    def __init__(self, serial_port):
        super(CUL, self).__init__()
        self._port = serial_port
        self._fd = os.open(self._port, os.O_RDWR)
        # initialize
        os.write(self._fd, b"V\n")
        time.sleep(1)
        os.write(self._fd, b"V\n")
        time.sleep(2)
        
    def __del__(self):
        os.close(self._fd)
        
    def send(self, msg):
        if not msg.endswith("\n"):
            msg += "\n"
        os.set_blocking(self._fd, True)
        os.write(self._fd, msg.encode("ascii"))
        
    def recv(self):
        rin, _, _ = select.select([self._fd], [], [], 0)
        if rin:
            fd = rin[0]
            return read_from_fd(fd)
        return None
