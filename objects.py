class Object:
    """Classe de base pour les objets (Weapon, Potion, Clé, etc...)"""
    def __init__(self, name):
        self.name = name

class Key(Object):
    """Représente une clé pour ouvrir des portes"""
    def __init__(self, name, opens):
        super().__init__(name)
        self.opens = opens  # Type de porte que la clé peut ouvrir
    
class Potion(Object):
    """Représente une potion de soin"""
    def __init__(self, name, heal_amount):
        super().__init__(name)
        self.heal_amount = heal_amount  # Quantité de points de vie restaurés