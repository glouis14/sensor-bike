###Install log 1 - "Jessie"

These are some notes regarding my first installation attempts on a Raspberry Pi 2 for the Sonic Bike Project.
I started off with a fresh download of Noobs v1.8 which resulted in a Raspian 'jessie' install. Later when working with Kaffe in London I learned that all the existing systems were using the previous 'wheezy' version, so I then continued to work with that which is covered in Install log 2.

####audio
Out of the box, there was no audio signal coming from the mini-jack output.
DuckDuckGo pointed me [here](https://www.raspberrypi.org/documentation/configuration/audio-config.md).
So actually audio was working, but by default it's using the HDMI audio channel.
To set the headphone jack as output:
	
	amixer cset numid=3 2

This works across a reboot.

####pd

	sudo apt-get install puredata
	
I noticed that pd generates noise as soon as the DSP is enabled, even if no patch is loaded. I guess that's what Dave hinted at when he suggested to set disable_audio_dither=1 in /boot/config.txt (see [sonicbikes/sonic-bike-init/Readme.md](https://github.com/sonicbikes/sonic-bike-init/blob/master/README.md) section B)

####network
Initially I wanted to set up a static IP and make a 1:1 Ethernet connection to my laptop (later at Kaffe's we switched back to DHCP). It should be noted here that 'jessie' handles things differently than 'wheezy'. Most online tutorials tell you to edit /etc/network/interfaces, however 'jessie' requires you to edit /etc/dhcpcd.conf as I found out down in the comments of this [page](http://www.suntimebox.com/raspberry-pi-tutorial-course/week-3/day-5/). Here's what I added at the end of the file

	interface eth0
	static ip_address=192.168.1.250
	static routers=192.168.1.254
	static domain_name_servers=192.168.1.254

####display
Probably redundant information for long-time Linux users, but being used to a Mac I found it puzzling that I couldn't change the display resolution in the GUI display settings. Menu => Preferences => Display Settings only lists 1184x624, even though my monitor supports 1080p

Here's two links on how to deal with this.

http://weblogs.asp.net/bleroy/getting-your-raspberry-pi-to-output-the-right-resolution
https://www.raspberrypi.org/forums/viewtopic.php?f=26&t=5851

	/opt/vc/bin/tvservice -m CEA
	
This lists 16 modes, here are the two relevant ones.

	(prefer) mode 4: 1280x720 60Hz 16:9 progressive 
	mode 16: 1920x1080 60Hz 16:9 progressive

Also querying DMT modes:

	/opt/vc/bin/tvservice -m DMT
	
Only 3 modes with 1024x768 max, so we gonna use CEA with these changes in /boot/config.txt

	hdmi_group = 1 (CEA)
	hdmi_mode = 16

####headless operation
In getting RPi work in headless mode I basically followed Frederik Olofsson's [guide](http://www.fredrikolofsson.com/f0blog/?q=node/630)

Testing audio output remotely:

	ssh pi@192.168.1.80
	sudo speaker-test -t sine -c 2

(this works w/o specifying a device like suggested by F.O.)

2nd terminal to copy test patch to RPi
	
	cd /Users/glui/Proj/Sonic\ Bikes\ \(Kaffe\ Matthews\)/pd
	scp testsines.pd pi@192.168.1.80:/home/pi/Desktop/SonicBikes

back on 1st terminal, start pd

	cd Desktop/SonicBikes/
	pd -stderr -nogui -verbose -audiodev 4 testsines.pd

F.O. uses crontab to configure the startup behaviour - later I learned about other methods (see log 2)

Create new script file autostart.sh with these lines

	#!/bin/bash
	pd -nogui -audiodev 4 /home/pi/Desktop/SonicBikes/testsines.pd

Make it executable

	$ chmod +x autostart.sh

Then edit/create crontab
	
	$ sudo crontab -e
	
And add at end

	@reboot /bin/bash /home/pi/autostart.sh
	
Then reboot.

To stop:

	$ ssh pi@raspberrypi.local
	$ sudo pkill pd
	$ sudo halt



####ftp
https://www.raspberrypi.org/documentation/remote-access/ssh/sftp.md

=> use SFTP when connecting to the RPi
