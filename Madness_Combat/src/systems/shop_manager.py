import pygame
from .economy_manager import EconomyManager
from .input_system import InputState
from ..entities.player import Player


class ShopManager:
    def __init__(self, economy_manager: EconomyManager, player: Player):
        self.economy_manager = economy_manager
        self.player = player

    def buy(self, input_state: InputState):
        if input_state.buying_barricade == True:
            if self.economy_manager.spend_money(self.economy_manager.prices["barricade"]):
                self.player.amount_of_barricades += 1
                print(f"DEBUG Player bought a barricade. Now player has {self.player.amount_of_barricades} barricades")
            else:
                print("DEBUG Player can't afford a barricade")