from abc import ABC, abstractmethod

from pygments.lexers import data
from rich.console import Console
from rich.panel import Panel

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

    """----------------- CHARACTER EVENTS --------------"""
    if event_type == "character_move":
      console.print(f"\n➡️ On se déplace vers {data}...\n")

    """----------------- ENVIRONMENT EVENTS --------------------"""

    if event_type == "found_door":
      console.print(f"\nTu as trouvé une porte menant vers [purple]{data}[purple]!")

    if event_type == "found_chest":
      console.print("\nTu as trouvé un [green]coffre[green]!")

    if event_type == "found_item":
      console.print(f"\nTu as trouvé [bold yellow]{data.name}![bold yellow]"
                    f"(Ouvre: {data.opens}")

    if event_type == "blocked_move":
      console.print("\n[bold red]Tu as pris un mur ![bold red]"
                    " Tu ne peux pas aller dans cette direction.")

    if event_type == "enemy_encounter":
      console.print(f"\nTu est tombé sur [red]{data.name}[red]!"
                    f"(HP: {data.health}, DMG: {data.attack})")

    if event_type == "enemy_defeated":
      console.print(f"\n Tu as battu [red]{data.name}[red] "
                    f"et gagné [blue]{data.dropped_exp} EXP![blue]")
    """============================== BUILDERS =============================="""

    """============================== Colorizer =============================="""


class ActiveUI(Observer):

  """============================== PRINTERS =============================="""

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""
