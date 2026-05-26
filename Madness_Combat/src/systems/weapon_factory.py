import json
from ..entities.weapon import Ranged, Melee
from .combat_system import CombatSystem
from ..entities.player import Player 

class WeaponFactory:
    def __init__(self, combat_system: CombatSystem, owner: Player):
        with open("Madness_Combat/data/weapons.json") as file:
            self.weapon_data = json.load(file)
        self.combat_system = combat_system
        self.player = owner
    
    def create_weapon(self, weapon_name: str):
        data = self.weapon_data[weapon_name]
        weapon_type = data["type"]

        if weapon_type == "ranged":
            return Ranged(data, self.player, self.combat_system)
        if weapon_type == "melee":
            return Melee(data, self.player, self.combat_system) 