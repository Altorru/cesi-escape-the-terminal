import inspect
import sys
import random
from base import Location, Door, Chest
from characters import Enemy
from factories import LocationFactory

class MapMatrix:
    def __init__(self, size):
        self.size = size
        self.matrix = [[None for _ in range(size)] for _ in range(size)]
    
    def generate_events(self):
        """Génère des événements aléatoires pour chaque case de la matrice"""
        for i in range(self.size):
            for j in range(self.size):
                self.matrix[i][j] = self.generate_random_event()

    def generate_random_event(self):
        """Génère un événement aléatoire"""
        event_types = [None, Door, Chest, Enemy]  # Ajouter None pour les cases vides

        chosen_event_type = random.choice(event_types)

        if chosen_event_type is Door:
            return LocationFactory.create_door()
        elif chosen_event_type is Chest:
            return LocationFactory.create_chest()
        elif chosen_event_type is Enemy:
            return LocationFactory.create_enemy()
        else:
            return None
    
    def show_matrix(self):
        """Affiche la matrice de la carte"""
        for row in self.matrix:
            print(" | ".join([str(type(event).__name__) if event else "Empty" for event in row]))

class Exploration:
    def __init__(self, player, matrix):
        self.player = player
        self.matrix = matrix
    
    