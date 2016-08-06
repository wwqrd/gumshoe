from random import randint

class Gumshoe:

    hotness_factor = 1

    # find a hacker
    def conduct_search():
        dice = randint(0,20) * hotness()
        if dice < 15:
            # You find nothing
            return "You find nothing"

        if dice > 15 and dice < 18:
            # You are close!
            hotness_factor = 2

        if dice > 20:
            hotness_factor = 1
            # You found a hacker!

    # return sleuth skill
    def skill():
        return captures() * 7

    # which hackers has sleuth caught
    def captures():
        return 0

    # multiplier for how likely sleuth will find something
    def hotness():
        return hotness_factor
