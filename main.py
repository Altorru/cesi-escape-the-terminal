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
from exploration import MapMatrix, Exploration

# Création du héros
hero = Hero("Alex", 100, 15)

# Création d'une matrice d'exploration avec des événements
exploration_matrix = [
    [None, Door("Door to Zone 2", "Zone 2"), Chest([Key("Silver Key", "Zone 3")])],
    [Enemy("Goblin", 30, 5, 20), None, Enemy("Orc", 50, 10, 40)],
    [Chest([Key("Gold Key", "Zone 4")]), Door("Door to Zone 3", "Zone 3"), None]
]

map_matrix = MapMatrix(3)
map_matrix.generate_events()
map_matrix.show_matrix()

exploration = Exploration(hero, map_matrix)
exploration.start()

print("\nExploration complete! 🎉")
