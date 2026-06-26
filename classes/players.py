import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orders import Order
    from .regions import Region
from .units import Unit, Levy, Knight, Siege, Ship
from .utils import MAX_SUPPLY

unitNames = {"knight": Knight, "levy": Levy, "ship": Ship, "siege": Siege}

setUps = {
    "House Baratheon": {"Smocza Skała": {"knight": 1, "levy": 1}, "Zatoka Rozbitków": {"ship": 2}, "Królewski Las": {"levy": 1}},
    "House Stark": {"Morze Dreszczy": {"ship": 1}, "Biały Port": {"levy": 1}, "Winterfell": {"knight": 1, "levy": 1}},
    "House Lannister": {"Złota Cieśnina": {"ship": 1}, "Kamienny Sept": {"levy": 1}, "Lannisport": {"knight": 1, "levy": 1}},
    "House Greyjoy": {"Strażnica n. Szarą Wodą": {"levy": 1}, "Zatoka Żelaznych Ludzi": {"ship" : 1}, "Pyke" : {"knight": 1, "levy": 1, "ship": 1}},
    "House Tyrell": {"Cieśnina Redwyne'ów": {"ship": 1}, "Dornijskie Pogranicze": {"levy": 1}, "Wysogród": {"levy": 1, "knight": 1}},
    "House Martell": {"Morze Dornijskie": {"ship": 1}, "Słoneczna Włócznia": {"knight": 1, "levy": 1}, "Słony Brzeg": {"levy": 1}},
    "House Targaryen": {},
    "House Arryn": {},
    "Unknown Player": {}
}

class Player:
    def __init__(self):
        self.castleCount = 0
        self.power = 0
        self.orders: list[Order] = []
        self.regions: list[Region] = []
        self.cards = [] # TODO implement house cards
        self.ironThrone = 0
        self.levies = 0
        self.court = 0
        self.powerToGain = 20

    def __str__(self):
        return "Unknown Player"

    def setUp(self, regions: dict[str, Region]):
        unitSetUp = setUps[str(self)]
        for region in unitSetUp.keys():
            for type in unitSetUp[region].keys():
                for _ in range(unitSetUp[region][type]):
                    __ = unitNames[type](regions[region], self)

    def countCrowns(self) -> int:
        return np.sum([region.power for region in self.regions])
    
    def countSupply(self) -> int:
        return max(np.sum([region.supply for region in self.regions]), MAX_SUPPLY)
    
    def countScore(self) -> int:
        return len([region for region in self.regions if region.muster > 0])
    
    def armies(self) -> list[tuple[str, int]]:
        return sorted(
            [(region.name, region.army) for region in self.regions if region.army > 0], 
            reverse=True
        )
    
    def decideSupport(region: Region): # 3rd party support - others are implied
        return False
    
class Baratheon(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Baratheon"

class Stark(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Stark"

class Lannister(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Lannister"

class Greyjoy(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Greyjoy"

class Tyrell(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Tyrell"

class Martell(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Martell"

class Arryn(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Arryn"

class Targaryen(Player):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "House Targaryen"