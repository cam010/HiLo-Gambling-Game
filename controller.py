import random

LOW = 'low'
HIGH = 'high'
SAME = 'same'


class Bank:
    all_time_earnings = 0

    def __init__(self, starting_money): 
        self.money = starting_money

    def win(self, win_amount):
        self.money += win_amount
        self.money = round(self.money, 2)

    def bet(self, bet=10):
        self.money -= bet
        self.money = round(self.money, 2)


def generate_number() -> int:
    return random.randint(1, 12)


def generate_chances(num):
    higher = 12 - num
    lower = num - 1
    same = 1
    return (higher, lower, same)


def evaluate_win(num1, num2, guess):
    if num1 == num2 and guess == 'same':
        win = True
    elif num1 < num2 and guess == 'high':
        win = True
    elif num1 > num2 and guess == 'low':
        win = True
    else:
        win = False
    return win


def generate_odds(chances):
    # chances = (high, low, same)
    higher = (12 - chances[0])/chances[0] if chances[0] != 0 else 0
    lower = (12 - chances[1])/chances[1] if chances[1] != 0 else 0
    return [[f"{(12 - chances[0])}/{chances[0]}", higher], [f"{(12 - chances[1])}/{chances[1]}", lower], ["11/1", 11/1]]


def generate_win_amount(odds: list[float, float, float], bet_amount: int, guess: str):
    # odds -> [high, low, same]
    if guess == 'high':
        win_amount = (odds[0] + 1) * bet_amount
    elif guess == 'low':
        win_amount = (odds[1] + 1) * bet_amount
    elif guess == 'same':
        win_amount = (odds[2] + 1) * bet_amount
    return round(win_amount, 2)
