from bs4 import BeautifulSoup  

def extract_species_counts(file_path):
    with open(file_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    species_map = {}

    for li in soup.find_all('li', id=lambda x: x and x.endswith('_out')):
        name_div = li.find('div', class_='snam')
        lim_span = li.find('span', class_='lim')
        input_span = li.find('input', class_='lim')

        if name_div and (lim_span or input_span):
            name = name_div.get_text(strip=True)
            if lim_span:
                value = lim_span.get_text(strip=True)
            else:
                value = input_span.get('value')
            species_map[name] = value

    return species_map

# Usage
file1 = 'active'
file2 = 'chimbo'


active_counts = extract_species_counts(f'files/{file1}_filter.html')
region_counts = extract_species_counts(f'files/{file2}_filter.html')

def compare_species_dicts(dict1, dict2):
    all_keys = set(dict1) | set(dict2)

    for key in sorted(all_keys):
        val1 = dict1.get(key)
        val2 = dict2.get(key)

        if val1 != val2:
            print(f"❌ {key}: {file1} → {val1}, {file2} → {val2}")
        #else:
        #    print(f"✅ {key}: {val1}")


compare_species_dicts(active_counts, region_counts)
