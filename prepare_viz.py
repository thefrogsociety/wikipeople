import pandas as pd
import networkx as nx
import json

# --- SETTINGS ---
# Change this to any "hub" person
# (Make sure the name is exactly as it appeared in your analysis output)
ROOT_PERSON = "Donald Trump"
GRAPH_FILE = "people-graph.csv"
JSON_OUTPUT_FILE = "graph-viz.json"
# ----------------

print(f"Loading full graph from {GRAPH_FILE}...")
df = pd.read_csv(GRAPH_FILE, encoding='utf-8')

# Create the full graph in NetworkX
G = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph())

if ROOT_PERSON not in G:
    print(f"Error: '{ROOT_PERSON}' not found in the graph. Check your spelling.")
    print("Try one of these hubs instead:")
    print([node for node, degree in G.in_degree() if degree > 200])
    exit()

print(f"Found '{ROOT_PERSON}'. Finding all direct connections...")

# find all people who link TO the root person
predecessors = set(G.predecessors(ROOT_PERSON))
# find all people the root person links TO
successors = set(G.successors(ROOT_PERSON))

# Combine
neighbors = predecessors | successors
neighbors.add(ROOT_PERSON)

print(f"Found {len(neighbors) - 1} connections.")

subgraph = G.subgraph(neighbors)

print("Converting subgraph to D3.js format...")
d3_data = nx.node_link_data(subgraph)

# a "group" property to style the nodes
for node in d3_data["nodes"]:
    if node["id"] == ROOT_PERSON:
        node["group"] = "root"
    elif node["id"] in predecessors and node["id"] in successors:
        node["group"] = "both" # Links both ways
    elif node["id"] in predecessors:
        node["group"] = "links_to_root" # Links TO root
    else:
        node["group"] = "linked_from_root" # Linked FROM root

print(f"Saving data to {JSON_OUTPUT_FILE}...")
with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(d3_data, f)

print("All done. You are ready to open index.html!")
