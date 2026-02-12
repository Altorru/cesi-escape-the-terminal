# Matrice représentant les différentes zones et leurs stages
# Chaque None correspond à une zone explorable ouverte.
# Il y a aussi 3 Classes Portale, Chest, Enemy pour les événements d'exploration
# Ces classes sont enfant de la classe Location.

from characters import Hero
from ui import PassiveUI
from exploration import Exploration

pui = PassiveUI()

pui.notify("title", "")

# Création du héros
hero = Hero("Alex", 100, 15)

exploration = Exploration(hero)
pui.notify("show_current_map", (exploration.map.matrix, (0, 0)))
exploration.start()
pui.notify("finished game", "")