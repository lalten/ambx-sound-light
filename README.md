# ambx-sound-light
Turns the [Philips AmBX Premium Kit](https://en.wikipedia.org/wiki/AmBX) Speakers into a light organ, using
 * Raspberry Pi
 * Philips [AEA2500](http://www.philips.de/c-p/AEA2500_12/bluetooth-hifi-adapter) Bluetooth Audio receiver
 * [CSL](http://www.amazon.de/dp/B00C7LXUDY) USB Audio I/O card

![](https://github.com/panzerkeks/ambx-sound-light/raw/master/doc/setup.png)
## Installation
```
sudo apt-get install python-pyusb python-dev apt-get libportaudio-dev python-pyaudio
```

Copy the *10-ambx.rules* file to */etc/udev/rules.d/10-ambx.rules* (or run the file using sudo)

The Audio warnings can be prevented by commenting out the non-existing devices in *usr/share/alsa/alsa.conf*

## Run
Run the lights.py file
 
