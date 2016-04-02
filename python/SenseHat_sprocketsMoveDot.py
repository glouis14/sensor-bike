#! /usr/bin/env python
from sense_hat import SenseHat
from time import sleep
from math import *
import serial

sh = SenseHat()
ser=serial.Serial ("/dev/ttyAMA0")
ser.baudrate = 115200

red = (255, 0, 0)
di = 0
data = 0
	
def drawDot (x, y):
	sh.clear()
	xi = trunc(x)
	xf = x- xi
	yi = trunc(y)
	yf = y - yi
	r = 1.0 - sqrt (xf*xf+yf*yf) / sqrt(2)
	sh.set_pixel (xi, yi, int(red[0] * r), int(red[1] * r), int(red[2] * r))
	r = 1.0 - sqrt (xf*xf+(1.0-yf)*(1.0-yf)) / sqrt(2)
	sh.set_pixel (xi, yi+1, int(red[0] * r), int(red[1] * r), int(red[2] * r))
	r = 1.0 - sqrt ((1.0-xf)*(1.0-xf)+yf*yf) / sqrt(2)
	sh.set_pixel (xi+1, yi, int(red[0] * r), int(red[1] * r), int(red[2] * r))
	r = 1.0 - sqrt ((1.0-xf)*(1.0-xf)+(1.0-yf)*(1.0-yf)) / sqrt(2)
	sh.set_pixel (xi+1, yi+1, int(red[0] * r), int(red[1] * r), int(red[2] * r))

	
	
while 1:
	b = ser.read ()
	if (ord(b) / 10 == 1):
		di = di + 1
	else:
		di = di - 1
		
	if (di >= 64):
		di = 0
	if (di < 0):
		di = 63
		
	sh.clear()
	sh.set_pixel (di/8, di%8, 255,255,255)
#	print (di/8)
#	print (di%8)
#	sleep(1)

#for a in range (0, 20):
#	sh.set_pixel (a, a, red)
#	sleep(1)
#	sh.clear()
#	drawDot (float(a+0.5),float(a+0.5))
#	drawDot (a*0.1 + 3, a*0.15 + 3)
#	sleep(1)
sh.clear()
