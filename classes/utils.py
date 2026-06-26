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

def checkArmyLimit(armies: list[tuple[str, list[Unit]]], armyLimit: list[int]) -> bool:
    armySizes = sorted([len(army) for (_, army) in armies if len(army) > 1], reverse=True)
    # print(armySizes)
    if len(armySizes) > len(armyLimit):
        return False
    else:
        for limit, army in zip(armyLimit, armySizes):
            # print(limit, army)
            if limit < army:
                return False
    return True

def calculateAttackerStrength(army: list[Unit], region) -> int:
    return np.sum([unit.attackScore(region)for unit in army])

def calculateArmyStrength(army: list[Unit])->int:
    return np.sum([unit.strength for unit in army])
