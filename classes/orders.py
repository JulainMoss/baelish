###TODO: StrengthenStar, Attack.executeTarget

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .players import Player
    from .regions import Region
from .units import Unit
from .utils import ARMY_LIMITS, checkArmyLimit



class Order:
    def __init__(self, player: Player, region: Optional[Region]=None):
        self.name: str = ""
        self.player = player
        if region:
            self.place(region)
        self.raidable = False
        self.raidableStar = False
        self.advantage = 0
        self.courtCost = 0
        self.supporting = False
        self.support = 0
        self.defence = 0

    def __str__(self):
        return self.name

    def place(self, region: Region):
        self.region = region
        region.order = self

    def execute(self) -> list[Region]:
        return []
    
    def executeTarget(self, region: Region):
        print(f"Exeecuting order {self} at {region.name}")
    
    def remove(self):
        print(f"Removing order {self} from {self.region.name}")
        self.region.order = None
        self.region = None

    def raid(self, player: Player):
        print(f"Order {self} raided by {str(player)}")
        self.remove()

class OrderStar():
    def __init__(self):
        self.courtCost = True


class Strengthen(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.name = "Strengthen"
        self.raidable = True
        self.raidableStar = True

    def execute(self) -> list[Region]:
        return [self.region] if self.region.canStrengthen() else []

    def executeTarget(self, region):
        gain = region.power + 1
        toGain = min(gain, self.player.powerToGain)
        self.player.power += toGain 
        self.player.powerToGain -= toGain 
        self.remove()
    
    def raid(self, raider: Player):
        self.player.power = max(0, self.player.power - 1)
        raider.power += 1 if raider.powerToGain else 0
        raider.powerToGain = max(0, raider.powerToGain - 1)
        super().raid(raider)


class Defend(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.name = "Defend"
        self.raidableStar = True
        self.defence = 1
    
class DefendStar(Order, OrderStar):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.defence = 2


class Support(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.name = "Support"
        self.raidable = True
        self.raidableStar = True
        self.supporting = True


class SupportStar(Support, OrderStar):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.support = 1


class Raid(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.name = "Raid"
        self.raidable = True
        self.raidable
    
    def execute(self) -> list[Region]:
        raidable = [region.order.raidable if region.order and region.player is not self.player else False for region in self.region.neighbours]
        available = [True for _ in self.region.neighbours] if self.region.isSea else [not region.isSea for region in self.region.neighbours]
        conditions = [r and a for (r, a) in zip(raidable, available)]
        return [region for region, condition in zip(self.region.neighbours, conditions) if condition]

    def executeTarget(self, region: Region):
        region.raid(self.player)
        self.remove()

class RaidStar(Raid, OrderStar):
    def __init__(self, player, region: Optional[Region]=None):
        super().__init__(player, region)

    def execute(self) -> list[Region ]:
        raidable = [region.order.raidableStar if region.order and region.player is not self.player else False for region in self.region.neighbours]
        available = self.region.neighbours if self.region.isSea else [not region.isSea for region in self.region.neighbours]
        conditions = [r and a for (r, a) in zip(raidable, available)]
        return [region for region, condition in zip(self.region.neighbours, conditions) if condition]


class Attack(Order):
    def __init__(self, player: Player, region: Optional[Region]=None, advantage=0):
        super().__init__(player, region)
        self.advantage = advantage
    
    # def _(self, unitToMove: Unit) -> list[Region]:
    #     self.execute([unitToMove])

    def execute(self, unitsToMove: list[Unit]) -> list[Region]:
        if isinstance(unitsToMove, Unit):
            unitsToMove = [unitsToMove]
        countToMove = len(unitsToMove)
        armies = self.player.armies()
        supplies = self.player.countSupply()
        maxArmy = ARMY_LIMITS[supplies]
        # 1: defining regions neighbouring order where units can be moved
        possibilities = self.region.findSeaNeighbours(self.player) if not self.region.isSea else [region for region in self.region.neighbours if region.isSea]
        if self.region in possibilities:
            possibilities.remove(self.region)
        
        # print([p.name for p in possibilities])
        # 2: checking possibilities meeting supply limit

        possibleFutureArmies = [(region, sorted(
            [(name, army + unitsToMove) if name == region.name else (name, army) for (name, army) in armies]
            , reverse=True
        ))
        for region in possibilities]

        return [region for (region, armies) in possibleFutureArmies if checkArmyLimit(armies, maxArmy)]


    def executeTarget(self, region: Region):
        pass

class AttackStar(Attack, OrderStar):
    def __init__(self, player, region = None):
        super().__init__(player, region, advantage=1)
        self.advantage = 1