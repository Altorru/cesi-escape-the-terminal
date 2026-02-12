from abc import ABC, abstractmethod

import questionary
from rich.console import Console
from rich.panel import Panel
import keyboard

console = Console()


class Observer(ABC):
    @abstractmethod
    def notify(self, event_type, data):
        """Mise à jour de l'observateur en fonction de l'événement"""
        pass


class PassiveUI(Observer):
    """============================== PRINTERS =============================="""
    """---------------- SCREENS -------------"""

    def notify(self, event_type, data):
        if event_type == "title":
            console.clear()
            console.print(Panel.fit(
                "[bold red]Escape from the Terminal[/bold red]\n",
                border_style="red"
            ))

        if event_type == "finished game":
            console.clear()
            console.print(Panel.fit(
                "[bold red]Vous avez terminé le jeu[/bold red]\n",
                border_style="red"
            ))

        """------------------- ENGINE EVENTS ----------------"""
        if event_type == "clear_screen":
            console.clear()

        """------------------- PLAYER EVENTS ----------------"""

        if event_type == "player_quit":
            console.print("\nJeux terminé. Tchao! 👋")

        if event_type == "moved_to_position":
            console.print(f"\nDéplacement vers {data}")

        """----------------- ENVIRONMENT EVENTS --------------------"""

        if event_type == "hit_outer_border":
            console.print("\n[red]Tu ne peux sortir de la carte ![/red]")

        if event_type == "hit_wall":
            console.print("\n[yellow]Tu t'est mangé un mur ![/yellow]")

        if event_type == "already_explored":
            console.print(
                "\nTu as déjà exploré cette zone. [i]Rien ne se passe.[/i]")

        if event_type == "empty_area":
            console.print("\n[orange]Il n'y a rien ici.[/orange]")

        """------------------- OBJECT EVENTS ----------------"""

        if event_type == "found_portal":
            console.print(
                f"\nTu as trouvé un portail menant vers [purple]{data}[/purple]!")

        if event_type == "found_chest":
            console.print("\nTu as trouvé un [green]coffre[/green]!")

        if event_type == "found_item":
            console.print(
                f"\nTu as trouvé [bold yellow]{data.name}![/bold yellow]"
                f"(Ouvre: {data.opens}")

        if event_type == "enemy_encounter":
            console.print(
                f"\nTu est tombé sur [bold red]{data.name}[/bold red]!"
                f"(HP: {data.health}, DMG: {data.attack})")

        if event_type == "enemy_defeated":
            console.print(f"\nTu as battu [red]{data.name}[/red] "
                          f"et gagné [blue]{data.dropped_exp} EXP ![/blue]")

        """============================== BUILDERS =============================="""
        """---------------- MAP BUILDING BLOCKS--------------------"""
        if event_type == "separator":
            console.print(f" | ".join(
                [str(type(event).__name__) if event else "Empty" for event in
                 data]))

        if event_type == "show_current_map":
            # data contains data[matrix]: matrice d'objets, data[current_position]: tuple
            # Border style then show the map matrix with the position of the player and the explored zones, else empty zones
            console.clear()

            def get_emoji(position, screen_matrix):
                return screen_matrix[position[0]][position[1]].emoji if \
                screen_matrix[position[0]][position[1]] else "⬜"

            map_str = ""
            matrix = data[0]
            current_position = data[1]
            for y, row in enumerate(matrix):
                for x, cell in enumerate(row):
                    if (y, x) == current_position:
                        map_str += "🧑 "  # Emoji for the player
                    elif cell and getattr(cell, "is_explored", False):
                        map_str += get_emoji((y, x), matrix) + " "
                    else:
                        map_str += "⬜ "
                map_str += "\n"

            console.print(
                Panel.fit(map_str, border_style="blue", title="Map"))

        """============================== Colorizer ==============================="""

class ActiveUI(Observer):
    """============================== PRINTERS ==============================="""

    def notify(self, event_type, data):
        """------------------- PLAYER EVENTS -----------------"""
        if event_type == "next_move":
            print("Utilisez les flèches pour vous déplacer et 'esc' pour quitter.")
            while True:
                event = keyboard.read_event()
                if event.event_type == keyboard.KEY_DOWN:
                    if event.name == "up":
                        return "Haut      ⮝"
                    elif event.name == "right":
                        return "Droite    ⮞"
                    elif event.name == "down":
                        return "Bas       ⮟"
                    elif event.name == "left":
                        return "Gauche    ⮜"
                    elif event.name == "esc":
                        return "Quitter"

        """============================== BUILDERS =============================="""

        """============================== Colorizer =============================="""
