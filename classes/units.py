from players import Player
from regions import Region

class Unit:
    def __init__(self, region: Region, allegiance: Player):
        self.region = region
        self.allegiance = allegiance
        self.strength = 0
    
    def canMoveTo(self, region: Region):
        return False

    def attackScore(self, region: Region):
        return self.strength

class LandUnit(Unit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)

    def canMoveTo(self, region: Region):
        return not region.isSea

class Levy(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 1
    
class Knight(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 2

class Siege(LandUnit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)

    def battleScore(self, region: Region):
        if region.muster:
            return 4

class Ship(Unit):
    def __init__(self, region: Region, allegiance: Player):
        super().__init__(region, allegiance)
        self.strength = 1
    
    def canMoveTo(self, region: Region):
        return region.isSea