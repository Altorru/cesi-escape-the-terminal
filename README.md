# 🎮 Escape from the Terminal

Un jeu d'exploration de donjon roguelike développé en Python appliquant les principes de la Programmation Orientée Objet (POO) et les principes SOLID.

**Projet réalisé en binôme pour CESI CDA 2026**

---

## 📋 Table des matières

- [Introduction](#-introduction)
- [Quickstart](#-quickstart)
- [Concepts de POO Utilisés](#-concepts-de-poo-utilisés)
- [Principes SOLID Appliqués](#-principes-solid-appliqués)
- [Design Patterns](#-design-patterns)
- [Architecture du Projet](#-architecture-du-projet)

---

## 🎯 Introduction

**Escape from the Terminal** est un jeu d'exploration de donjon en mode texte où le joueur incarne un héros qui doit naviguer à travers des niveaux générés procéduralement. Le joueur peut combattre des ennemis, découvrir des trésors, collecter des clés pour déverrouiller des portails, et progresser à travers différents niveaux.

### Fonctionnalités principales

- 🗺️ **Génération procédurale** de cartes avec des chemins garantis
- ⚔️ **Système de combat** au tour par tour contre divers ennemis
- 🎒 **Gestion d'inventaire** avec potions de soin et clés
- 🌀 **Portails verrouillés** nécessitant des clés pour accéder à des niveaux bonus
- 📊 **Système de progression** avec points d'expérience
- 🎨 **Interface utilisateur riche** avec emojis et interactions au clavier

---

## 🚀 Quickstart

### Méthode 1 (sans Docker)

#### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

#### Installation

1. **Cloner ou télécharger le projet**

```bash
cd cesi-escape-the-terminal
```

2. **Créer un environnement virtuel (recommandé)**

```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
# ou
venv\Scripts\activate  # Sur Windows
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

#### Lancer le jeu

```bash
python main.py
```

#### Contrôles

- **Flèches directionnelles** : Déplacer le héros (↑ ↓ ← →)
- **I** : Ouvrir l'inventaire
- **Q** : Quitter le jeu

### Méthode 2 (avec Docker)

1. **Construire l'image Docker**

```bash
docker build -t escape-terminal .
```

2. **Lancer le conteneur**

```bash
docker run -it escape-terminal
```

3. **Contrôles**

- **Flèches directionnelles** : Déplacer le héros (↑ ↓ ← →)
- **I** : Ouvrir l'inventaire
- **Q** : Quitter le jeu

---

## 🏗️ Concepts de POO Utilisés

### 1. **Classes et Objets**

Tout dans le jeu est représenté par des objets issus de classes bien définies.

**Exemples :**
- [`characters.py`](characters.py) : `Character`, `Hero`, `Enemy`
- [`base.py`](base.py) : `Location`, `Wall`, `Exit`, `Portal`, `Chest`
- [`objects.py`](objects.py) : `Object`, `Key`, `Potion`

```python
# Création d'un héros (objet de la classe Hero)
hero = Hero("Alex", 100, 15)
```

---

### 2. **Héritage**

L'héritage permet de créer des hiérarchies de classes et de réutiliser du code.

#### Héritage simple

**Fichier [`characters.py`](characters.py) :**

```python
class Character:
    """Classe de base pour tous les personnages"""
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

class Hero(Character):
    """Le héros hérite de Character et ajoute exp et inventory"""
    def __init__(self, name, health, attack):
        super().__init__(name, health, attack)
        self.exp = 0
        self.inventory = []
```

**Utilisé dans :**
- `Character` → `Hero`, `Enemy` ([`characters.py`](characters.py))
- `Location` → `Wall`, `Exit`, `Portal`, `Chest` ([`base.py`](base.py))
- `Object` → `Key`, `Potion` ([`objects.py`](objects.py))

#### Héritage multiple

**Fichier [`characters.py`](characters.py) :**

```python
class Enemy(Character, Location):
    """Enemy hérite à la fois de Character et Location"""
    def __init__(self, name, health, attack, dropped_exp):
        super().__init__(name, health, attack)
        self.dropped_exp = dropped_exp
        self.is_explored = False
        self.can_be_explored = True
```

Cela permet à `Enemy` d'être à la fois un personnage combattant ET une location explorable sur la carte.

---

### 3. **Encapsulation**

L'encapsulation consiste à regrouper les données et les méthodes qui les manipulent dans une classe, tout en contrôlant l'accès.

**Fichier [`characters.py`](characters.py) :**

```python
class Character:
    def is_alive(self):
        """Méthode qui encapsule la logique de vérification de vie"""
        return self.health > 0

    def take_damage(self, damage):
        """Contrôle la modification de la santé"""
        self.health -= damage
    
    def heal(self, amount):
        """Empêche de dépasser max_health"""
        self.health = min(self.max_health, self.health + amount)
```

**Avantages :**
- Protège l'intégrité des données (ex: `heal()` ne permet pas de dépasser `max_health`)
- Centralise la logique métier
- Facilite la maintenance

---

### 4. **Polymorphisme**

Le polymorphisme permet d'utiliser une même interface pour différentes implémentations.

#### Polymorphisme de méthode

**Fichier [`base.py`](base.py) :**

Toutes les classes héritant de `Location` implémentent `trigger_event()` différemment :

```python
class Wall(Location):
    def trigger_event(self, hero):
        """Ne fait rien, bloque simplement"""
        self.is_explored = True

class Portal(Location):
    def trigger_event(self, hero):
        """Téléporte vers un autre niveau"""
        if self.is_locked and has_key:
            self.exploration.next_level(next_level)

class Chest(Location):
    def trigger_event(self, hero):
        """Ajoute des objets à l'inventaire"""
        for item in self.contents:
            hero.inventory.append(item)
```

**Fichier [`exploration.py`](exploration.py) :**

```python
def trigger_current_event(self):
    current_event = self.map.matrix[self.current_position[0]][self.current_position[1]]
    if hasattr(current_event, 'trigger_event'):
        current_event.trigger_event(self.player)  # Appel polymorphe
```

Peu importe le type de `Location`, on peut appeler `trigger_event()` et obtenir le comportement approprié.

---

### 5. **Abstraction**

L'abstraction force les classes filles à implémenter certaines méthodes, créant des contrats clairs.

**Fichier [`base.py`](base.py) :**

```python
from abc import ABC, abstractmethod

class Location(ABC):
    """Classe abstraite définissant le contrat pour toutes les locations"""
    @abstractmethod
    def trigger_event(self, hero):
        """Méthode abstraite que TOUTES les sous-classes doivent implémenter"""
        pass
```

**Fichier [`ui.py`](ui.py) :**

```python
class Observer(ABC):
    @abstractmethod
    def notify(self, event_type, data):
        """Toutes les UI doivent implémenter cette méthode"""
        pass

class PassiveUI(Observer):
    def notify(self, event_type, data):
        # Implémentation pour l'affichage passif
        if event_type == "enemy_encounter":
            console.print(f"Tu es tombé sur {data.name}!")

class ActiveUI(Observer):
    def notify(self, event_type, data):
        # Implémentation pour les interactions utilisateur
        if event_type == "next_move":
            return get_key()
```

**Avantages :**
- Garantit que toutes les sous-classes respectent le contrat
- Facilite l'extension du code
- Empêche l'instanciation de classes incomplètes

---

### 6. **Composition**

La composition consiste à créer des objets complexes en combinant d'autres objets.

**Fichier [`exploration.py`](exploration.py) :**

```python
class Exploration:
    def __init__(self, player, level=1):
        self.player = player  # Composition : Exploration POSSÈDE un Hero
        self.map = MapMatrix(5, self)  # Composition : Exploration POSSÈDE une MapMatrix
        self.portals_list = []

class MapMatrix:
    def __init__(self, size, exploration=None):
        self.matrix = self.generate_procedural_map(exploration)
        # Composition : La matrice contient des objets Location
```

**Relation : "HAS-A" vs "IS-A"**
- Héritage : "Hero IS-A Character" (hérite)
- Composition : "Exploration HAS-A MapMatrix" (possède)

---

## 🎖️ Principes SOLID Appliqués

Les principes SOLID sont cinq principes de conception orientée objet qui rendent le code plus maintenable, flexible et évolutif.

---

### 1. **S - Single Responsibility Principle (SRP)**

> *"Une classe ne devrait avoir qu'une seule raison de changer"*

Chaque classe a une responsabilité unique et bien définie.

#### Exemples :

| Classe | Responsabilité unique | Fichier |
|--------|----------------------|---------|
| `Character` | Gérer la santé et les attaques d'un personnage | [`characters.py`](characters.py) |
| `Location` | Définir un emplacement explorable | [`base.py`](base.py) |
| `MapMatrix` | Générer et gérer la carte du niveau | [`exploration.py`](exploration.py) |
| `RpgFightEvent` | Gérer le déroulement d'un combat | [`events.py`](events.py) |
| `PassiveUI` | Afficher des informations à l'utilisateur | [`ui.py`](ui.py) |
| `ActiveUI` | Récupérer les entrées utilisateur | [`ui.py`](ui.py) |
| `LocationFactory` | Créer des instances de locations | [`factories.py`](factories.py) |
| `ObjectFactory` | Créer des instances d'objets | [`factories.py`](factories.py) |

**Contre-exemple (à éviter) :**
Une classe `Game` qui gèrerait à la fois l'affichage, la logique de combat, la génération de cartes, et la gestion des personnages violerait le SRP.

---

### 2. **O - Open/Closed Principle (OCP)**

> *"Les classes doivent être ouvertes à l'extension mais fermées à la modification"*

On peut ajouter de nouvelles fonctionnalités sans modifier le code existant.

#### Exemple avec `Location`

**Fichier [`base.py`](base.py) :**

```python
class Location(ABC):
    @abstractmethod
    def trigger_event(self, hero):
        pass
```

**Extension sans modification :**

Pour ajouter un nouveau type de location (ex: `Trap`), on n'a pas besoin de modifier `Location` ni les autres sous-classes :

```python
class Trap(Location):
    def trigger_event(self, hero):
        hero.take_damage(10)
        pui.notify("trap_triggered", "")
```

#### Exemple avec les Factories

**Fichier [`factories.py`](factories.py) :**

Les factories permettent d'ajouter de nouveaux types d'ennemis ou d'objets sans modifier la logique d'exploration :

```python
class LocationFactory:
    @staticmethod
    def create_enemy(name=None):
        enemy_types = [
            {"name": "un Goblin", "health": 30, "attack": 5, "reward": 20},
            {"name": "un Orc", "health": 50, "attack": 10, "reward": 40},
            {"name": "un Troll", "health": 80, "attack": 15, "reward": 60},
        ]
        # Pour ajouter un nouveau type, il suffit d'ajouter un dictionnaire
```

---

### 3. **L - Liskov Substitution Principle (LSP)**

> *"Les objets d'une classe dérivée doivent pouvoir remplacer les objets de la classe de base sans altérer le fonctionnement du programme"*

Toute sous-classe doit pouvoir être utilisée à la place de sa classe parente.

#### Exemple avec `Location`

**Fichier [`exploration.py`](exploration.py) :**

```python
def trigger_current_event(self):
    current_event = self.map.matrix[self.current_position[0]][self.current_position[1]]
    # current_event peut être Wall, Portal, Chest, Enemy, Exit...
    # Tous respectent le contrat de Location
    if hasattr(current_event, 'trigger_event'):
        current_event.trigger_event(self.player)
```

Peu importe le type exact de `Location`, le code fonctionne car toutes les sous-classes respectent le contrat `trigger_event(hero)`.

#### Exemple avec `Character`

**Fichier [`characters.py`](characters.py) :**

```python
def attack_target(self, target):
    target.take_damage(self.attack)
```

On peut passer n'importe quel `Character` (Hero ou Enemy) en tant que `target`, car tous ont la méthode `take_damage()`.

---

### 4. **I - Interface Segregation Principle (ISP)**

> *"Les clients ne doivent pas dépendre d'interfaces qu'ils n'utilisent pas"*

Créer des interfaces spécifiques plutôt qu'une interface générale massive.

#### Exemple avec `Observer`

**Fichier [`ui.py`](ui.py) :**

```python
class Observer(ABC):
    @abstractmethod
    def notify(self, event_type, data):
        pass
```

L'interface `Observer` est minimale : une seule méthode `notify()`. Les classes UI n'ont pas à implémenter des dizaines de méthodes inutilisées.

Les UI peuvent choisir de réagir uniquement aux événements qui les concernent :

```python
class PassiveUI(Observer):
    def notify(self, event_type, data):
        if event_type == "enemy_encounter":
            console.print(f"Rencontre avec {data.name}")
        # Ignore les autres événements non pertinents
```

#### Séparation `PassiveUI` vs `ActiveUI`

Au lieu d'avoir une seule grosse classe `UI` avec toutes les méthodes d'affichage ET d'interaction, on sépare :

- **PassiveUI** : Affichage uniquement (lecture seule)
- **ActiveUI** : Interactions utilisateur (lecture des touches, sélections)

---

### 5. **D - Dependency Inversion Principle (DIP)**

> *"Les modules de haut niveau ne doivent pas dépendre des modules de bas niveau. Les deux doivent dépendre d'abstractions."*

On dépend d'interfaces abstraites, pas d'implémentations concrètes.

#### Exemple avec `Exploration` et `Location`

**Fichier [`exploration.py`](exploration.py) :**

```python
class Exploration:
    def trigger_current_event(self):
        current_event = self.map.matrix[...]  # Peut être n'importe quelle Location
        if hasattr(current_event, 'trigger_event'):
            current_event.trigger_event(self.player)
```

`Exploration` ne dépend pas directement de `Portal`, `Chest`, ou `Enemy`. Elle dépend de l'abstraction `Location` et de son contrat `trigger_event()`.

#### Exemple avec `Observer`

**Fichiers [`ui.py`](ui.py), [`base.py`](base.py), [`events.py`](events.py), [`exploration.py`](exploration.py) :**

```python
pui = PassiveUI()  # Instanciation d'un Observer

# Les autres modules utilisent l'interface Observer, pas PassiveUI directement
pui.notify("event_type", data)
```

Si on veut changer l'implémentation de l'UI (ex: interface graphique), on peut créer une nouvelle classe implémentant `Observer` sans toucher au code métier.

---

## 🎨 Design Patterns

### 1. **Factory Pattern** (Patron Fabrique)

Centralise la création d'objets complexes dans des classes dédiées.

**Fichier [`factories.py`](factories.py) :**

```python
class LocationFactory:
    @staticmethod
    def create_portal(exploration):
        names = ["un Portail Secret", "un Portail Mystérieux"]
        name = random.choice(names)
        return Portal(name, exploration)
    
    @staticmethod
    def create_enemy():
        enemy_types = [...]
        enemy_info = random.choice(enemy_types)
        return Enemy(enemy_info["name"], enemy_info["health"], ...)

class ObjectFactory:
    @staticmethod
    def create_key(opens):
        names = ["une Clé en Fer", "une Clé en Or"]
        return Key(random.choice(names), opens)
```

**Avantages :**
- Centralise la logique de création
- Facilite l'ajout de nouveaux types
- Rend le code plus testable

**Utilisé dans :**
- [`exploration.py`](exploration.py) : `LocationFactory.create_enemy()`, `ObjectFactory.create_key()`

---

### 2. **Observer Pattern** (Patron Observateur)

Permet à des objets de s'abonner et de réagir à des événements sans couplage fort.

**Fichier [`ui.py`](ui.py) :**

```python
class Observer(ABC):
    @abstractmethod
    def notify(self, event_type, data):
        pass

class PassiveUI(Observer):
    def notify(self, event_type, data):
        if event_type == "enemy_encounter":
            console.print(f"Rencontre avec {data.name}!")
```

**Utilisé partout dans le code :**

```python
pui = PassiveUI()
pui.notify("found_chest", "")
pui.notify("enemy_defeated", enemy)
```

**Avantages :**
- Découple la logique métier de l'affichage
- Facilite le changement d'interface (terminal → GUI)
- Permet d'ajouter des observateurs sans modifier le code existant

---

### 3. **Strategy Pattern** (Patron Stratégie)

Différentes implémentations de `trigger_event()` permettent de changer le comportement d'une location sans modifier le code appelant.

**Fichier [`base.py`](base.py) :**

```python
class Wall(Location):
    def trigger_event(self, hero):
        # Stratégie : Ne rien faire

class Chest(Location):
    def trigger_event(self, hero):
        # Stratégie : Ajouter des objets à l'inventaire

class Enemy(Character, Location):
    def trigger_event(self, hero):
        # Stratégie : Déclencher un combat
```

---

## 📁 Architecture du Projet

```
cesi-escape-the-terminal/
│
├── main.py                 # Point d'entrée du jeu
├── base.py                 # Classes de base abstraites (Location et ses dérivées)
├── characters.py           # Personnages (Character, Hero, Enemy)
├── objects.py              # Objets du jeu (Key, Potion)
├── events.py               # Événements (PathEvent, RpgFightEvent)
├── exploration.py          # Logique d'exploration (MapMatrix, Exploration)
├── factories.py            # Factories pour créer objets et locations
├── ui.py                   # Interfaces utilisateur (Observer, PassiveUI, ActiveUI)
└── requirements.txt        # Dépendances Python
```

### Flux d'exécution

```
main.py
  ↓
Création du Hero
  ↓
Création de l'Exploration (contient MapMatrix)
  ↓
MapMatrix génère la carte avec des Locations
  ↓
Boucle de jeu (Exploration.start())
  ↓
- Affichage de la carte (PassiveUI)
- Lecture des entrées (ActiveUI)
- Déplacement du héros
- Déclenchement des événements (trigger_event)
  ↓
Combat, coffres, portails...
  ↓
Progression vers le niveau suivant
```

---

## 🎓 Principes Pédagogiques

Ce projet illustre les concepts fondamentaux de la POO et les principes SOLID de manière pratique :

### Concepts POO démontrés :
- ✅ **Classes et Objets**
- ✅ **Héritage simple et multiple**
- ✅ **Encapsulation**
- ✅ **Polymorphisme**
- ✅ **Abstraction (ABC)**
- ✅ **Composition**

### Principes SOLID démontrés :
- ✅ **Single Responsibility** : Chaque classe a une seule responsabilité
- ✅ **Open/Closed** : Extension sans modification via héritage et factories
- ✅ **Liskov Substitution** : Les sous-classes sont interchangeables
- ✅ **Interface Segregation** : Interfaces minimales et spécifiques
- ✅ **Dependency Inversion** : Dépendance aux abstractions

### Design Patterns :
- ✅ **Factory Pattern** : Création centralisée d'objets
- ✅ **Observer Pattern** : Découplage UI et logique métier
- ✅ **Strategy Pattern** : Comportements interchangeables

---

## 📚 Ressources

- [Python ABC Module](https://docs.python.org/3/library/abc.html)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [Design Patterns in Python](https://refactoring.guru/design-patterns/python)

---

## 👥 Auteurs

Projet réalisé en binôme pour **CESI CDA 2026** avec [Evan Viguié](https://github.com/EvanViguie)