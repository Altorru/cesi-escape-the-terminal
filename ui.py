from rich.console import Console
from rich.panel import Panel

console = Console()

class PassiveUI:

  """============================== PRINTERS =============================="""
  @staticmethod
  def print_title():
    console.clear()
    console.print(Panel.fit(
      "[bold red]Escape from the Terminal[/bold red]\n",
      border_style="red"
    ))
  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""


class ActiveUI:

  """============================== PRINTERS =============================="""

  """============================== BUILDERS =============================="""

  """============================== Colorizer =============================="""
