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
