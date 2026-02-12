from base import Portal, Chest, Wall, Location, Exit
from characters import Enemy, Hero
from objects import Key
from ui import PassiveUI

pui = PassiveUI()

class PathEvent:
    """Classe représentant un événement dans une case de la matrice d'exploration"""
    def __init__(self, location:Location):
        self.location = location

    def trigger_event(self, hero:Hero):
        """Déclenche l'événement associé à la location"""
        if isinstance(self.location, Portal):
            self.location.trigger_event(hero)
        
        elif isinstance(self.location, Chest):
            pui.notify("found_chest", "")
            for item in self.location.contents:
                hero.inventory.append(item)
                if isinstance(item, Key):
                    pui.notify("found_item", item)
        elif isinstance(self.location, Enemy):
            enemy = self.location
            pui.notify("enemy_encounter", enemy)
            pui.notify("enemy_defeated", enemy)
            hero.exp += enemy.dropped_exp
        
        elif isinstance(self.location, Wall):
            self.location.trigger_event(hero)
        
        elif isinstance(self.location, Exit):
            self.location.trigger_event(hero)
        
        return None