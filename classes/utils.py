import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .units import Unit

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

def checkArmyLimit(armies: list[list[Unit]], armyLimit: list[int]) -> bool:
    return np.all([limit >= army for limit, army in zip(armyLimit + [1]*(len(armies)-len(armyLimit)), sorted([len(army) for army in armies], reverse=True))])

def calculateAttackerStrength(army: list[Unit], region) -> int:
    return np.sum([unit.attackScore(region)for unit in army])

def calculateArmyStrength(army: list[Unit])->int:
    return np.sum([unit.strength for unit in army])
