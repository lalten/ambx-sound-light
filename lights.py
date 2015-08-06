#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ambx.ambx import AMBX, Lights
import pyaudio # from http://people.csail.mit.edu/hubert/pyaudio/
import numpy   # from http://numpy.scipy.org/
import struct

lights = [Lights.LEFT, Lights.RIGHT, Lights.WWLEFT, Lights.WWCENTER, Lights.WWRIGHT]
decay = 0.5


'''
http://julip.co/2012/05/arduino-python-soundlight-spectrum/
'''


def list_devices(p):
    # List all audio input devices
#    p = pyaudio.PyAudio()
    i = 0
    devNr = 0
    n = p.get_device_count()
    while i < n:
        dev = p.get_device_info_by_index(i)
        if dev['maxInputChannels'] > 0:
            print str(i)+'. '+dev['name']
            devNr = i
        i += 1
    return devNr

def arduino_soundlight(p,device=0):

	#    p = pyaudio.PyAudio()
	print "choosing device: "+str(device)+': '+pyaudio.PyAudio().get_device_info_by_index(device)['name']

	chunk      = 2**12 # Change if too fast/slow, never less than 2**11
	scale      = 10    # Change if too dim/bright
	exponent   = 1     # Change if too little/too much difference between loud and quiet sounds
	#samplerate = 44100
	samplerate = int(p.get_device_info_by_index(device)['defaultSampleRate'])
	print "samplerate: %d"%samplerate
	# CHANGE THIS TO CORRECT INPUT DEVICE
	# Enable stereo mixing in your sound card
	# to make you sound output an input
	# Use list_devices() to list all your input devices
	#device   = 14 #'dmix'

	stream = p.open(format = pyaudio.paInt16,
					channels = 1,
					rate = samplerate,
					input = True,
					frames_per_buffer = chunk,
					input_device_index = device)

	#print "Starting, use Ctrl+C to stop"
	dev = None
	try:
		dev = AMBX(0)

		for light in lights:
			try:
				dev.set_color_rgb8(light, [255, 255, 255])
			except IOError:
				print 'USB Error'
				break
		
		bass_temp = 0
		mid_temp = 0
		treble_temp = 0

		while True:
			try:
				data  = stream.read(chunk)
			except IOError:
				print 'Overflow'

			# Do FFT
			[bass, mid, treble] = calculate_levels(data, chunk, samplerate)

			# nice levels
			bass    = max(min(int(max(min(bass  / scale, 1.0), 0.0)**exponent*250 + decay*bass_temp     ),255),0)
			mid     = max(min(int(max(min(mid   / scale, 1.0), 0.0)**exponent*250 + decay*mid_temp      ),255),0)
			treble  = max(min(int(max(min(treble/ scale, 1.0), 0.0)**exponent*250 + decay*treble_temp   ),255),0)
			bass_temp = bass
			mid_temp = mid
			treble_temp = treble

			#print bass, mid, treble

			for light in lights:
				try:
					dev.set_color_rgb8(light, [bass, mid, treble])
				except IOError:
					print 'USB Error'

	except IndexError:
		if dev is None:
			print 'No AmbX found!'
			
	except KeyboardInterrupt:
		pass
	finally:
		print "…Stop"
		stream.close()
		p.terminate()
	if dev is not None:
		for light in lights:
			dev.set_color_rgb8(light, [0, 0, 0])



def calculate_levels(data, chunk, samplerate):
    # Use FFT to calculate volume for each frequency
    global MAX

    # Convert raw sound data to Numpy array
    fmt = "%dH"%(len(data)/2)
    data2 = struct.unpack(fmt, data)
    data2 = numpy.array(data2, dtype='h')

    # Apply FFT
    fourier = numpy.fft.fft(data2)
    ffty = numpy.abs(fourier[0:len(fourier)/2])/1000
    ffty1=ffty[:len(ffty)/2]        # erste hälfte
    ffty2=ffty[len(ffty)/2::]+2     # zweite hälfte +2
    ffty2=ffty2[::-1]               # umdrehen
    ffty=ffty1+ffty2                # addieren
    ffty=numpy.log(ffty)-2

    fourier = list(ffty)[4:-4]
    fourier = fourier[:len(fourier)/2]

    size = len(fourier)

    # Add up for NUM_LIGHTS lights
#     NUM_LIGHTS = 5
#     levels = [   sum(fourier[i:(i+size/NUM_LIGHTS)]) for i in xrange(0, size, size/NUM_LIGHTS)  ][:NUM_LIGHTS]
    bass = sum(fourier[:5])/(5-0)
    mid = sum(fourier[6:70])/(70-6)
    treble = sum(fourier[71:])/(size-71)

    return [bass, mid, treble]

if __name__ == '__main__':
    p = pyaudio.PyAudio()
    devNr = list_devices(p)
    arduino_soundlight(p,devNr)
