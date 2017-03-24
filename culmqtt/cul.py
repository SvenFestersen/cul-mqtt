# -*- coding: utf-8 -*-
import logging
import os
import select
import time


def read_from_fd(fd):
    result = b""
    while not result.endswith(b"\n"):
        result += os.read(fd, 1)
    return result


class CUL(object):
    
    def __init__(self, serial_port, log_level=logging.ERROR):
        super(CUL, self).__init__()
        self._port = serial_port
        self._fd = os.open(self._port, os.O_RDWR)
        # initialize
        os.write(self._fd, b"V\n")
        time.sleep(1)
        os.write(self._fd, b"V\n")
        time.sleep(2)
        self._logger = logging.getLogger("cul-mqqt.CUL")
        self._logger.setLevel(log_level)
        self._logger.info("CUL configured and ready.")
        self._logger.debug("Using serial port {0}.".format(serial_port))
        
    def __del__(self):
        os.close(self._fd)
        
    def send(self, msg):
        if type(msg) == bytes:
            msg = msg.decode("ascii")
        if not msg.endswith("\n"):
            msg += "\n"
        os.set_blocking(self._fd, True)
        os.write(self._fd, msg.encode("ascii"))
        self._logger.debug("Message transmitted: '{0}'.".format(msg.strip()))
        
    def recv(self):
        rin, _, _ = select.select([self._fd], [], [], 0)
        if rin:
            fd = rin[0]
            msg = read_from_fd(fd)
            self._logger.debug("Message received: '{0}'.".format(msg.strip()))
            return msg
        return None
