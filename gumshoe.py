from random import randint
Hacker = __import__("apps/theinstitution~gumshoe/hacker")

class Gumshoe:

    def __init__():
        self.heat(0)
        self.captures = 0

    # find a hacker
    def conduct_search():
        dice = randint(0,20) + self.heat()
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
