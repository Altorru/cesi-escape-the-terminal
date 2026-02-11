from abc import ABC, abstractmethod

from ui import PassiveUI

ui = PassiveUI()


class Location(ABC):
    """Classe de base pour les différentes locations (Door, Chest, etc...)"""
    def __init__(self, can_be_explored=True):
        self.can_be_explored = can_be_explored
        self.is_explored = False
    
    @abstractmethod
    def trigger_event(self, hero):
        """Méthode à implémenter pour déclencher l'événement associé à la location"""
        pass

class Door(Location):
    """Représente une porte dans une zone d'exploration"""
    def __init__(self, name, leads_to=None):
        super().__init__()
        self.name = name
        self.leads_to = leads_to  # Zone vers laquelle la porte mène
    
    def trigger_event(self, hero):
        """Déclenche l'événement de la porte"""
        ui.notify("found_door", self.leads_to)
        self.is_explored = True
        return self.leads_to

class Chest(Location):
    """Représente un coffre dans une zone d'exploration"""
    def __init__(self, contents=None):
        super().__init__()
        if contents is None:
            contents = []
        self.contents = contents  # Contenu du coffre (ex: arme, potion)
    
    def trigger_event(self, hero):
        """Déclenche l'événement du coffre"""
        ui.notify("found_chest", "")
        for item in self.contents:
            hero.inventory.append(item)
            if hasattr(item, "name"):
                ui.notify("found_item", item.name)
        self.is_explored = True