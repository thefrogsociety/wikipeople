# WikiPeople

A Python data pipeline that turns the entire Simple English Wikipedia into a "people-only" network graph, visualized interactively using D3.js. This project downloads and parses the full Wikipedia XML dump, queries the Wikidata SPARQL endpoint to identify all "person" articles, builds the graph data, and displays a dynamic, searchable network visualization in your browser.

The final web application allows you to search for any person in the dataset and see their mutual connections and the links between those connections.

# How It Works: The Data Pipeline & Visualization

## parse_wiki.py: 

Reads the multi-gigabyte simplewiki-latest-pages-articles-multistream.xml.bz2 dump. It parses the wikitext of every article to find all internal links, creating a massive edge-list.csv file (e.g., "Albert Einstein" -> "Germany").

## filter_people.py:

Runs one "master query" against the Wikidata SPARQL endpoint to get a complete list of all 77,000+ articles on Simple English Wikipedia that are an "instance of human."

Saves this master list to people-list.txt.

Filters the edge-list.csv to keep only the links that go from a person to another person, saving the result as people-graph.csv.

## create_full_json.py:

Reads the filtered people-graph.csv.

Converts the graph data (nodes and links) into a full_graph.json file, adding Simple English Wikipedia URLs to each person. This JSON format is optimized for loading into the web visualization.

## index.html:

A single-page web application using D3.js.

Loads the entire network graph from full_graph.json.

Provides a search bar to dynamically select a "root" person.

Calculates and displays the subgraph of mutually linked neighbors and the connections between them using a force-directed layout.

Allows dragging nodes, zooming/panning, viewing names, and double-clicking nodes to open their Wikipedia page.

## analyze.py (Optional):

Loads the people-graph.csv into networkx.

Runs a network analysis to find the "hub people" (highest in-degree) and the average number of connections, printing results to the terminal.

# Final Dataset Stats (from Simple English Wikipedia)

Total People Identified: 77,212

Total People-to-People Links: 91,509

(Analysis results from analyze.py can be added here if desired)

# How to Use

## Clone the repository:

git clone [https://github.com/your-username/wikipeople.git](https://github.com/your-username/wikipeople.git)
cd wikipeople

## Set up the environment:

python -m venv venv

## Activate the environment (use venv\Scripts\activate on Windows)

source venv/bin/activate 

## Install required libraries
pip install pandas networkx requests 

## Create requirements.txt (optional but good practice)
pip freeze > requirements.txt 


## Download the Data:

Download the Simple English Wikipedia dump.

Get the file named simplewiki-latest-pages-articles-multistream.xml.bz2.

Place it in the root of the wikipeople folder.

## Run the Data Pipeline:

### Parse the XML (Takes ~10-15 mins)
python parse_wiki.py

### Filter for people & create people-graph.csv (Takes ~10-20 mins, one time only)
python filter_people.py

### Create the JSON for the web app (Takes ~1 min)
python create_full_json.py 


## Run the Visualization:

### Start a simple web server from the wikipeople directory
python -m http.server 8000 

### Open your web browser and go to: http://localhost:8000

(The page will load full_graph.json, which might take a few seconds).

## Run Analysis:

### Get statistics about the network
python analyze.py 


# Core Technologies

Python 3

pandas: For handling the large CSV data.

networkx: For graph creation and analysis (used in analyze.py and create_full_json.py).

requests: For querying the Wikidata API.

Wikidata SPARQL: For database querying and data enrichment.

D3.js (v7): For the interactive web visualization.

HTML/CSS/JavaScript: For the web frontend.
