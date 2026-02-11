import random

from base import Door, Chest
from characters import Enemy


class LocationFactory:
    """Factory pour créer des instances de Door, Chest, Enemy, etc..."""
    @staticmethod
    def create_door(leads_to=None):
        names = ["une Porte Secrete",
                 "une Porte Mystérieuse",
                 "une Porte cachée",
                 "une Porte Ancienne"]
        name = random.choice(names)
        return Door(name, leads_to)
    
    @staticmethod
    def create_chest(contents=[]):
        return Chest(contents)
    
    @staticmethod
    def create_enemy(name=None):
        enemy_types = [
            {"name": "un Goblin", "health": 30, "attack": 5, "reward": 20},
            {"name": "un Orc", "health": 50, "attack": 10, "reward": 40},
            {"name": "un Troll", "health": 80, "attack": 15, "reward": 60}
        ]
        enemy_info = random.choice(enemy_types)
        name = name if name else enemy_info["name"]
        return Enemy(name,
                     enemy_info["health"],
                     enemy_info["attack"],
                     enemy_info["reward"])
