from rich.console import Console
from rich.panel import Panel
from abc import ABC, abstractmethod

console = Console()

class Observer(ABC):
    @abstractmethod
    def notify(self, event_type, data):
        """Mise à jour de l'observateur en fonction de l'événement"""
        pass

class PassiveUI(Observer):

  """============================== PRINTERS =============================="""

  def notify(self, event_type, data):
    if event_type == "title":
      console.clear()
      console.print(Panel.fit(
        "[bold red]Escape from the Terminal[/bold red]\n",
        border_style="red"
      ))

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""


class ActiveUI(Observer):

  """============================== PRINTERS =============================="""

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""
