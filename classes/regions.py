from __future__ import annotations
import numpy as np
from units import Unit
from players import Player
from orders import Order

class Region:
    def __init__(self, name: str, power=0, supply=0):
        self.name = name
        self.allegiance: Player = None
        self.order: Order = Order
        self.army: list[Unit] = []
        self.muster = 0
        self.power = power
        self.supply = supply
        self.neighbours: list[Region] = None
        self.isSea = False
        self.garrison = None

    def setUpBorders(self, neighbours: list[Region]):
        self.neighbours = neighbours
    
    def raid(self, player: Player):
        self.order.raid(player)

    def defenceBonus(self):
        return self.order.defenceBonus()
    
    def calculateSupport(self):
        if self.order.supporting:
            return self.order.support() +  self.calculateArmyStrength()
        else:
            return 0

    def calculateArmyStrength(self):
        strength = np.sum([unit.strength for unit in self.army]) 
    
    def findSeaNeighbours(self, player: Player, burnList: list[Region]) -> list[Region]:
        if self.allegiance != player:
            return []
        seas = [region for region in self.neighbours if region.isSea and region not in burnList]
        seaNeighbours = []
        for sea in seaNeighbours:
            seaNeighbours += sea.findSeaNeighbours(player, burnList+[self])
        return list(set([region for region in self.neighbours if not region.isSea] + seaNeighbours))

class Land(Region):
    def __init__(self, name:str, power=0, supply=0, isHome=False, muster=0, garrison=None):
        super().__init__(name, power=power, supply=supply)
        self.powerToken = False
        self.home = isHome
        self.isSea = False
        self.muster = muster #0 - regular land, 1 - castle, 2 - fortress
        if garrison:
            self.garrison = garrison
        if isHome:
            self.garrison = 2

class Sea(Region):
    def __init__(self, name):
        super().__init__(name)
        self.isSea = True
    

