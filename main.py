# Matrice représentant les différentes zones et leurs stages
# Chaque None correspond à une zone explorable ouverte
# Il y a aussi 3 Classes Door, Chest, Enemy pour les événements d'exploration
# Ces classes sont enfant de la classe Location

from base import Door, Chest
from characters import Enemy, Hero
from objects import Key
from ui import PassiveUI

ui = PassiveUI()

ui.notify("title", "")

# Création du héros
hero = Hero("Alex", 100, 15)

# Création d'une matrice d'exploration avec des événements
exploration_matrix = [
    [None, Door("Door to Zone 2", "Zone 2"), Chest([Key("Silver Key", "Zone 3")])],
    [Enemy("Goblin", 30, 5, 20), None, Enemy("Orc", 50, 10, 40)],
    [Chest([Key("Gold Key", "Zone 4")]), Door("Door to Zone 3", "Zone 3"), None]
]

# Simulation d'une exploration
for i in range(len(exploration_matrix)):
    for j in range(len(exploration_matrix[i])):
        location = exploration_matrix[i][j]
        if location is not None:
            result = location.trigger_event(hero)
            if result is not None:
                ui.notify("character_move", result)
                # Ici, vous pourriez implémenter la logique pour changer de zone d'exploration

ui.notify("victory_screen", "")
