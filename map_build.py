import json
import argparse

argparse = argparse.ArgumentParser(description='Build a map from a JSON file.')
argparse.add_argument('json_file', type=str, help='Path to the JSON file containing the map data.')
argparse.add_argument('output', type=str, help='')
args = argparse.parse_args()

nodes = []
edges = []

with open(args.json_file, 'r', encoding='utf-8') as f:
    map_data = json.load(f)
    nodes = map_data["nodes"]
    edges = map_data["edges"]
regions = []
for node in nodes:
    region = {"name": node["name"], "traits": {}, "borders": []}
    for trait in node["traits"]:
        region["traits"][trait["name"]] = trait["value"]
    regions.append(region)

# regions = [
#     {"name": node["name"],
#      "traits": [{trait["name"] : trait["value"]} for trait in node["traits"]]
#     }for node in nodes]
for edge in edges:
    regions[edge["i"]]["borders"].append(regions[edge["j"]]["name"])
    regions[edge["j"]]["borders"].append(regions[edge["i"]]["name"])

with open(args.output, 'w', encoding='utf-8') as f:
    json.dump(regions, f, indent=3, ensure_ascii=True)