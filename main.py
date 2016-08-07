### Author: Wayward & Joshua
### Description: Find hackers around the site, and bring them to justice!
### Category: Games
### License: MIT
### Appname: Gumshoe

# TODO
#
# - opening screen: 'What is your hacker alias?' -- Can we get this from the device?
# - Default screen to show user and their exp
# - Shake device to search
# - When hacker encountered, two options:
#    - FIGHT! You stand a {poor | fair | good | excellent} chance of winning
#    - RUN! You have a x% chance of losing some exp.
# - "battle screen" to show two exp bars
#    - exp to increase following battle, according to fraction of enemy exp

import ubinascii as binascii
import wifi
import buttons
import ugfx
import pyb
import os
from imu import IMU
from database import database_set, database_get

STRENGTH = ['gloriously bald', 'bearded', 'cute', 'feeble', 'wimpy', 'coy', 'lonely', 'emo', 'uber', 'mutant', 'evil', 'l33t'] # ajectives
BREEDS = ['n00b', 'pokemon player', 'dweeb', 'nerd', 'geek', 'scriptkiddie', 'h4x0r', 'blackhat', 'sysadmin', 'rogue A.I'] # nouns

def roll_dice(sides):
    return round((pyb.rng()/1073741824) * sides)

class Hacker:

    @classmethod
    def xp_range(player_xp):
        return round(player_xp)

    @classmethod
    def discover(player_xp):
       breed = BREEDS[roll_dice(len(BREEDS) - 1)]
       base_xp = player_xp
       xp_range = Hacker.xp_range(player_xp)
       xp = player_xp + roll_dice(xp_range*2) - xp_range
       return Hacker(breed, xp)

    def relative_strength(self, player_xp):
        xp_range = Hacker.xp_range(player_xp)
        xp_relative_value = (self.xp - player_xp + xp_range)/(xp_range*2)
        relative_strength = round(xp_relative_value * len(STRENGTH))
        return STRENGTH[relative_strength]

    def __init__(self, breed, xp):
        self.breed = breed
        self.xp = xp

    def description(player_xp):
        return ("%i %s" % relative_strength(player_xp), breed)

class Gumshoe:
    def __init__(self):
        self.heat_factor = 0
        self.captures = 0
        self.xp = 0
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
            self.tail = Hacker.discover(self.xp)
            tail_description = self.tail.description(self.xp)
            self.xp + self.xp + 5
            return "You found a %s!" % tail_description

        # You find nothing
        self.heat_factor = self.heat_factor + 1
        return "You find nothing."

class Game:

    def __init__(self):
        self.gumshoe = Gumshoe()

    def inactive(self):
        while True:
            ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            ugfx.Label(5, 5, ugfx.width(), 20, "Hello agent,")
            ugfx.Label(5, 20, ugfx.width(), 20, "Captures: %i" % self.gumshoe.captures)
            ugfx.Label(5, 40, ugfx.width(), 20, "XP: %i" % self.gumshoe.xp)
            pyb.delay(1000)

    def search(self):
        ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
        ugfx.Label(5, 5, ugfx.width(), 20, "Scanning for hackers!...")
        ugfx.set_default_font(ugfx.FONT_NAME)
        ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, self.gumshoe.conduct_search())

    def battle(self, hacker):
        # 320 x 240
        #
        # ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
        # ugfx.Label(5, 5, ugfx.width(), 20, "Your oponent attacks!")
        # ugfx.set_default_font(ugfx.FONT_NAME)
        # ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, self.gumshoe.conduct_search())

        return True

    def welcome(self):
        return True

ugfx.init()
buttons.init()
ugfx.clear()
imu = IMU()
game = Game()

game.inactive()

