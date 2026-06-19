import pygame


class EconomyManager:
    def __init__(self):
        self.credits = 0
        self.prices = {"barricade": 30, "ammo": 5, "medkit": 100}

    def add_money(self, amount: int):
        self.credits += amount

    def subtruct_money(self, amount: int):
        self.credits -= amount

    def can_afford(self, price: int) -> bool:
        if self.credits >= price:
            return True
        else:
            return False

    def spend_money(self, price: int) -> bool:
        if not self.can_afford(price):
            return False

        self.subtruct_money(price)
        return True
