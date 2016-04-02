#! /usr/bin/env python
from sense_hat import SenseHat
from time import sleep
from math import *
import OSC
import time

sh = SenseHat()
sh.set_imu_config (True, True, True)  # gyroscope only

#red = [255.0, 0.0, 0.0]
red = (255, 0, 0)

client = OSC.OSCClient()
client.connect(('127.0.0.1', 9001))


	
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
	orad = sh.get_orientation_radians()
#	print("p: {pitch}, r: {roll}, y: {yaw}".format(**orad))
	p = orad['pitch']
	r = orad['roll']
	y = orad['yaw']
	m = OSC.OSCMessage("/sh")
	m.append(r)
	client.send(m)
#	drawDot(-p*5.0 + 3.5, r*5.0 + 3.5)
#	print (r)
#	sleep(1)

#for a in range (0, 20):
#	sh.set_pixel (a, a, red)
#	sleep(1)
#	sh.clear()
#	drawDot (float(a+0.5),float(a+0.5))
#	drawDot (a*0.1 + 3, a*0.15 + 3)
#	sleep(1)
sh.clear()
