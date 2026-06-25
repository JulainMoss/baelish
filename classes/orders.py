from players import Player
from units import Unit
from regions import Region
from typing import Optional
from utils import ARMY_LIMITS, checkArmyLimit


class Order:
    def __init__(self, player: Player, region: Optional[Region]=None):
        self.player = player
        self.region = region
        self.raidable = False

    def raidableStar(self) -> bool:
        return self.raidable
    
    def place(self, region: Region):
        self.region = region
        region.order = self

    def defenceBonus(self)-> int:
        return 0

    def execute(self) -> list[Region]:
        return []
    
    def executeTarget(self, region: Region):
        pass

    def supporting(self) -> bool:
        return False
    
    def support(self) -> int:
        return 0
    
    def remove(self):
        self.region.order = None
        self.region = None

    def raid(self):
        self.remove


class Stengthen(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.raidable = True

    def execute(self) -> list[Region]:
        gain = self.region.power + 1
        self.player.power += max(gain, self.player.powerToGain)
        self.remove()
        return []
    
    def raid(self, raider: Player):
        self.player.power = max(0, self.player.power - 1)
        raider.power += 1 if raider.powerToGain else 0
        raider.powerToGain = max(0, raider.powerToGain - 1)
        super().raid()

class Defend(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)

    def raidableStar(self) -> bool:
        return True
    
    def defenceBonus(self) -> int:
        return 1
    
class DefendStar(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
    
    def defenceBonus(self) -> int:
        return 2

class Support(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.raidable = True

    def support(self):
        return 0
    
    def supporting(self):
        return True

class SupportStar(Support):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)

    def support(self):
        return 1

class Raid(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.raidable = True
    
    def execute(self) -> list[Region]:
        regions = [region.order.raidable or False for region in self.region.neighbours]
        raidable = self.region.neighbours if self.region.isSea else [not region.isSea for region in self.region.neighbours]
        return [region for region, condition in zip(self.region.neighbours, regions and raidable) if condition]

    def executeTarget(self, region: Region):
        region.raid(self.player)
        self.remove()

class Attack(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
    
    def execute(self, unitsToMove: list[Unit]) -> list[Region]:
        countToMove = len(unitsToMove)
        armies = self.player.armies()
        supplies = self.player.countSupply()
        maxArmy = ARMY_LIMITS[supplies]
        # 1: defining regions neighbouring order where units can be moved
        possibilities = self.region.findSeaNeighbours(self.player) if not self.region.isSea else [region for region in self.region.neighbours if region.isSea]

        # 2: checking possibilities meeting supply limit

        possibleFutureArmies = [(region, sorted(
            [(name, army + countToMove) if name == region.name else (name, army) for (name, army) in armies]
            , reverse=True
        ))
        for region in possibilities]

        return [region for (region, armies) in possibleFutureArmies if checkArmyLimit(armies, maxArmy)]
    
    def executeTarget(self, region: Region):
        pass
        