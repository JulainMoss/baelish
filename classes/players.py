import numpy as np

class Player:
    def __init__(self):
        self.castleCount = 0
        self.supply = 0
        self.power = 0
        self.orders = []
        self.regions = []
        self.ironThrone = 0
        self.levies = 0
        self.court = 0
        self.powerToGain = 20

    def countCrowns(self):
        return np.sum([region.power for region in self.regions])
    
    def countSupply(self):
        return np.sum([region.supply for region in self.regions])