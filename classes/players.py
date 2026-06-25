import numpy as np
from orders import Order
from regions import Region
from utils import MAX_SUPPLY

class Player:
    def __init__(self):
        self.castleCount = 0
        self.power = 0
        self.orders: list[Order] = []
        self.regions: list[Region] = []
        self.ironThrone = 0
        self.levies = 0
        self.court = 0
        self.powerToGain = 20

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