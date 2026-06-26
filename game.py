import json
from eng import engToPol
from classes.regions import Land, Sea, Region
from classes.orders import Order
from classes.players import Stark, Lannister, Baratheon, Targaryen, Tyrell, Greyjoy, Arryn, Martell

players = {"Stark": Stark(),
           "Lannister": Lannister(),
           "Targaryen": Targaryen(),
           "Greyjoy": Greyjoy(),
           "Tyrell": Tyrell(),
           "Arryn": Arryn(),
           "Baratheon": Baratheon(),
           "Martell": Martell()}

def mapSetUp():
    with open("./data/map.json", 'r', encoding='utf-8') as f:
        jsonData = json.load(f)
    regions = {}
    neighbours = []
    for region in jsonData:
        name = region['name']
        traits = region['traits'].keys()
        traitVals = region['traits']

        # print(name)
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

def playersSetUp(regions: dict[str, Region]):
    for player in players.values():
        player.setUp(regions)


def example():
    regions = mapSetUp()
    playersSetUp(regions)
    print(regions["Winterfell"])
    print(regions["Zatoka Żelaznych Ludzi"])