🕸️ WikiPeople

A Python data pipeline that turns the entire Simple English Wikipedia into a "people-only" network graph. This project downloads and parses the full Simple English Wikipedia XML dump, queries the Wikidata SPARQL endpoint to identify all "person" articles, and builds a graph to analyze the connections between them.

The final analysis finds the most-connected "hubs" in the encyclopedia and the average number of connections per person.

🚀 How It Works: The Data Pipeline

parse_wiki.py: Reads the multi-gigabyte simplewiki-latest-pages-articles-multistream.xml.bz2 dump. It parses the wikitext of every article to find all internal links, creating a massive edge-list.csv file (e.g., "Albert Einstein" -> "Germany"). (~10-15 mins runtime).

filter_people.py:

Runs one "master query" against the Wikidata SPARQL endpoint to get a complete list of all articles on Simple English Wikipedia that are an "instance of human." (~10-20 mins runtime, one time only).

Saves this master list to people-list.txt.

Filters the edge-list.csv to keep only the links that go from a person to another person, saving the result as people-graph.csv. (Quick).

analyze.py:

Loads the final people-graph.csv into a networkx directed graph.

Runs a network analysis to find the "hub people" (highest in-degree), the most "connected" people (highest out-degree), and the average number of connections. (Quick).

prepare_viz_data.py:

Loads people-graph.csv.

Creates a small JSON file (graph-viz.json) containing a specified root person and their direct connections, formatted for D3.js. (Quick).

index.html:

A webpage that loads graph-viz.json and displays an interactive, force-directed graph using D3.js. Allows zooming, panning, dragging nodes, and viewing names on hover.

📊 Final Analysis Results (Simple English Wikipedia)

Total People Identified: 77,212

Total People-to-People Links: 91,509

Top 10 Hub People (Most Mentioned):

Donald Trump (mentioned by 590 other people)

Barack Obama (mentioned by 476 other people)

Elizabeth II (mentioned by 442 other people)

Ronald Reagan (mentioned by 391 other people)

George W. Bush (mentioned by 351 other people)

Bill Clinton (mentioned by 326 other people)

Joe Biden (mentioned by 299 other people)

Jimmy Carter (mentioned by 203 other people)

Richard Nixon (mentioned by 196 other people)

George H. W. Bush (mentioned by 178 other people)

Average Connections:

On average, a 'person' article is mentioned by 2.50 other 'person' articles.

Top 10 Most 'Connected' People (Link OUT the most):

John Wayne (links to 140 other people)

Bernie Sanders (links to 113 other people)

Christopher Plummer (links to 99 other people)

Ronald Reagan (links to 97 other people)

CM Punk (links to 92 other people)

Donald Trump (links to 81 other people)

Jimmy Carter (links to 66 other people)

Hans Zimmer (links to 64 other people)

DJ Khaled (links to 59 other people)

Nicholas Hoult (links to 58 other people)

Note on Link Counts: These numbers are based only on the Simple English Wikipedia and only count links pointing directly to other people identified by Wikidata. Links to movies, places, concepts, or articles not classified as 'human' are excluded. This explains why the "links out" count might seem lower than expected compared to the full English Wikipedia.

🛠️ How to Use

Clone the repository:

git clone [https://github.com/YourUsername/wikipeople.git](https://github.com/YourUsername/wikipeople.git)
cd wikipeople


Set up the environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
# Create requirements.txt first: pip freeze > requirements.txt
pip install -r requirements.txt 


Download the Data:

Download the Simple English Wikipedia dump.

Get the file named simplewiki-latest-pages-articles-multistream.xml.bz2.

Place it in the root of the wikipeople folder.

Run the Pipeline:

# 1. Parse the XML (Takes ~10-15 mins)
python parse_wiki.py

# 2. Build the master people list (Takes ~10-20 mins, one time only)
#    and filter the links (Quick)
python filter_people.py

# 3. Get the analysis results (Quick)
python analyze.py


Run the Visualization:

# 1. Prepare data for one person (e.g., Donald Trump, Quick)
python prepare_viz_data.py 

# 2. Start a local web server
python -m http.server

# 3. Open your browser to http://localhost:8000


(Press Ctrl+C in the terminal to stop the server)

Important: The large data files (edge-list.csv, people-list.txt, people-graph.csv, graph-viz.json) and the original dump file are not included in this repository due to their size. You must run the Python scripts to generate them.

⚙️ Core Technologies

Python 3

pandas: For handling the large CSV data.

networkx: For graph creation and analysis.

wikitextparser: For parsing the raw Wikipedia text.

Wikidata SPARQL: For database querying and data enrichment via API.

D3.js (v7): For interactive, browser-based graph visualization.

Tailwind CSS: For basic styling of the visualization page.
