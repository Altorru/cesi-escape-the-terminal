import random

import questionary

from base import Portal, Chest, Wall, Exit
from characters import Enemy
from factories import LocationFactory
from ui import PassiveUI, ActiveUI

pui = PassiveUI()
aui = ActiveUI()

class MapMatrix:
    def __init__(self, size, exploration=None):
        self.size = size
        self.matrix = self.generate_procedural_map(exploration)
    
    def generate_procedural_map(self, exploration):
        """Génère une matrice de la carte avec premièrement des murs pour créer des chemins, puis ajoute des événements aléatoires dans les cases restantes"""
        # Étape 1 : Générer des murs pour créer au moins un chemin de la position de départ (0, 0) à la position d'arrivée (size-1, size-1)
        # Parcourir en démarrant de 0 0 aléatoirement vers le bas ou la droite, et ajouter des murs aléatoires sur les cases non visitées
        x, y = 0, 0
        self.matrix = [[None for _ in range(self.size)] for _ in range(self.size)]
        safe_zones = [(0, 0), (self.size - 1, self.size - 1)]
        while (x, y) != (self.size - 1, self.size - 1):
            self.matrix[x][y] = None  # Assurer que le chemin est libre
            if x < self.size - 1 and y < self.size - 1:
                if random.choice([True, False]):
                    y += 1  # Aller à droite
                else:
                    x += 1  # Aller en bas
                safe_zones.append((x, y))
            elif x < self.size - 1:
                x += 1  # Aller en bas
                safe_zones.append((x, y))
            elif y < self.size - 1:
                y += 1  # Aller à droite
                safe_zones.append((x, y))

        # Ajouter des murs aléatoires dans les cases non visitées
        for i in range(self.size):
            for j in range(self.size):
                if (i, j) not in safe_zones and random.random() < 0.5:  # 50% de chance d'ajouter un mur
                    self.matrix[i][j] = Wall()
        
        # Étape 2 : Ajouter des événements aléatoires dans les cases restantes (celles qui ne sont pas des murs)
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] is None:  # Si la case n'est pas un mur
                    self.matrix[i][j] = self.generate_random_event(exploration)

        self.matrix[0][0] = None  # Assurer que la position de départ est vide
        self.matrix[self.size - 1][self.size - 1] = Exit()  # Assurer que la position d'arrivée est une sortie
        return self.matrix

    @staticmethod
    def generate_random_event(exploration):
        """Génère un événement aléatoire"""
        event_types = [None, Portal, Chest, Enemy]  # Ajouter None pour les cases vides
        weights = [0.4, 0.1, 0.25, 0.25] # Pondération pour favoriser les cases vides

        chosen_event_type = random.choices(event_types, weights=weights, k=1)[0]

        if chosen_event_type is Portal:
            return LocationFactory.create_portal(exploration)
        elif chosen_event_type is Chest:
            return LocationFactory.create_chest()
        elif chosen_event_type is Enemy:
            return LocationFactory.create_enemy()
        else:
            return None
    
    def show_matrix(self):
        """Affiche la matrice de la carte"""
        for row in self.matrix:
            pui.notify("separator", row)

class Exploration:
    def __init__(self, player, level=1):
        self.player = player
        self.map = MapMatrix(5, self)
        self.current_position = (0, 0)  # Position de départ
        self.level = level
    
    def __str__(self):
        return f"Exploration Level {self.level}"    
    
    def next_level(self, delta=1):
        """Passe au niveau suivant en générant une nouvelle carte et en réinitialisant la position du joueur"""
        self.level += delta
        self.map = MapMatrix(5 + self.level, self) # Augmenter la taille de la carte à chaque niveau
        self.current_position = (0, 0)
        print(f"\n🎉 Welcome to {self}!")
        self.map.show_matrix()

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
            pui.notify("hit_outer_border", "")
            return False
        if (self.map.matrix[self.current_position[0]][self.current_position[1]]
            and not self.map.matrix[self.current_position[0]][self.current_position[1]].
                can_be_explored):
            pui.notify("hit_wall", "")
            self.current_position = (x, y)  # Revert to the previous position
            return False
        pui.notify("moved_to_position", self.current_position )
        return True
    
    def trigger_current_event(self):
        """Déclenche l'événement de la case actuelle"""
        current_event = self.map.matrix[self.current_position[0]][self.current_position[1]]
        if current_event and (not current_event.is_explored or isinstance(current_event, Portal)):
            current_event.trigger_event(self.player)
            if isinstance(current_event, Exit):
                exit(0)
        elif current_event and current_event.is_explored:
            pui.notify("already_explored", "")
            print("\n🔁 You've already explored this area. Nothing happens.")
        else:
            print("\n🌳 This area is empty. Nothing happens.")
    
    def start(self): # Move with questionary
        """Démarre l'exploration de la matrice"""
        previous_position_valid = True
        while True:
            if previous_position_valid:
                self.trigger_current_event()

            # Demander au joueur où il veut aller ensuite
            next_move = questionary.select(
                "Where do you want to go next?",
                choices=["Up", "Down", "Left", "Right", "Exit Exploration"]
            ).ask()

            if next_move == "Exit Exploration":
                print("\nExiting exploration. Goodbye! 👋")
                break
            
            previous_position_valid = self.move_player(next_move)
    
    