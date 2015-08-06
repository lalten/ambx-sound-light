# -*- coding: utf-8 -*-
'''
Python interface to Philips AMBX hardware.
Based on combusd (http://code.google.com/p/combustd/) by Martijn de Boer / Gert-Jan de Boer.
'''
import usb
import logging

# from support.ByteArray import B,Bhex
# from support.usbutil import devices_by_vendor_product

logger = logging.getLogger("AMBX")

# Usb identification
VENDOR  = 0x0471
PRODUCT = 0x083f

# Endpoints
EP_IN = 0x81
EP_OUT = 0x02
EP_PNP = 0x83

# Packet start
PKT_HEADER = 0xA1

# -- Commands --


# Set a single color, for a specific light
# Params 0xRR 0xGG 0xBB
# 0xRR = Red color
# 0xGG = Green color
# 0xBB = Blue color
SET_LIGHT_COLOR = 0x03

# Set a color sequence using delays
# Params 0xMM 0xMM then a repeated sequence of 0xRR 0xGG 0xBB
# 0xMM = milliseconds
# 0xMM = milliseconds
# 0xRR = Red color
# 0xGG = Green color
# 0xBB = Blue color
SET_TIMED_COLOR_SEQUENCE = 0x72

# -- Lights --
# Definitions so we do not need to remember the hex values for the lights
class Lights:
    # LEFT/RIGHT lights. Normally placed adjecent to your screen.
    LEFT = 0x0B
    RIGHT = 0x1B
  
    # Wallwasher lights. Normally placed behind your screen.
    WWLEFT = 0x2B
    WWCENTER = 0x3B
    WWRIGHT = 0x4B
                              
# Timeouts
TIMEOUT_LIBUSBC = 2500
TIMEOUT_LIBUSBR = 2500
TIMEOUT_LIBUSBW = 2500

def float_to_rgb8(color):
    return [min(max(int(x*256.0),0),255) for x in color]

class AMBX(object):
    def __init__(self, dev=0, usbdev=None):
        self._log = logging.getLogger("AMBX.%i" % dev)
        if usbdev is None:
            devs = devices_by_vendor_product(VENDOR, PRODUCT)
            self._devptr = devs[dev]
        else:
            self._devptr = usbdev
        self.num = dev
        self._init_hw()
        
    def _init_hw(self):
        self._log.debug("Opening device")
        self._dev = self._devptr.open()
        self._log.debug("Claiming interface 0")
        self._dev.claimInterface(0)
        self._log.debug("Initialisation succesful")

    def write(self, data, timeout=TIMEOUT_LIBUSBW):
        '''Write command data to device'''
        return self._dev.interruptWrite(EP_OUT, data, timeout)

    def set_color_rgb8(self, light, color):
        '''Set light color'''
        self.write(B([PKT_HEADER, light, SET_LIGHT_COLOR, color[0], color[1], color[2]]))
        
    def set_color_float(self, light, color):
        self.set_color_rgb8(light, float_to_rgb8(color))

    def set_sequence_rgb8(self, light, millis, colors):
        '''Set light color sequence'''
        assert(millis >= 0 and millis <= 0xffff)
        assert(len(colors) == 16) # must be 16 colors
        pkt = [PKT_HEADER, light, SET_TIMED_COLOR_SEQUENCE, millis >> 8, millis & 255]
        for color in colors:
            assert(len(color) == 3)
            pkt.extend(color)
        self.write(B(pkt))
        
    def set_sequence_float(self, light, millis, colors):
        self.set_sequence_rgb8(light, millis, [float_to_rgb8(color) for color in colors])









# Part of "terra", (C) W.J. van der Laan 2009
"""Simple byte array handling (pre python 3.0)"""
from array import array

def B(x):
    return array("B",x)

def Bhex(d):
    return " ".join(["%02x" % x for x in d])

def hex_dump(d, width=16):
    addr = 0
    s = ""
    while addr < len(d):
        s += "%04x: " % addr
        s += " ".join(["%02x" % x for x in d[addr:addr+width]])
        addr += width
        s += "\n"
    return s

def pad(d, size, value=0):
    if len(d) < size:
        return d + B([value]*(size-len(d)))
    else:
        return d










'''
libusb Python utilities
W.J van der Laan 2010
'''
import usb
#import logging

logger = logging.getLogger("support.usbutil")

def device_by_num(busnum, devnum):
    '''
    Look up libusb device handle by busnum and devnum.
    Raise LookupError if none found.

    >>> device_by_num('001','001')
    <usb.Device object at 0x91dfea8>
    '''
    for bus in usb.busses():
        if bus.dirname == busnum:
            for device in bus.devices:
                if device.filename == devnum:
                    return device
    raise LookupError("No such device %s/%s" % (busnum, devnum))

def devices_by_vendor_product(vendor, product):
    '''
    Enumerate all USB devices with the right vendor
    and product ID
    '''
    devs = []
    logger.debug("Enumerating devices")
    for bus in usb.busses():
        for device in bus.devices:
            if device.idVendor==vendor and device.idProduct==product:
                logger.debug("Found device %i on %s:%s", len(devs), bus.dirname, device.filename)
                devs.append(device)
    return devs




















