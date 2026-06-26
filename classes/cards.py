from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .players import Player

class HouseCard:
    def __init__(self, player: Player):
        self.strength = 0
        self.swords = 0
        self.towers = 0
        self.player = player
        self.inHand = True
    
    def useInBattle(self, battle):
        self.inHand = False

    def ability(self, battle):
        pass