from characters import Hero
from exploration import Exploration
from ui import PassiveUI

pui = PassiveUI()

pui.notify("title", "")

# Création du héros
hero = Hero("Alex", 100, 15)

exploration = Exploration(hero)
exploration.start()