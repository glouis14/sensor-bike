###SENSOR BIKE

The Sensor-Bike is an extension of the Sonic-Bike by [Kaffe Matthews / BRI](http://sonicbikes.net) with additional sensors beyond the existing GPS-system.

It inherits code from Wolfgang Hauptfleisch, Dave Griffiths, Tom Keene & Jairo Sanchez.<br>
The Lua code in particular has been largely untouched so far and continues to handle the GPS-processing. Instead of triggering sound files directly it now forwards zone information via OSC to pd as implemented by Dave.<br>
The initial pd patches are derived from Dave's [sonic-kayaks](https://github.com/nebogeo/sonic-kayaks)(-[puredata](https://github.com/nebogeo/sonic-kayaks-puredata)). <br>
The Python code is new and handles sensor data received from the Sense-Hat as well as the extra micro-controller that handles sensors outside the main Raspberry Pi box.



License
------------------
Sonic-Bike embedded system for Kaffe Matthews <br>
Copyright (C) 2016 Sukandar Kartadinata <br>
Based on code by Wolfgang Hauptfleisch, Dave Griffiths, Tom Keene & Jairo Sanchez<br>

This program is free software: you can redistribute it and/or modify<br>
it under the terms of the GNU General Public License as published by<br>
the Free Software Foundation, either version 3 of the License, or<br>
(at your option) any later version.<br>

This program is distributed in the hope that it will be useful,<br>
but WITHOUT ANY WARRANTY; without even the implied warranty of<br>
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the<br>
GNU General Public License for more details.<br>

You should have received a copy of the GNU General Public License<br>
along with this program.  If not, see <http://www.gnu.org/licenses/>.
