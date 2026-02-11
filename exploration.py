import questionary
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
    def __init__(self, player, map):
        self.player = player
        self.map = map
        self.current_position = (0, 0)  # Position de départ

    def move_player(self, direction):
        """Déplace le joueur dans la matrice en fonction de la direction choisie"""
        x, y = self.current_position
        if direction == "Up" and x > 0:
            self.current_position = (x - 1, y)
        elif direction == "Down" and x < self.map.size - 1:
            self.current_position = (x + 1, y)
        elif direction == "Left" and y > 0:
            self.current_position = (x, y - 1)
        elif direction == "Right" and y < self.map.size - 1:
            self.current_position = (x, y + 1)
        else:
            print("\n🚫 You can't move in that direction!")
    
    def start(self): # Move with questionary
        """Démarre l'exploration de la matrice"""
        while True:
            current_event = self.map.matrix[self.current_position[0]][self.current_position[1]]
            if current_event:
                result = current_event.trigger_event(self.player)
                if result is not None:
                    print(f"\n➡️ Moving to {result}...\n")
                    # Ici, vous pourriez implémenter la logique pour changer de zone d'exploration
            else:
                print("\n🌳 You are in an empty area. Nothing happens.")
            
            # Demander au joueur où il veut aller ensuite
            next_move = questionary.select(
                "Where do you want to go next?",
                choices=["Up", "Down", "Left", "Right", "Exit Exploration"]
            ).ask()

            if next_move == "Exit Exploration":
                print("\nExiting exploration. Goodbye! 👋")
                break
            
            self.move_player(next_move)
        
    