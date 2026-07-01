import os
import glob
import json
import re

def parse_markdown_tables(directory):
    catalog = {}
    
    # Iterate through all md files
    for filepath in glob.glob(os.path.join(directory, "*.md")):
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
            for line in lines:
                line = line.strip()
                if line.startswith('|') and line.endswith('|'):
                    parts = [p.strip() for p in line.strip('|').split('|')]
                    # Expecting at least 7 parts (for the 7 columns)
                    if len(parts) >= 7 and parts[1].lower() != 'name' and not parts[1].startswith('---'):
                        name = parts[1]
                        test_type = parts[2]
                        keys = parts[3]
                        duration = parts[4]
                        languages = parts[5]
                        url_raw = parts[6]
                        
                        # Clean up URL (extract from <url> or [text](url))
                        url_match = re.search(r'<(https?://[^>]+)>', url_raw)
                        if url_match:
                            url = url_match.group(1)
                        else:
                            url_match2 = re.search(r'\[.*?\]\((https?://[^)]+)\)', url_raw)
                            url = url_match2.group(1) if url_match2 else url_raw
                        
                        # Add to catalog, keyed by URL to deduplicate
                        if url not in catalog:
                            catalog[url] = {
                                "name": name,
                                "test_type": test_type,
                                "keys": keys,
                                "duration": duration,
                                "languages": languages,
                                "url": url
                            }
                            
    return list(catalog.values())

if __name__ == "__main__":
    src_dir = r"C:\Users\91807\Downloads\sample_conversations\GenAI_SampleConversations"
    dest_file = os.path.join(os.path.dirname(__file__), "catalog.json")
    
    data = parse_markdown_tables(src_dir)
    print(f"Extracted {len(data)} unique items.")
    
    with open(dest_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
