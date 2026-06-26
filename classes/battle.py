from typing import TYPE_CHECKING
import numpy as np

if TYPE_CHECKING:
    from .players import Player
    from .regions import Region
    from .units import Unit
    from .orders import Order

def countInitialBattleScore(defender: Player, attacker: Player, region: Region, attackingArmy: list[Unit], attackOrder: Order):
    defenderAllies = region.defenceBonus() # defence order bonus
    + np.sum([neighbour.calculateSupport() for neighbour in region.neighbours if neighbour.player == defender])  # support from surrounding orders
    + (region.garrison if region.garrison else 0) # local garrison
    + region.calculateArmyStrength() # army strength

    attackerAllies = attackOrder.advantage # attack order bonus
    + np.sum([neighbour.calculateSupport() for neighbour in region.neighbours if neighbour.player == attacker]) # support from surrounding orders
    + np.sum([unit.attackScore() for unit in attackingArmy]) # army strength

    return defenderAllies, attackerAllies