from base import Door, Chest, Location
from characters import Enemy, Hero
from objects import Key

class PathEvent:
    """Classe représentant un événement dans une case de la matrice d'exploration"""
    def __init__(self, location:Location):
        self.location = location

    def trigger_event(self, hero:Hero):
        """Déclenche l'événement associé à la location"""
        if isinstance(self.location, Door):
            print(f"\n🚪 You found a door leading to {self.location.leads_to}!")
            return self.location.leads_to
        
        elif isinstance(self.location, Chest):
            print("\n🧰 You found a chest!")
            for item in self.location.contents:
                hero.inventory.append(item)
                if isinstance(item, Key):
                    print(f"\n🔑 You found a {item.name}! (Opens: {item.opens})")
        
        elif isinstance(self.location, Enemy):
            enemy = self.location
            print(f"\n👹 You encountered an enemy: {enemy.name} (HP: {enemy.health}, DMG: {enemy.attack})!")
            print(f"\n🎉 You defeated the {enemy.name} and gained {enemy.dropped_exp} EXP!")
            hero.exp += enemy.dropped_exp
        
        return None