from abc import ABC, abstractmethod

from ui import PassiveUI

pui = PassiveUI()


class Location(ABC):
    """Classe de base pour les différentes locations (Door, Chest, etc...)"""
    def __init__(self, can_be_explored=True):
        self.can_be_explored = can_be_explored
        self.is_explored = False
    
    @abstractmethod
    def trigger_event(self, hero):
        """Méthode à implémenter pour déclencher l'événement associé à la location"""
        pass

class Wall(Location):
    """Représente un mur infranchissable dans une zone d'exploration"""
    def __init__(self):
        super().__init__(can_be_explored=False)
    
    def trigger_event(self, hero):
        """Le mur ne déclenche aucun événement, il bloque simplement le passage"""
        pui.notify("blocked_move", "")

class Door(Location):
    """Représente une porte dans une zone d'exploration"""
    def __init__(self, name, leads_to=None):
        super().__init__()
        self.name = name
        self.leads_to = leads_to  # Zone vers laquelle la porte mène
    
    def trigger_event(self, hero):
        """Déclenche l'événement de la porte"""
        pui.notify("found_door", self.leads_to)
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
        pui.notify("found_chest", "")
        for item in self.contents:
            hero.inventory.append(item)
            if hasattr(item, "name"):
                pui.notify("found_item", item.name)
        self.is_explored = True