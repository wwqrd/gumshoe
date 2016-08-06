from random import randint

class Gumshoe:

    hotness_factor = 1

    # find a hacker
    def conduct_search():
        dice = randint(0,20) * hotness()
        if dice < 15:
            # You find nothing

        if dice > 15 and < 18:
            # You are close!
            hotness_factor = 2

        if dice > 20
            hotness_factor = 1
            # You found a hacker!

    # return sleuth skill
    def skill():
        return captures() * 7

    # which hackers has sleuth caught
    def captures():

    # multiplier for how likely sleuth will find something
    def hotness():
        return hothess_factor
