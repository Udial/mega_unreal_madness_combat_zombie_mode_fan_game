import json
import os
from ..entities.weapon import Ranged


class SaveManager:
    def __init__(self, save_path = "Madness_Combat/saves/savegame.json"):
        self.save_path = save_path

    def has_save(self) -> bool:
        return os.path.exists(self.save_path) and os.path.getsize(self.save_path) > 0
    
    def reset_save(self):
        if self.has_save():
            os.remove(self.save_path)
            return True
        
        return False
    
    def save_game(self, scene):
        os.makedirs(os.path.dirname(self.save_path), exist_ok = True)

        player = scene.player
        weapon = player.weapon
        next_wave_index = scene.wave_manager.current_wave_index

        if scene.wave_manager.is_in_break:
            next_wave_index += 1

        data = {
            "player": {
                "x": player.pos_x,
                "y": player.pos_y,
                "hp": player.hp,
                "armor": player.armor,
                "ammo": player.ammo,
                "amount_of_barricades": player.amount_of_barricades,
                "weapon_id": getattr(weapon, "weapon_id", "bat"),
                "weapon_current_ammo": getattr(weapon, "current_ammo", None)
            },
            "economy": {
                "credits": scene.economy_manager.credits
            },
            "world": {
                "current_room": scene.current_room
            },
            "wave": {
                "next_wave_index": next_wave_index,
                "all_waves_completed": scene.wave_manager.all_waves_completed
            }
        }

        with open(self.save_path, "w") as file:
            json.dump(data, file, indent=4)
    
    def load_game(self, scene):
        if not self.has_save():
            return False
        
        with open(self.save_path, "r") as file:
            data = json.load(file)
        
        player_data = data.get("player", {})
        economy_data = data.get("economy", {})
        world_data = data.get("world", {})
        wave_data = data.get("wave", {})

        player = scene.player

        player.pos_x = player_data.get("x", player.pos_x)
        player.pos_y = player_data.get("y", player.pos_y)
        player.update_rect()

        player.hp = player_data.get("hp", player.hp)
        player.armor = player_data.get("armor", player.armor)
        player.ammo = player_data.get("ammo", player.ammo)
        player.amount_of_barricades = player_data.get(
            "amount_of_barricades",
            player.amount_of_barricades
        )

        scene.economy_manager.credits = economy_data.get(
            "credits",
            scene.economy_manager.credits
        )

        scene.current_room = world_data.get("current_room", scene.current_room)

        weapon_id = player_data.get("weapon_id", "bat")
        weapon = scene.weapon_factory.create_weapon(weapon_id)
        scene.weapon_factory.assign_weapon(weapon, player)

        if isinstance(weapon, Ranged):
            weapon.current_ammo = player_data.get(
                "weapon_current_ammo",
                weapon.current_ammo
            )
            weapon.reloading = False
            weapon.reload_timer = 0

        next_wave_index = wave_data.get("next_wave_index", 0)

        scene.wave_manager.current_wave_index = next_wave_index - 1
        scene.wave_manager.is_in_break = True
        scene.wave_manager.all_waves_completed = wave_data.get(
            "all_waves_completed",
            False
        )

        scene.wave_manager.spawn_queue.clear()
        scene.wave_manager.tab_hold_duration = 0
        scene.wave_manager.spawn_timer = 0

        scene.zombie_list.clear()
        scene.projectile_list.clear()

        scene.camera.update(scene.player)

        return True