#!/usr/bin/python

from Adafruit_Thermal import *
import socket

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

printer.feed(3)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    printer.println(s.getsockname()[0])
except:
    printer.println('Network is unreachable.')

printer.feed(1)