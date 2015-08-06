# ambx-sound-light
Turns the [Philips AmBX Premium Kit](https://en.wikipedia.org/wiki/AmBX) Speakers into a light organ, using
 * Raspberry Pi
 * Philips [AEA2500](http://www.philips.de/c-p/AEA2500_12/bluetooth-hifi-adapter) Bluetooth Audio receiver
 * [CSL](http://www.amazon.de/dp/B00C7LXUDY) USB Audio I/O card


## Installation
 * sudo apt-get install python-pip python-dev apt-get libportaudio-dev python-pyaudio
 * sudo pip install pyusb pyaudio
 
Copy the 10-ambx.rules to /etc/udev/rules.d/10-ambx.rules

## Run
Run the lights.py file
 
