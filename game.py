import json
from eng import engToPol
from classes.regions import Land, Sea, Region
from classes.orders import Order, Attack
from classes.units import Ship, Levy
from classes.players import Stark, Lannister, Baratheon, Targaryen, Tyrell, Greyjoy, Arryn, Martell
from classes.utils import ARMY_LIMITS

players = {"Stark": Stark(),
           "Lannister": Lannister(),
           "Targaryen": Targaryen(),
           "Greyjoy": Greyjoy(),
           "Tyrell": Tyrell(),
           "Arryn": Arryn(),
           "Baratheon": Baratheon(),
           "Martell": Martell()}

def mapSetUp()->list[Region]:
    with open("./data/map.json", 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    regions = {}
    neighbours = []
    for region in jsonData:
        name = region['name']
        traits = region['traits'].keys()
        traitVals = region['traits']

        if engToPol["sea"] in traits:
            item = Sea(name)
        else:
            (isHouse, owner) = (True, players[traitVals[engToPol["house"]]]) if engToPol['house'] in traits else (False, None)
            power = int(traitVals[engToPol["power"]]) if engToPol["power"] in traits else 0
            supply = int(traitVals[engToPol["supply"]]) if  engToPol["supply"] in traits else 0
            muster = int(traitVals[engToPol['muster']]) if engToPol["muster"] in traits else 0
            hasPort = True if engToPol["port"] in traits else False
            item = Land(name, power, supply, isHouse=isHouse, muster=muster, port=hasPort)
            item.changeAllegiance(owner)
        regions[name] = item
        neighbours.append((name, region["borders"]))

    for name, neighbourList in neighbours:
        for neighbour in neighbourList:
            regions[name].addNeighbour(regions[neighbour])
    return regions

def playersSetUpWMap(regions: dict[str, Region]):
    for player in players.values():
        player.setUp(regions)

def playersSetUp()->list[Region]:
    regions = mapSetUp()
    playersSetUpWMap(regions)
    return regions


def example():
    regions: list[Region] = playersSetUp()
    greyjoy: Greyjoy = players["Greyjoy"]
    sup = greyjoy.countSupply()
    
    # print([(r.name, len(r.army), str(r.allegiance)) for r in greyjoy.regions])
    _ = Levy(regions["Palec Flinta"], greyjoy)
    _ = Levy(regions["Palec Flinta"], greyjoy)
    # print([(r.name, len(r.army)) for r in greyjoy.regions])
    print([r.name for r in regions["Strażnica n. Szarą Wodą"].findSeaNeighbours(greyjoy)])
    attackOrder = Attack(greyjoy, regions["Strażnica n. Szarą Wodą"])
    print([r.name for r in attackOrder.execute(regions["Strażnica n. Szarą Wodą"].army[0])])

    

if __name__ == "__main__":
    example()