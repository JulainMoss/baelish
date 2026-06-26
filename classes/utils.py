from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .regions import Region
    from .players import Player
    from .units import Unit
    from .orders import Order
import numpy as np

ARMY_LIMITS = [
    [2, 2],
    [3, 2],
    [3, 2, 2],
    [3, 2, 2, 2],
    [3, 3, 2, 2],
    [4, 3, 2, 2],
    [4, 3, 2, 2, 2]
]
MAX_SUPPLY = 6

FORTIFICATION = ["None", "Castle", "Fortress"]

def checkArmyLimit(armies: list[tuple[str, int]], armyLimit: list[int]) -> bool:
    armySizes = [army for (_, army) in armies]
    if len(armySizes) > len(armyLimit):
        return False
    else:
        for limit, army in zip(armyLimit, armySizes):
            if limit < army:
                return False
    return True

def countInitialBattleScore(defender: Player, attacker: Player, region: Region, attackingArmy: list[Unit], attackOrder: Order):
    defenderAllies = region.defenceBonus() # defence order bonus
    + np.sum([neighbour.calculateSupport() for neighbour in region.neighbours if neighbour.allegiance == defender])  # support from surrounding orders
    + (region.garrison if region.garrison else 0) # local garrison
    + region.calculateArmyStrength() # army strength

    attackerAllies = attackOrder.advantage # attack order bonus
    + np.sum([neighbour.calculateSupport() for neighbour in region.neighbours if neighbour.allegiance == attacker]) # support from surrounding orders
    + np.sum([unit.attackScore() for unit in attackingArmy]) # army strength

    return defenderAllies, attackerAllies
