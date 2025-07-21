from random import randint

class Dice:
    def __init__(self):
        self._results = 0

    def roll_dice(self):
        self._result = randint(1, 6)
