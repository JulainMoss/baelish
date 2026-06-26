from typing import TYPE_CHECKING
import numpy as np

from .utils import calculateArmyStrength, calculateAttackerStrength

if TYPE_CHECKING:
    from .players import Player
    from .regions import Region
    from .units import Unit
    from .orders import Order

def countInitialBattleScore(defender: Player, attacker: Player, region: Region, attackingArmy: list[Unit], attackOrder: Order):
    defenderAllies = region.defenceBonus() # defence order bonus
    + (region.garrison if region.garrison else 0) # local garrison
    + region.calculateArmyStrength() # army strength

    attackerAllies = attackOrder.advantage # attack order bonus
    + np.sum([neighbour.calculateSupport() for neighbour in region.neighbours if neighbour.player == attacker]) # support from surrounding orders
    + np.sum([unit.attackScore() for unit in attackingArmy]) # army strength

    return defenderAllies, attackerAllies


class Battle:
    def __init__(self, defender: Player, attacker: Player, attackingArmy: list[Unit], battleRegion: Region, attackerRegion: Region, attackOrder: Order):
        self.defender = defender
        self.attacker = attacker
        self.battleRegion = battleRegion
        self.attackerRegion = attackerRegion
        
        self.attackingArmy = attackingArmy
        self.defendingArmy: list[Unit] = battleRegion.army
        
        self.attackOrder = attackOrder
        self.defenderOrder: Order = battleRegion.order
        self.callSupport()
        self.countInitialScore()


    def countInitialScore(self):
        self.defenceSupport = [neighbour.calculateSupport(self.defender, self.attacker, self.region) for neighbour in self.region.neighbours]
        self.defenceSupportStrength = np.sum([calculateArmyStrength(army) for (_, army) in self.defenceSupport])
        
        self.defenderStrength = self.defenceSupportStrength  # support
        + (self.battleRegion.garrison if self.battleRegion.garrison else 0) # garrison
        + calculateArmyStrength(self.defendingArmy) # defending army
        + (self.defenderOrder.defence) # order bonus

        self.attackSupport = [neighbour.calculateSupport(self.attacker, self.defender, self.region) for neighbour in self.region.neighbours]
        self.attackSupportStrength = np.sum([calculateAttackerStrength(army)for (_, army) in self.attackSupport])
        
        self.attackerStrength = self.attackSupportStrength
        + calculateAttackerStrength(self.attackingArmy, self.battleRegion)
        + self.attackOrder.advantage

    