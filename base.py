import random

class Location:
    """Classe de base pour les différentes locations (Door, Chest, etc...)"""
    def __init__(self, can_be_explored=True):
        self.can_be_explored = can_be_explored

class Door(Location):
    """Représente une porte dans une zone d'exploration"""
    def __init__(self, name, leads_to):
        super().__init__()
        self.name = name
        self.leads_to = leads_to  # Zone vers laquelle la porte mène

class Chest(Location):
    """Représente un coffre dans une zone d'exploration"""
    def __init__(self, contents):
        super().__init__()
        self.contents = contents  # Contenu du coffre (ex: arme, potion)