from __future__ import annotations
import numpy as np
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .units import Unit
    from .players import Player
    from .orders import Order

from .utils import FORTIFICATION

class Region:
    def __init__(self, name: str, power=0, supply=0, ):
        self.name = name
        self.player: Player = None

        self.power = power
        self.supply = supply

        self.order: Order = None
        self.army: list[Unit] = []
        self.neighbours: list[Region] = []
        self.garrison = None
        

    def __str__(self):
        neighbourNames: list[str] = [neighbour.name for neighbour in self.neighbours]
        order = [f"Current order: {self.order}"] if self.order else []
        armies = [f"Army: {", ".join([str(unit) for unit in self.army])}"] if self.army else []
        desc = "\n".join([self.name]+[f"Belongs to: {self.player}"]+order+[f"Neighbours: {neighbourNames}"]+armies)
        return desc

    def addArmy(self, unit: Unit):
        self.army.append(unit)
        self.player = unit.player

    def canStrengthen(self):
        return False

    def changePlayer(self, player: Player):
        self.player = player

    def addNeighbour(self, neighbour: Region):
        self.neighbours.append(neighbour)

    def setUpBorders(self, neighbours: list[Region]):
        self.neighbours = neighbours
    
    def raid(self, player: Player):
        self.order.raid(player)

    def defenceBonus(self):
        return self.order.defenceBonus()
    
    def calculateSupport(self, region: Region) -> int:
        if self.order.supporting and (self.isSea or not region.isSea):
            return self.order.support() +  self.calculateArmyStrength()
        else:
            return 0

    def calculateArmyStrength(self):
        strength = np.sum([unit.strength for unit in self.army]) 

    def calculateAttackStrength(self):
        strength = np.sum([unit.attackScore() for unit in self.army]) 

    def findSeaNeighbours(self, player: Player, burnList: Optional[list[Region]]=[]) -> list[Region]:
        if self.player != player:
            return []
        seas = [region for region in self.neighbours if region.isSea and region not in burnList]
        seaNeighbours = []
        for sea in seas:
            seaNeighbours += sea.findSeaNeighbours(player, burnList+[self])
        return list(set([region for region in self.neighbours if not region.isSea] + seaNeighbours))

class Land(Region):
    def __init__(self, name:str, power=0, supply=0, isHouse=False, muster=0, garrison=None, port=False):
        super().__init__(name, power, supply)
        self.powerToken = False
        self.isHouse = isHouse
        self.isSea = False
        self.muster = muster #0 - regular land, 1 - castle, 2 - fortress

        self.port = port
        if garrison:
            self.garrison = garrison
        if isHouse:
            self.garrison = 2
    
    def canStrengthen(self):
        return True
    
    def __str__(self):
        desc = super().__str__()
        fullDesc = [
            desc,
            f"Fortification: {FORTIFICATION[self.muster]}"
        ]
        fullDesc += [f"power: {self.power}"] if self.power else [] 
        fullDesc += [f"supply: {self.supply}"] if self.supply else [] 
        fullDesc += [f"Garrison Strength: {self.garrison}"] if self.garrison else []
        fullDesc += ["Region has Port"] if self.port else []
        return "\n".join(fullDesc)
        

class Sea(Region):
    def __init__(self, name):
        super().__init__(name)
        self.isSea = True

    def __str__(self):
        desc = super().__str__()
        return "\n".join([desc]+["Sea region"])

