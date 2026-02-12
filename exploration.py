import random

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
        self.matrix = [
            [None for _ in range(self.size)] for _ in range(self.size)]
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
                if ((i, j)
                    # 50% de chance d'ajouter un mur
                    not in safe_zones and random.random() < 0.5):
                    self.matrix[i][j] = Wall()

        # Ajouter X portails aléatoires dans une case vide (1 portail tous les 5 niveaux)
        num_portals = max(1, exploration.level // 5)
        print(f"Generating {num_portals} portals for level {exploration.level}")
        for num in range(num_portals):
            while True:
                x, y = random.randint(0, self.size - 1), random.randint(0,
                                                                        self.size - 1)
                if self.matrix[x][y] is None:  # Si la case est vide
                    self.matrix[x][y] = Portal(f"Portal {num + 1}", exploration)
                    break

        # Étape 2 : Ajouter des événements aléatoires dans les cases restantes
        # (celles qui ne sont pas des murs)
        for i in range(self.size):
            for j in range(self.size):
                if self.matrix[i][j] is None:  # Si la case n'est pas un mur
                    self.matrix[i][j] = self.generate_random_event()

        self.matrix[0][0] = None  # Assurer que la position de départ est vide
        # Assurer que la position d'arrivée est une sortie
        self.matrix[self.size - 1][self.size - 1] = Exit(exploration)
        return self.matrix

    @staticmethod
    def generate_random_event():
        """Génère un événement aléatoire"""
        # Ajouter None pour les cases vides
        event_types = [None, Chest, Enemy]
        # Pondération pour favoriser les cases vides
        weights = [0.5, 0.25, 0.25]

        chosen_event_type = random.choices(event_types, weights=weights, k=1)[0]

        if chosen_event_type is Chest:
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
        self.level = level
        self.map = MapMatrix(5, self)
        self.current_position = (0, 0)

    def __str__(self):
        return f"Exploration Level {self.level}"

    def next_level(self, delta=1):
        """Passe au niveau suivant en générant une nouvelle carte et en
        réinitialisant la position du joueur"""
        self.level += delta
        # Augmenter la taille de la carte à chaque niveau
        self.map = MapMatrix(5 + self.level, self)
        self.current_position = (0, 0)
        pui.notify("clear_screen", "")
        pui.notify("welcome_to_level", self)
        pui.notify("show_current_map", [self.map.matrix, self.current_position])

    def move_player(self, direction):
        """Déplace le joueur dans la matrice en fonction de la direction choisie"""
        x, y = self.current_position
        if direction == "Haut" and x > 0:
            self.current_position = (x - 1, y)
        elif direction == "Bas" and x < self.map.size - 1:
            self.current_position = (x + 1, y)
        elif direction == "Gauche" and y > 0:
            self.current_position = (x, y - 1)
        elif direction == "Droite" and y < self.map.size - 1:
            self.current_position = (x, y + 1)
        else:
            return False, "border"

        current_cell = self.map.matrix[self.current_position[0]][
            self.current_position[1]]
        if (current_cell is not None and
            hasattr(current_cell, 'can_be_explored') and
            not current_cell.can_be_explored):
            if hasattr(current_cell, 'trigger_event'):
                current_cell.trigger_event(self.player)
            self.current_position = (x, y)  # Revert to the previous position
            return False, "wall"
        return True, None

    def trigger_current_event(self):
        """Déclenche l'événement de la case actuelle"""
        current_event = self.map.matrix[self.current_position[0]][
            self.current_position[1]]
        if current_event is not None and (
            (hasattr(current_event,
                     'is_explored') and not current_event.is_explored) or
            isinstance(current_event, Portal)):
            if hasattr(current_event, 'trigger_event'):
                current_event.trigger_event(self.player)
        elif (current_event is not None and
              hasattr(current_event, 'is_explored') and
              current_event.is_explored):
            pui.notify("already_explored", "")
        else:
            pui.notify("empty_area", "")

    def start(self):  # Move with questionary
        """Démarre l'exploration de la matrice"""
        previous_position_valid = True
        error_message = None

        while True:
            pui.notify("show_current_map",
                       [self.map.matrix, self.current_position])

            # Afficher le message d'erreur après la carte s'il y en a un
            if error_message:
                if error_message == "wall":
                    pui.notify("hit_wall", "")
                elif error_message == "border":
                    pui.notify("hit_outer_border", "")

            if previous_position_valid:
                self.trigger_current_event()

            # Demander au joueur où il veut aller ensuite
            next_move = aui.notify("next_move", "")

            if next_move == "Quitter":
                break

            previous_position_valid, error_message = self.move_player(next_move)