from players import Player
from regions import Region
from typing import Optional


class Order:
    def __init__(self, player: Player, region: Optional[Region]=None):
        self.player = player
        self.region = region
        self.raidable = False

    def raidableStar(self):
        return self.raidable
    
    def place(self, region: Region):
        self.region = region
        region.order = self

    def execute(self):
        return []
    
    def executeTarget(self, region: Region):
        pass
    
    def remove(self):
        self.region.order = None
        self.region = None

    def raid(self):
        self.remove


class Stengthen(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
        self.raidable = True

    def execute(self):
        gain = self.region.power + 1
        self.player.power += max(gain, self.player.powerToGain)
        self.remove()
        return []
    
    def raid(self, raider: Player)

class Defend(Order):
    def __init__(self, player: Player, region=None):
        super().__init__(player, region)

    def raidableStar(self):
        return True

class Support(Order):
    def __init__(self, player: Player, region=None):
        super().__init__(player, region)
        self.raidable = True

class Raid(Order):
    def __init__(self, player: Player, region=None):
        super().__init__(player, region)
        self.raidable = True
    
    def execute(self):
        regions = [region.order.raidable or False for region in self.region.neighbours]
        raidable = self.region.neighbours if self.region.isSea else [not region.isSea for region in self.region.neighbours]
        return [region for region, condition in zip(self.region.neighbours, regions and raidable) if condition]

    def executeTarget(self, region: Region):
        region.raid(self.player)
        self.remove()

class Attack(Order):
    def __init__(self, player: Player, region: Optional[Region]=None):
        super().__init__(player, region)
    
    def execute(self):
        canGoTo = []
        if self.region.isSea:
