import os

class PyBlasterException(Exception):
    pass

PINMAP = None
live_pins = set()

def get_pin(i):
    if not PINMAP:
        raise PyBlasterException('No pin naming scheme has been chosen. Call piblaster_naming(), bcm_naming(), wiringpi_naming(), or board_naming().')
    try:
        return PINMAP[i]
    except KeyError:
        raise PyBlasterException('Pin %d is not valid -- only GPIO pins with no special purpose are allowed.' % i)

def piblaster_naming():
    global PINMAP
    PINMAP = {n: n for n in range(8)}

def bcm_naming():
    global PINMAP
    PINMAP = {4:0, 17:1, 18:2, 21:3, 27:3, 22:4, 23:5, 24:6, 25:7}

def wiringpi_naming():
    global PINMAP
    PINMAP = {7:0, 0:1, 1:2, 2:3, 3:4, 4:5, 5:6, 6:7}

def board_naming():
    global PINMAP()
    PINMAP = {7:0, 11:1, 12:2, 13:3, 15:4, 16:5, 18:6, 22:7}

def restart():
    if not PINMAP:
        raise PyBlasterException('No pin naming scheme has been chosen. Call piblaster_naming(), bcm_naming(), wiringpi_naming(), or board_naming().')
    os.system('sudo pi-blaster')

def cleanup():
    for pin in live_pins:
        os.system('echo "release %d" > /dev/pi-blaster' % pin)

def enable(i):
    pin = get_pin(i)
    os.system('echo "lock %d" > /dev/pi-blaster' % pin)
    live_pins.add(pin)

def disable(i):
    pin = get_pin(i)
    os.system('echo "release %d" > /dev/pi-blaster' % pin)
    if pin in live_pins:
        live_pins.remove(pin)

def set(i, val):
    pin = get_pin(i)
    if val < 0 or val > 1:
        raise PyBlasterException('Brightness value %f out of range: must be in [0, 1].' % val)
    if pin not in live_pins:
        raise PyBlasterException('Pin %d is not currently active.' % i)
    os.system('echo "%d=%f" > /dev/pi-blaster' % (pin, val))
