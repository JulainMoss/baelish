from __future__ import annotations
from units import Unit
from players import Player
from orders import Order

class Region:
    def __init__(self, name: str, power=0, supply=0):
        self.name = name
        self.allegiance = None
        self.order: Order = None
        self.army: list[Unit] = []
        self.power = power
        self.supply = supply
        self.neighbours: list[Region] = None
        self.isSea = False

    def setUpBorders(self, neighbours: list[Region]):
        self.neighbours = neighbours
    
    def raid(self, player: Player):
        self.order.raid(player)
        

class Land(Region):
    def __init__(self, name:str, power=0, supply=0, isHome=False, muster=0, garrison=0):
        super().__init__(name, power=power, supply=supply)
        self.powerToken = False
        self.home = isHome
        self.isSea = False
        self.muster = muster #0 - regular land, 1 - castle, 2 - fortress
        self.garrison = None
        if garrison:
            self.garrison = garrison
        if isHome:
            self.garrison = 2

class Sea(Region):
    def __init__(self, name):
        super().__init__(name)
        self.isSea = True
