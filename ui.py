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
      console.print(f"\n🚪 Tu as trouvé une porte menant vers {data.leads_to}!")

    if event_type == "found_chest":
      console.print("\n🧰 Tu as trouvé un coffre!")

    if event_type == "found_item":
      console.print(f"\n🔑 You found a {data.name}!")

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""


class ActiveUI(Observer):

  """============================== PRINTERS =============================="""

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""
