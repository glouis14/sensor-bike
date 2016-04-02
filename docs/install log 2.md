###Install log 2 - "Wheezy"

Upon arrival at London in March 2016 for the "[Interaction Residency](http://sonicbikes.net/2016/03/10/interaction-residency-with-sukandar-kartadinata-march/)" we decided to base further development on the existing setup using Raspian 'wheezy' rather than on my board which was running 'jessie'. 

####network
In absence of a router with Ethernet ports we had to get the WiFi dongle working in order to connect the Raspberry Pi to the internet. Two links that helped:

http://www.ghacks.net/2009/04/14/connect-to-a-wireless-network-via-command-line/
https://www.modmypi.com/blog/how-to-set-up-the-ralink-rt5370-wifi-dongle-on-raspian

In /etc/wpa_supplicant/wpa_supplicant.conf add this:
	
	network={
		ssid="<SSID of your wifi network>"
		psk="<the password for this network>"
	}
	
Then stop and restart wlan0:

	sudo wpa_action wlan0 stop
	sudo ifup wlan0
	sudo wpa_cli status

####sensors
The first step was getting the [Sense-Hat](https://www.raspberrypi.org/products/sense-hat/) working. This RPi add-on board has the following sensors:

	Gyroscope
	Accelerometer
	Magnetometer
	Temperature
	Barometric pressure
	Humidity
	
Data from the first three is combined by an on-board micro-controller to provide [pitch, roll, and yaw](https://en.wikipedia.org/wiki/Aircraft_principal_axes), in what is typically called an [IMU](https://en.wikipedia.org/wiki/Inertial_measurement_unit). We are mostly interested in 'roll' to detect when the bicyclist is leaning left or right, as well 'yaw' to get an immediate heading (GPS only provides that after a considerable delay and does not detect a tight circle). Raw accelerometer data could also be helpful to register starts&stops (horizontal) as well as bumps and overall street roughness (vertical). In addition to that the Sense-Hat has an 8x8 RGB-LED matrix and a little joystick that could prove helpful in providing basic diagnostic information when no laptop is available to debug the RPi.

Installing the Sense-Hat libraries:

	sudo apt-get update
	sudo apt-get install sense-hat
	sudo pip-3.2 install pillow

Python "hello world"

	#! /usr/bin/env python
	from sense_hat import SenseHat
	sense = SenseHat()
	sense.show_message("Hello world!")

Full API tp be found [here](http://pythonhosted.org/sense-hat/api/).

Next step was to establish OSC communication towards pd, following this [guide](https://github.com/alx-s/RPi_tutorials/tree/master/OSC_python-pd). Update: pyOSC is now [here](https://pypi.python.org/pypi/pyOSC).

Note that the API has changed, so some of the examples there won't work. E.g. one has to create a message first then attach data to it:

	import OSC
	client = OSC.OSCClient()
	client.connect(('127.0.0.1', 9001))
	m = OSC.OSCMessage("/sh")
	m.append(data)
	client.send(m)

####uart
Additional sensors will be connected to a separate micro-controller (using a Teensy at the moment, but might scale down to something cheaper depending on final requirements). Data from this is piped in thru the RPi's UART port. Instructions how to set this up can e.g. be found [here](https://electrosome.com/uart-raspberry-pi-python/). 

In short, edit /boot/cmdline.txt and remove this:

	‘console=ttyAMA0,115200’ and 
	‘kgdboc=ttyAMA0,115200’

Then in /etc/inittab comment out the line

	‘2:23:respawn:/sbin/getty -L ttyAMA0 115200 vt100’

Reboot, then install minicom

	sudo apt-get install minicom

And test it with

	sudo minicom -b 115200 -o -D /dev/ttyAMA0

In Python:

	import serial
	ser=serial.Serial ("/dev/ttyAMA0")
	ser.baudrate = 115200
	while 1:
		byte = ser.read()
		m = OSC.OSCMessage("/ser")
		m.append(ord(byte))
		client.send(m)

####startup
As mentioned in the first install log, there's a few ways to establish a startup sequence. [Here](http://raspberrywebserver.com/serveradmin/run-a-script-on-start-up.html), some options are listed. In any case following the instructions of the original [sonic-bike-init](https://github.com/sonicbikes/sonic-bike-init/blob/master/README.md) didn't work because systemctl wasn't installed on the 'wheezy-RPi' at hand. Doing so was not recommended by Dave and Tom, as in fact systemctl is somewhat [controversial](http://www.pcworld.com/article/2841873/meet-systemd-the-controversial-project-taking-over-a-linux-distro-near-you.html).

So instead, the startup was implemented thru /etc/init.d where the file actually calling the /sonic-bike-init/start script is /etc/rc.local

####lua
After talking to Dave, we decided to keep the original Lua scripts in place to handle the GPS data and the associated mapping process. Python will run in parallel and take care of the additional sensors. Both send data to pd via OSC. 

To establish OSC in Lua install the library from [koniu](https://github.com/koniu/luaosc). This in turn requires [lpack](http://lua-users.org/wiki/LuaPack) and [LuaSocket](http://www.tecgraf.puc-rio.br/~diego/professional/luasocket/), as well as [luarocks](https://luarocks.org/#quick-start) to install the two.

In src/osc/client.lua two lines need to be disabled:

	--local r = self.socket:receive()
	--if r then return osc.decode(r) end

