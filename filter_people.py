import requests
import pandas as pd
import time
import os

print("--- Starting filter_people.py script ---")

EDGE_FILE = 'edge-list.csv'
PEOPLE_LIST_FILE = 'people-list.txt'
FINAL_GRAPH_FILE = 'people-graph.csv'

def build_master_people_list():
    """
    This will take 10-20 minutes.
    """
    people = set()
    endpoint_url = "https://query.wikidata.org/sparql"
    
    query = """
    SELECT ?articleTitle WHERE {
      # ?item is a 'human'
      ?item wdt:P31 wd:Q5 .
      
      # ?sitelink is the article on simple.wiki
      ?sitelink schema:about ?item ;
                schema:isPartOf <https://simple.wikipedia.org/> ;
                schema:name ?articleTitle . 
    }
    """
    
    print("Running master query to find all people... This will take 10-20 minutes.")
    
    try:
        headers = {
            'Accept': 'application/sparql-results+json',
            'User-Agent': 'WikiPeopleProject/1.0 (contact@example.com)'
        }
        # Use POST for this large, complex query
        data = { 'query': query }
        
        r = requests.post(endpoint_url, data=data, headers=headers)
        r.raise_for_status() 
        data = r.json()
        
        results = data.get('results', {}).get('bindings', [])
        print(f"Master query complete. Found {len(results)} people.")
        
        for result in results:
            person_name = result.get('articleTitle', {}).get('value')
            if person_name:
                people.add(person_name)
        
        return list(people)

    except Exception as e:
        print(f"\n--- CRITICAL ERROR ---")
        print(f"Master query failed: {e}")
        print("------------------------\n")
        return None

# --- Main Script Logic ---

people_set = set()

if os.path.exists(PEOPLE_LIST_FILE):
    print("Found existing people list. Loading...")
    with open(PEOPLE_LIST_FILE, 'r', encoding='utf-8') as f:
        people_set = set(f.read().splitlines())
else:
    print("No people-list.txt found. Building it from Wikidata...")
    
    people_list = build_master_people_list()
    
    if people_list:
        people_set = set(people_list)
        print(f"Saving {len(people_set)} people to {PEOPLE_LIST_FILE}...")
        with open(PEOPLE_LIST_FILE, 'w', encoding='utf-8') as f:
            for person in people_set:
                f.write(f"{person}\n")
    
    else:
        print("Could not build people list. Exiting.")
        exit()

if not people_set:
    print("People list is empty. Exiting.")
    exit()

print(f"Loaded {len(people_set)} people.")

print(f"Loading {EDGE_FILE} again to filter...")
df_edges = pd.read_csv(EDGE_FILE, encoding='utf-8')

print(f"Filtering {EDGE_FILE} to keep only people-to-people links...")
df_people_edges = df_edges[
    df_edges['source'].isin(people_set) &
    df_edges['target'].isin(people_set)
]

print(f"Saving final graph with {len(df_people_edges)} links to {FINAL_GRAPH_FILE}...")
df_people_edges.to_csv(FINAL_GRAPH_FILE, index=False, encoding='utf-8')
print(f"All done! Final graph saved to {FINAL_GRAPH_FILE}.")