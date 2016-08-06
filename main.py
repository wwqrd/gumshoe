### Author: Dave Arter @davea
### Description: Where Am I? Show/share your location within EMF
### Category: Other
### License: MIT
### Appname: Where Am I?

import ubinascii as binascii
import wifi
import buttons
import ugfx
import pyb
import os
from imu import IMU
from database import database_set, database_get

utils = __import__("apps/davea~whereami/utils")

ugfx.init()
buttons.init()
ugfx.clear()
imu = IMU()

def set_orientation():
    orientation = ugfx.orientation()
    ival = imu.get_acceleration()
    if ival['y'] < -0.5:
        if orientation != 0:
            ugfx.orientation(0)
    elif ival['y'] > 0.5:
        if orientation != 180:
            ugfx.orientation(180)


def display_location():
    location = database_get('current-location', "Unknown")
    ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
    ugfx.Label(5, 5, ugfx.width(), 20, "Current location:")
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, location)

while True:
    pyb.wfi()
    set_orientation()
    display_location()
    pyb.delay(1000)
