# 🕸️ WikiPeople

A Python data pipeline that turns the entire Simple English Wikipedia into a "people-only" network graph. My project downloads and parses the full Wikipedia XML dump, queries the Wikidata SPARQL endpoint to identify all "person" articles, and builds a graph to analyze the connections between them.

The final analysis finds the most-connected "hubs" in the encyclopedia and the average number of connections per person.

---

## How It Works: The Data Pipeline

1.  **`parse_wiki.py`**: Reads the multi-gigabyte `simplewiki-latest-pages-articles-multistream.xml.bz2` dump. It parses the wikitext of every article to find all internal links, creating a massive `edge-list.csv` file (e.g., "Albert Einstein" -> "Germany").

2.  **`filter_people.py`**:
    * Runs one "master query" against the Wikidata SPARQL endpoint to get a complete list of all 77,000+ articles on Simple English Wikipedia that are an "instance of human."
    * Saves this master list to `people-list.txt`.
    * Filters the `edge-list.csv` to keep only the links that go from a person to another person, saving the result as `people-graph.csv`.

3.  **`analyze.py`**:
    * Loads the final `people-graph.csv` into a `networkx` directed graph.
    * Runs a network analysis to find the "hub people" (highest in-degree) and the average number of connections.

---

## 📊 Final Analysis Results

* **Total People Identified:** 77,212
* **Total People-to-People Links:** 91,509

*(You can paste the output of your `analyze.py` script here to show the Top 10 hubs!)*

---

## 🛠️ How to Use

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/wikipeople.git](https://github.com/your-username/wikipeople.git)
    cd wikipeople
    ```

2.  **Set up the environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate 
    pip install -r requirements.txt 
    ```
    *(**Note:** You'll need to create a `requirements.txt` file by running `pip freeze > requirements.txt`)*

3.  **Download the Data:**
    * Download the [Simple English Wikipedia dump](https://dumps.wikimedia.org/simplewiki/latest/).
    * Get the file named `simplewiki-latest-pages-articles-multistream.xml.bz2`.
    * Place it in the root of the `wikipeople` folder.

4.  **Run the Pipeline:**
    ```bash
    # 1. Parse the XML (Takes ~10-15 mins)
    python parse_wiki.py

    # 2. Filter for people (Takes ~10-20 mins, one time only)
    python filter_people.py

    # 3. Get your answers! (Takes ~2 seconds)
    python analyze.py
    ```

## ⚙️ Core Technologies
* **Python 3**
* **`pandas`**: For handling the large CSV data.
* **`networkx`**: For graph creation and analysis.
* **`wikitextparser`**: For parsing the raw Wikipedia text.
* **Wikidata SPARQL**: For database querying and data enrichment.
