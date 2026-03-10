import random
from abc import ABC, abstractmethod

from ui import PassiveUI
import questionary
import random
from objects import Key
from ui import PassiveUI

pui = PassiveUI()


class Location(ABC):
    """Classe de base pour les différentes locations (Portal, Chest, etc.)"""
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
        self.tile_type = "wall"

    def trigger_event(self, hero):
        """Le mur ne déclenche aucun événement, il bloque simplement le passage"""
        self.is_explored = True

class Exit(Location):
    """Représente la sortie de la zone d'exploration"""
    def __init__(self, exploration=None):
        super().__init__(can_be_explored=True)
        self.exploration = exploration
        self.tile_type = "door"

    def trigger_event(self, hero):
        """Déclenche l'événement de la sortie"""
        self.is_explored = True
        pui.notify("found_exit", "")
        self.exploration.next_level(1)

class Portal(Location):
    """Représente un portail vers une prochaine zone ou un autre portail"""
    def __init__(self, name, exploration):
        super().__init__()
        self.name = name
        self.exploration = exploration
        self.tile_type = "portal"
        self.is_locked = True # Par défaut, le portail est verrouillé et nécessite une clé pour être utilisé

    def trigger_event(self, hero):
        """Déclenche l'événement de la porte"""
        self.is_explored = True
        if self.exploration:
            next_level = random.randint(1, 3) # Simuler la génération d'un prochain niveau
            next_level_str = f"Level {self.exploration.level + next_level}"
            pui.notify("found_portal", next_level_str)
            if self.is_locked and hero.inventory and any(isinstance(item, Key) and item.opens == self for item in hero.inventory):
                # Select to use or not the portal
                use_portal = questionary.confirm( f"Veux-tu utiliser le portail pour aller vers {next_level_str} ?" ).ask()
                if use_portal:
                    self.exploration.next_level(next_level)
                    return self.exploration
            else:
                pui.notify("portal_locked", "")
        else:
            pui.notify("found_portal", "nulle part")
        return self.exploration



class Chest(Location):
    """Représente un coffre dans une zone d'exploration"""
    def __init__(self, contents=None):
        super().__init__()
        if contents is None:
            contents = []
        self.contents = contents  # Contenu du coffre (ex : arme, potion)
        self.tile_type = "chest"

    def trigger_event(self, hero):
        """Déclenche l'événement du coffre"""
        pui.notify("found_chest", "")
        for item in self.contents:
            hero.inventory.append(item)
            if hasattr(item, "name"):
                pui.notify("found_item", item)
        self.is_explored = True