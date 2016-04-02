#! /usr/bin/env python
import serial
from time import sleep

ser=serial.Serial ("/dev/ttyAMA0")
ser.baudrate = 115200
#data = ser.read(10)
for w in range(10):
	ser.write("a")
	sleep (1)

