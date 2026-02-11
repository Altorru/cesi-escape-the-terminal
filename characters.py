class Character:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def is_alive(self):
        return self.health > 0

    def take_damage(self, damage):
        self.health -= damage
    
    def attack_target(self, target):
        target.take_damage(self.attack)

class Enemy(Character):
    """Représente un ennemi dans une zone d'exploration"""
    def __init__(self, name, health, attack, dropped_exp):
        super().__init__(name, health, attack)
        self.dropped_exp = dropped_exp

class Hero(Character):
    """Représente le héros du jeu"""
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)
        self.exp = 0
        self.inventory = []