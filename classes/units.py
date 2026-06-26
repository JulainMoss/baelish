from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .players import Player
    from .regions import Region

class Unit:
    def __init__(self, region: Region, allegiance: Player):
        self.region = region
        self.allegiance = allegiance
        self.strength = 0
        self.inRetreat = False
    
    def __str__(self):
        return "Unknown Unit"

    def canMoveTo(self, region: Region):
        return False

    def attackScore(self, region: Region):
        return self.strength

class LandUnit(Unit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)

    def __str__(self):
        return "Unknown Land Unit"

    def canMoveTo(self, region: Region):
        return not region.isSea

class Levy(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 1
    
    def __str__(self):
        return "Levy"
    
class Knight(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 2
    
    def __str__(self):
        return "Knight"

class Siege(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)

    def __str__(self):
        return "Siege Weapon"

    def attackScore(self, region: Region):
        if region.muster:
            return 4
        else:
            return 0

class Ship(Unit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 1
    
    def canMoveTo(self, region: Region):
        return region.isSea
    
    def __str__(self):
        return "Ship"