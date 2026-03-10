from base import Portal, Chest, Wall, Location, Exit
from characters import Enemy, Hero
from objects import Key, Potion
from ui import PassiveUI, ActiveUI

pui = PassiveUI()
aui = ActiveUI()


class PathEvent:
    """Classe représentant un événement dans une case de la matrice d'exploration"""

    def __init__(self, location: Location):
        self.location = location

    def trigger_event(self, hero: Hero):
        """Déclenche l'événement associé à la location"""
        if isinstance(self.location, Portal):
            self.location.trigger_event(hero)

        elif isinstance(self.location, Chest):
            pui.notify("found_chest", "")
            for item in self.location.contents:
                hero.inventory.append(item)
                if isinstance(item, Key):
                    pui.notify("found_item", item)
        elif isinstance(self.location, Enemy):
            enemy = self.location
            pui.notify("enemy_encounter", enemy)
            pui.notify("enemy_defeated", enemy)
            hero.exp += enemy.dropped_exp

        elif isinstance(self.location, Wall):
            self.location.trigger_event(hero)

        elif isinstance(self.location, Exit):
            self.location.trigger_event(hero)

        return None


class RpgFightEvent:
    """Classe représentant un événement de combat contre un ennemi"""

    def __init__(self, enemy: Enemy):
        self.enemy = enemy

    def trigger_event(self, hero: Hero):
        """Déclenche l'événement de combat contre l'ennemi, choix du joueur pour attaquer, ouvrir l'inventaire, ou fuir"""
        pui.notify("enemy_encounter", self.enemy)
        while hero.is_alive() and self.enemy.is_alive():
            action = aui.notify("choose_fight_action", "")
            if action == "Attaquer":
                hero.attack_target(self.enemy)
            elif (
                action == "Inventaire"
            ):  # Affiche l'inventaire et permet d'utiliser une potion de soin sinon retourne au choix d'action
                item_selected = aui.notify("show_inventory", hero.inventory)
                if isinstance(item_selected, Potion):
                    hero.heal(item_selected.heal_amount)
                    hero.inventory.remove(item_selected)
                    pui.notify("show_health_bar_and_name", hero)
                else:
                    continue
            elif action == "Fuir":
                pui.notify("fled_from_battle", "")
                return None
            if self.enemy.is_alive():
                self.enemy.attack_target(hero)
            pui.notify("show_health_bar_and_name", self.enemy)
            pui.notify("show_health_bar_and_name", hero)
        if hero.is_alive():
            pui.notify(
                "enemy_defeated",
                self.enemy,
            )
        else:
            pui.notify("player_defeated", "")
            exit()
        hero.exp += self.enemy.dropped_exp
        return None
