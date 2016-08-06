### Author: Wayward, Joshua, Dave Arter @davea
### Description: Find hackers around the site, and bring them to justice!
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

STRENGTH = ['feeble', 'wimpy', 'coy', 'kind', 'uber', 'evil']

class Hacker:

    # generate a hacker
    @classmethod
    def discover():
        return Hacker('Hacker',
                      randint(0, len(STRENTH) - 1))

    def __init__(name, strength):
        self.name = name
        self.strength = strength

    # hacker's name
    def get_name():
        return self.name

    # hacker strength
    def get_strength():
        return STRENGTH[self.strength]

def roll_dice(sides):
    return round((pyb.rng()/1073741824) * sides)

class Gumshoe:
    def __init__():
        self.heat(0)
        self.captures = 0
        self.load()

    def load():
        heat = database_get('gumshoe_stats_heat')
        if heat:
            self.heat(heat)
        captures = database_get('gumshoe_stats_captures')
        if captures:
            self.captures = captures

    def save():
        database_set('gumshoe_stats_heat', self.heat())
        database_set('gumshoe_stats_captures', self.captures())

    # find a hacker
    def conduct_search():
        dice = roll_dice(20) + self.heat()
        if dice < 15:
            # You find nothing
            self.heat(self.heat() + 1)
            return "You find nothing."

        if dice > 15 and dice < 18:
            # You are close!
            self.heat (5)
            return "You can sense something nearby!"

        if dice > 20:
            # You found a hacker!
            self.heat(-5)
            self.tailing = Hacker.generate()
            return "You found a {self.tailing.get_strength()} {self.tailing.get_name()}!"
            self.save()

    # return sleuth skill
    def skill():
        return self.captures() * 7

    # which hackers has sleuth caught
    def captures():
        return 0

    # multiplier for how likely sleuth will find something
    def heat(heat_factor):
        if heat_factor:
            self.heat_factor = heat_factor
        return self.heat_factor

    def save():

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
