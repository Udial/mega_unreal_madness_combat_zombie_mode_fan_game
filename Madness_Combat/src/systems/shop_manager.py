import json
from .economy_manager import EconomyManager
from ..systems.weapon_factory import WeaponFactory
from ..entities.player import Player


class ShopManager:
    def __init__(
        self,
        economy_manager: EconomyManager,
        player: Player,
        weapon_factory: WeaponFactory
    ):
        self.economy_manager = economy_manager
        self.player = player
        self.weapon_factory = weapon_factory

        with open("Madness_Combat/data/shop_items.json") as file:
            self.shop_items = json.load(file)

        self.last_message = ""

    def get_items_by_category(self, category: str) -> list:
        return self.shop_items.get(category, [])
    
    def buy_item(self, category: str, item: dict) -> bool:
        price = item["price"]
        if not self.economy_manager.spend_money(price):
            self.last_message = "Not enough credits"
            print(f"DEBUG SHOP: can't afford {item['name']}")
            return False
        if category == "weapons":
            self.buy_weapon(item)
        elif category == "ammo":
            self.buy_ammo(item)
        elif category == "consumables":
            self.buy_consumable(item)
        elif category == "armor":
            self.buy_armor(item)
        
        self.last_message = f"Bought {item['name']}"
        print(f"DEBUG SHOP: bought {item['name']}")
        return True
    
    def buy_weapon(self, item: dict):
        weapon_id = item["weapon_id"]
        weapon = self.weapon_factory.create_weapon(weapon_id)
        self.weapon_factory.assign_weapon(weapon, self.player)
    
    def buy_ammo(self, item: dict):
        self.player.ammo += item["amount"]
    
    def buy_consumable(self, item: dict):
        if "heal" in item and (self.player.hp < self.player.max_hp):
            self.player.hp = int(min(self.player.max_hp, self.player.hp + item["heal"]))
        
    def buy_armor(self, item: dict):
        if "charge" in item and (self.player.armor < self.player.max_armor):
            self.player.armor = int(min(self.player.max_armor, self.player.armor + item["charge"]))