import json
from ..entities.weapon import Ranged, Melee
from .combat_system import CombatSystem
from ..entities.player import Player 

class WeaponFactory:
    def __init__(self, combat_system: CombatSystem):
        with open("Madness_Combat/data/weapons.json") as file:
            self.weapon_data = json.load(file)
        self.combat_system = combat_system
    
    def create_weapon(self, weapon_name: str,):
        data = self.weapon_data[weapon_name]
        weapon_type = data["type"]

        weapon = None

        if weapon_type == "ranged":
            weapon = Ranged(data, self.combat_system)
        if weapon_type == "melee":
            weapon = Melee(data, self.combat_system) 
        
        weapon.weapon_id = weapon_name
        return weapon

    def assign_weapon(self, weapon, target):
        target.weapon = weapon
        weapon.owner = target