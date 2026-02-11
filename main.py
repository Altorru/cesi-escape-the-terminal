# Matrice représentant les différentes zones et leurs stages
# Chaque None correspond à une zone explorable ouverte
# Il y a aussi 3 Classes Door, Chest, Enemy pour les événements d'exploration
# Ces classes sont enfant de la classe Location

from characters import Enemy, Hero
from ui import PassiveUI

ui = PassiveUI()

ui.notify("title", "")
from exploration import MapMatrix, Exploration

# Création du héros
hero = Hero("Alex", 100, 15)

map_matrix = MapMatrix(3)
map_matrix.generate_events()
map_matrix.show_matrix()

exploration = Exploration(hero, map_matrix)
exploration.start()

print("\nExploration complete! 🎉")
