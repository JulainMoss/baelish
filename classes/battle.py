from typing import TYPE_CHECKING, Optional
import numpy as np
import asyncio

from .utils import calculateArmyStrength, calculateAttackerStrength

if TYPE_CHECKING:
    from .players import Player
    from .regions import Region
    from .units import Unit
    from .orders import Order
    from .cards import HouseCard, BattlePhase


class Battle:
    def __init__(self, attacker: Player, defender: Player, attackingArmy: list[Unit], battleRegion: Region, attackerRegion: Region, attackOrder: Order):
        self.defender = defender
        self.attacker = attacker
        self.battleRegion = battleRegion
        self.attackerRegion = attackerRegion
        
        self.attackingArmy = attackingArmy
        self.defendingArmy: list[Unit] = battleRegion.army

        
        
        self.attackOrder = attackOrder
        self.defenderOrder: Order = battleRegion.order
        
        self.countInitialScore()
        
        self.attackerCard: HouseCard = self.attacker.chooseCard(self)
        self.defenderCard: HouseCard = self.defender.chooseCard(self)

        if self.defenderCard.useNow:
            self.defenderCard.ability(self)
        
        if self.attackerCard.useNow:
            self.attackerCard.ability(self)

        defender.useValyrianSword(self)
        attacker.useValyrianSword(self)

        if self.defenderStrength > self.attackerStrength or (self.defenderStrength == self.attackerStrength and defender.levies < attacker.levies):
            # defender won the battle
            # use cards abilities
            # execute or save units
            # retreat
            # update regions
            pass
        else:
            # attacker won
            pass
            


    def countInitialScore(self):
        self.defenceSupport = [neighbour.calculateSupport(self.defender, self.attacker, self.region) for neighbour in self.region.neighbours]
        self.defenceSupportStrength = np.sum([calculateArmyStrength(army) for (_, army) in self.defenceSupport])
        
        self.defenderStrength = (
                                self.defenceSupportStrength  
                                + (self.battleRegion.garrison if self.battleRegion.garrison else 0) 
                                + calculateArmyStrength(self.defendingArmy) 
                                + (self.defenderOrder.defence)
        ) 

        self.attackSupport = [neighbour.calculateSupport(self.attacker, self.defender, self.region) for neighbour in self.region.neighbours]
        self.attackSupportStrength = np.sum([calculateAttackerStrength(army)for (_, army) in self.attackSupport])
        
        self.attackerStrength = (
                                self.attackSupportStrength
                                + calculateAttackerStrength(self.attackingArmy, self.battleRegion)
                                + self.attackOrder.advantage
        )

        return self.attackerStrength, self.defenderStrength
    


def operateBattle(attacker: Player, defender: Player, attackingArmy: list[Unit], battleRegion: Region, attackerRegion: Region, attackOrder: Order):
    currentBattle = Battle(attacker, defender, attackingArmy, battleRegion, attackerRegion, attackOrder)
    scores = currentBattle.countInitialScore()