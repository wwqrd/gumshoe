### Author: Wayward & Joshua
### Description: Find hackers around the site, and bring them to justice!
### Category: Games
### License: MIT
### Appname: Gumshoe

# TODO
#
# - opening screen: 'What is your hacker alias?' -- Can we get this from the device?
# - Default show user and their exp
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
            self.heat_factor = 10

        if dice >= 20:
            self.heat_factor = -3

        if dice < 15:
            self.heat_factor = self.heat_factor + 1

        return dice

class Battle:

    @classmethod
    def find_battle(self, player_xp, dice_roll):
        return Battle(player_xp, dice_roll)

    def __init__(self, player_xp, dice_roll):
        self.player_xp = player_xp
        self.dice_roll = dice_roll
        self.target = False
        self.battling = False
        self.get_target()

    def status(self):
        if self.dice_roll < 15:
            return "You find nothing."

        if self.dice_roll >= 15 and self.dice_roll <= 19:
            return "You can sense something nearby!"

        if self.dice_roll >= 20:
            return "You found %s!" % self.target.description()

    def get_target(self):
        if not self.target and self.is_found():
            self.target = Hacker.discover(self.player_xp)
        return self.target

    def is_found(self):
        if self.dice_roll <= 19:
            return False
        else:
            return True

    # Do you want to do battle?
    def choose_action():
        return True

    # Do battle!
    def battle():
        return True

class Game:

    def __init__(self):
        global game_state
        self.gumshoe = Gumshoe()
        game_state = 'INACTIVE'

    def render(self):
        global game_state
        print('render '+game_state)
        ugfx.clear()
        if game_state == 'SEARCH':
            ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            ugfx.Label(5, 5, ugfx.width(), 20, "Scanning for hackers!...")
            ugfx.set_default_font(ugfx.FONT_NAME)
            ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, self.current_battle.status())
        # elif game_state == 'BATTLE':
            # ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            # ugfx.Label(5, 5, ugfx.width(), 20, "Battle mode")
            # 320 x 240
            #
            # ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            # ugfx.Label(5, 5, ugfx.width(), 20, "Your oponent attacks!")
            # ugfx.set_default_font(ugfx.FONT_NAME)
            # ugfx.Label(5, 30, ugfx.width(), ugfx.height()-30, self.gumshoe.conduct_search())
        elif game_state == 'INACTIVE':
            ugfx.set_default_font(ugfx.FONT_MEDIUM_BOLD)
            ugfx.Label(5, 5, ugfx.width(), 25, "Hello agent,")
            ugfx.Label(5, 25, ugfx.width(), 25, "Captures: %i" % self.gumshoe.captures)
            ugfx.Label(5, 50, ugfx.width(), 25, "XP: %i" % self.gumshoe.xp)
            ugfx.Label(5, 75, ugfx.width(), 25, "Instructions:")
            ugfx.Label(5, 100, ugfx.width(), 25, "(1) Explore the EMF site")
            ugfx.Label(5, 125, ugfx.width(), 50, "(2) When in position, press A to start a search for nearby hackers...")
            ugfx.Label(5, 175, ugfx.width(), 50, "Beware of confronting more experienced hackers!")

    def inactive(self):
        global game_state
        game_state = 'INACTIVE'

    def search(self):
        global game_state
        print('search method')
        dice_roll = self.gumshoe.conduct_search()
        self.current_battle = Battle.find_battle(self.gumshoe.xp, dice_roll)
        game_state = 'SEARCH'

    def battle(self):
        game_state = 'BATTLE'

ugfx.init()
buttons.init()
ugfx.clear()
imu = IMU()
game_state = 'INACTIVE'
last_render_state = False
game = Game()

game.inactive()

def render():
    global game, last_render_state, game_state
    if(last_render_state != game_state):
        game.render()
        last_render_state = game_state

while True:
    print(game_state)
    render()
    if(game_state == 'INACTIVE' and buttons.is_pressed("BTN_A")):
        game.search()
        render()
    if(game_state == 'SEARCH' and not game.current_battle.is_found()):
        pyb.delay(3000)
        game.inactive()
        render()

    pyb.delay(50)
