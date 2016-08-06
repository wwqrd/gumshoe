### Author: Wayward, Joshua, Dave Arter @davea
### Description: Find hackers around the site, and capture them!
### Category: Games
### License: MIT
### Appname: Gumshoe

import ubinascii as binascii
import wifi
import buttons
import ugfx
import pyb
import os
from imu import IMU
from database import database_set, database_get

utils = __import__("apps/theinstitution~gumshoe/utils")
Gumshoe = __import__("apps/theinstitution~gumshoe/gumshoe")

ugfx.init()
buttons.init()
ugfx.clear()
imu = IMU()
gumshoe = Gumshoe()

def set_orientation():
    orientation = ugfx.orientation()
    ival = imu.get_acceleration()
    if ival['y'] < -0.5:
        if orientation != 0:
            ugfx.orientation(0)
    elif ival['y'] > 0.5:
        if orientation != 180:
            ugfx.orientation(180)


def play():
    ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
    ugfx.Label(5, 5, ugfx.width(), 20, "Scanning for hackers!...")
    ugfx.set_default_font(ugfx.FONT_NAME)
    ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, gumshoe.conduct_search())

while True:
    pyb.wfi()
    set_orientation()
    play()
    pyb.delay(15000)
