import random

from base import Portal, Chest
from objects import Key, Potion
from characters import Enemy


class LocationFactory:
    """Factory pour créer des instances de Portal, Chest, Enemy, etc..."""

    @staticmethod
    def create_portal(exploration):
        names = [
            "un Portail Secret",
            "un Portail Mystérieux",
            "un Portail caché",
            "un Portail Ancien",
        ]
        name = random.choice(names)
        return Portal(name, exploration)

    @staticmethod
    def create_chest(contents=None):
        if contents is None:
            contents = []
        return Chest(contents)

    @staticmethod
    def create_enemy(name=None):
        enemy_types = [
            {"name": "un Goblin", "health": 30, "attack": 5, "reward": 20},
            {"name": "un Orc", "health": 50, "attack": 10, "reward": 40},
            {"name": "un Troll", "health": 80, "attack": 15, "reward": 60},
        ]
        enemy_info = random.choice(enemy_types)
        name = name if name else enemy_info["name"]
        return Enemy(
            name, enemy_info["health"], enemy_info["attack"], enemy_info["reward"]
        )


class ObjectFactory:
    """Factory pour créer des instances d'objets (Weapon, Potion, Key, etc...)"""

    @staticmethod
    def create_key(opens):
        names = ["une Clé en Fer", "une Clé en Or", "une Clé en Argent"]
        name = random.choice(names)
        return Key(name, opens)

    @staticmethod
    def create_potion():
        names_values = [
            ("une Potion de Soin Mineure", 20),
            ("une Potion de Soin Majeure", 50),
            ("une Potion de Soin Ultime", 100),
        ]
        weights = [
            0.5,
            0.3,
            0.2,
        ]  # Pondération pour favoriser les potions de soin mineures
        name, heal_amount = random.choices(names_values, weights=weights, k=1)[0]
        return Potion(name, heal_amount)
