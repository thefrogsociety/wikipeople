import pandas as pd
import networkx as nx
import json
import os

GRAPH_FILE = 'people-graph.csv'
JSON_OUTPUT_FILE = 'full_graph.json'
SIMPLE_WIKI_URL_PREFIX = "https://simple.wikipedia.org/wiki/"

print(f"Loading full graph from {GRAPH_FILE}...")
if not os.path.exists(GRAPH_FILE):
    print(f"Error: {GRAPH_FILE} not found. Please run filter_people.py first.")
    exit()

try:
    df = pd.read_csv(GRAPH_FILE, encoding='utf-8')
    if df.empty:
        print(f"Error: {GRAPH_FILE} is empty.")
        exit()
except Exception as e:
    print(f"Error reading {GRAPH_FILE}: {e}")
    exit()


print("Building NetworkX graph...")
# Create the full graph in NetworkX
G = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph())

print(f"Graph built with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")

print("Preparing JSON data...")
# Use NetworkX's node_link_data format, which includes nodes and links lists
# suitable for D3, but represents the *entire* graph.
# We add the URL here.
graph_data = nx.node_link_data(G)

# Add URL to each node
print("Adding Wikipedia URLs to nodes...")
for node_dict in graph_data.get('nodes', []):
    node_id = node_dict.get('id')
    if node_id:
        # Simple URL encoding: replace spaces with underscores
        encoded_title = node_id.replace(' ', '_')
        node_dict['url'] = SIMPLE_WIKI_URL_PREFIX + encoded_title


print(f"Saving full graph data to {JSON_OUTPUT_FILE}...")
try:
    with open(JSON_OUTPUT_FILE, 'w', encoding='utf-8') as f:
        # Use separators=(',', ':') for a more compact JSON file
        json.dump(graph_data, f, ensure_ascii=False, separators=(',', ':'))
except Exception as e:
    print(f"Error writing JSON file: {e}")
    exit()

print(f"All done. {JSON_OUTPUT_FILE} created successfully.")
print("You can now open index.html (make sure it's the updated version).")