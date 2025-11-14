import bz2
import xml.etree.cElementTree as etree
import wikitextparser as wtp
import pandas as pd
import os

DUMP_FILE = 'simplewiki-latest-pages-articles-multistream.xml.bz2'
OUTPUT_FILE = 'edge-list.csv'

# keep track of links
edges = set()

print(f"Starting to parse {DUMP_FILE}...")
print("This will take several minutes. Please wait...")

with bz2.open(DUMP_FILE, 'r') as f:
    # use iterparse to read the file element by element
    for _, elem in etree.iterparse(f, events=('end',)):
        
        if elem.tag == '{http://www.mediawiki.org/xml/export-0.11/}page':
            
            title = elem.findtext('{http://www.mediawiki.org/xml/export-0.11/}title')
            
            wikitext = elem.findtext('.//{http://www.mediawiki.org/xml/export-0.11/}text')
            
            # make sure it's a real article
            if wikitext and title and not any(title.startswith(prefix) for prefix in ['User:', 'File:', 'Template:', 'Wikipedia:', 'Help:', 'Category:', 'Talk:']):
                
                try:
                    parsed = wtp.parse(wikitext)
                    
                    for link in parsed.wikilinks:
                        target_title = str(link.title).strip()
                        
                        # add this link (as a tuple) to our set
                        if target_title:
                            edges.add((title, target_title))
                            
                except Exception as e:
                    pass
            
            # clear to keep RAM low
            elem.clear()

print(f"\nParsing complete. Found {len(edges)} unique links.")
print(f"Saving links to {OUTPUT_FILE}...")

df = pd.DataFrame(list(edges), columns=['source', 'target'])
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8')

print(f"All done. Data saved to {OUTPUT_FILE}.")