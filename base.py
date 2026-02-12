from abc import ABC, abstractmethod
from ui import PassiveUI
import questionary
import random

pui = PassiveUI()


class Location(ABC):
    """Classe de base pour les différentes locations (Portal, Chest, etc...)"""
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
        pui.notify("hit_wall", "")

class Exit(Location):
    """Représente la sortie de la zone d'exploration"""
    def __init__(self):
        super().__init__(can_be_explored=True)
    
    def trigger_event(self, hero):
        """Déclenche l'événement de la sortie"""
        pui.notify("found_exit", "")
        self.is_explored = True

class Portal(Location):
    """Représente un portail vers une prochaine zone ou un autre portail"""
    def __init__(self, name, exploration):
        super().__init__()
        self.name = name
        self.exploration = exploration
    
    def trigger_event(self, hero):
        """Déclenche l'événement de la porte"""
        if self.exploration:
            next_level = random.randint(1, 3) # Simuler la génération d'un prochain niveau
            next_level_str = f"Level {self.exploration.level + next_level}"
            pui.notify("found_portal", next_level_str)
            # Select to use or not the portal
            use_portal = questionary.confirm( f"Veux-tu utiliser le portail pour aller vers {next_level_str} ?" ).ask()
            if use_portal:
                self.exploration.next_level(next_level)
                return self.exploration
        else:
            pui.notify("found_portal", "nulle part")
        self.is_explored = True
        return self.exploration 

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