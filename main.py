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

STRENGTH = ['feeble', 'wimpy', 'coy', 'lonely', 'uber', 'evil', 'l33t']
BREEDS = ['dweeb', 'nerd', 'scriptkid', 'haxor', 'blackhat', 'whitehat', 'consumate professional']

def roll_dice(sides):
    return round((pyb.rng()/1073741824) * sides)

class Hacker:
    def __init__(self, name, strength):
        self.name = name
        self.strength = strength

    # hacker's name
    def get_name(self):
        return BREEDS[self.name]

    # hacker strength
    def get_strength(self):
        return STRENGTH[self.strength]

class Gumshoe:
    def __init__(self):
        self.heat_factor = 0
        self.captures = 0
        self.load()

    def load(self):
        heat = database_get('gumshoe_stats_heat')
        if heat:
            self.heat_factor = heat
        captures = database_get('gumshoe_stats_captures')
        if captures:
            self.captures = captures

    def save(self):
        database_set('gumshoe_stats_heat', self.heat_factor)
        database_set('gumshoe_stats_captures', self.captures())

    # find a hacker
    def conduct_search(self):
        dice = roll_dice(20) + self.heat_factor
        print('dice roll: %i' % dice)

        if dice >= 15 and dice <= 19:
            # You are close!
            self.heat_factor = 10
            return "You can sense something nearby!"

        if dice >= 20:
            # You found a hacker!
            self.heat_factor = -3
            self.tail = Hacker(roll_dice(len(BREEDS) - 1), roll_dice(len(STRENGTH) - 1))
            return "You found a " + self.tail.get_strength() + " " + self.tail.get_name() + "!"

        # You find nothing
        self.heat_factor = self.heat_factor + 1
        return "You find nothing."

    # return sleuth skill
    def skill(self):
        return self.captures() * 7

    # which hackers has sleuth caught
    def captures():
        return 0

    def save():
        return 1

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
    pyb.delay(1000)
