import json
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

BASE_URL = 'https://www.shl.com'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def fetch_details(url):
    # get the page for a specific test
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # get description
        desc = ""
        meta = soup.find('meta', attrs={'name': 'description'})
        if meta and meta.get('content'):
            desc = meta['content'].strip()
                
        skills = []
        job_levels = []
        
        text = soup.get_text(separator=' ', strip=True).lower()
        
        # guess job level from text
        if 'entry level' in text or 'graduate' in text:
            job_levels.append('Entry')
        if 'professional' in text or 'mid-level' in text:
            job_levels.append('Professional')
        if 'manager' in text:
            job_levels.append('Manager')
        if 'executive' in text:
            job_levels.append('Executive')
            
        # remove duplicates
        job_levels = list(set(job_levels))
            
        # guess skills measured
        for h in soup.find_all(['h2', 'h3', 'h4', 'strong']):
            h_text = h.get_text(strip=True).lower()
            if 'skills measured' in h_text or 'what it measures' in h_text:
                sibling = h.find_next_sibling(['ul', 'p'])
                if sibling:
                    if sibling.name == 'ul':
                        for li in sibling.find_all('li'):
                            skills.append(li.get_text(strip=True))
                    else:
                        skills.append(sibling.get_text(strip=True))
                    break

        return desc, skills, job_levels
    except Exception as e:
        print("error getting details:", e)
        return "", [], []

def main():
    tests = []
    start = 0
    
    print("scraping catalog...")
    
    while True:
        url = f"https://www.shl.com/products/product-catalog/?start={start}"
        res = requests.get(url, headers=HEADERS)
        
        if res.status_code != 200:
            break
            
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # find Individual Test Solutions table
        th = soup.find('th', string=lambda text: text and 'Individual Test Solutions' in text)
        if not th:
            break
            
        table = th.find_parent('table')
        rows = table.find_all('tr')
        
        data_rows = []
        for r in rows:
            if r.find('td'):
                data_rows.append(r)
        
        if len(data_rows) == 0:
            break
            
        for row in data_rows:
            cells = row.find_all(['td', 'th'])
            if cells[0].name == 'th':
                continue
                
            a_tag = cells[0].find('a')
            if not a_tag:
                continue
                
            name = a_tag.text.strip()
            href = a_tag.get('href')
            if href.startswith('/'):
                href = BASE_URL + href
            
            test_type = ""
            if len(cells) > 3:
                test_type = cells[3].text.strip()
            
            tests.append({
                'name': name,
                'url': href,
                'test_type': test_type,
                'description': '',
                'skills': [],
                'job_levels': []
            })
            
        start += 12

    print(f"found {len(tests)} tests. getting details...")
    
    # use threads to make it faster
    with ThreadPoolExecutor(max_workers=5) as pool:
        futures = []
        for t in tests:
            futures.append(pool.submit(fetch_details, t['url']))
            
        for i, future in enumerate(futures):
            desc, skills, levels = future.result()
            tests[i]['description'] = desc
            tests[i]['skills'] = skills
            tests[i]['job_levels'] = levels

    with open('shl_individual_tests.json', 'w', encoding='utf-8') as f:
        json.dump(tests, f, indent=4)
        
    print("done!")

if __name__ == '__main__':
    main()
