import networkx as nx
import pandas as pd

GRAPH_FILE = 'people-graph.csv'

try:
    print(f"Loading graph from {GRAPH_FILE}...")
    df = pd.read_csv(GRAPH_FILE, encoding='utf-8')
except FileNotFoundError:
    print(f"Error: Could not find {GRAPH_FILE}.")
    exit()

if df.empty:
    print(f"Error: {GRAPH_FILE} is empty.")
    exit()

# create a directed graph (since links go one way)
G = nx.from_pandas_edgelist(df, 'source', 'target', create_using=nx.DiGraph())

print(f"--- WikiPeople Analysis ---")
print(f"Graph created with {G.number_of_nodes()} people and {G.number_of_edges()} links.")
print("---------------------------------")


print("Analyzing 'hub' people (most mentioned)...")

# check 'in_degree' (how many links point TO them)
hub_scores = dict(G.in_degree())
hub_scores = {person: score for person, score in hub_scores.items() if score > 0}
sorted_hubs = sorted(hub_scores.items(), key=lambda item: item[1], reverse=True)

print("\n--- Top 10 Hub People (Most Mentioned) ---")
for person, score in sorted_hubs[:10]:
    print(f"{person} (mentioned by {score} other people)")

print("---------------------------------")


print("Analyzing average connections...")

total_in_degree = sum(dict(G.in_degree()).values())
if G.number_of_nodes() > 0:
    avg_connection = total_in_degree / G.number_of_nodes()
    print(f"\nOn average, a 'person' article is mentioned by {avg_connection:.2f} other 'person' articles.")
else:
    print("\nCould not calculate average connections: No people found in graph.")
    
print("---------------------------------")


out_scores = dict(G.out_degree())
out_scores = {person: score for person, score in out_scores.items() if score > 0}
sorted_out = sorted(out_scores.items(), key=lambda item: item[1], reverse=True)

print("\n--- Top 10 Most 'Connected' People (Link OUT the most) ---")
for person, score in sorted_out[:10]:
    print(f"{person} (links to {score} other people)")