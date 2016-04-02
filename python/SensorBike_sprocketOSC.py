#! /usr/bin/env python
from time import sleep
from math import *
import serial
import OSC

ser=serial.Serial ("/dev/ttyAMA0")
ser.baudrate = 115200
client = OSC.OSCClient()
client.connect(('127.0.0.1', 9001))

while 1:
	b = ser.read ()
	if (ord(b) / 10 == 1):
		d = 1
	else:
		d = 2
	m = OSC.OSCMessage("/ser")
	m.append(d)
	client.send(m)
