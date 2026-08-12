from bs4 import BeautifulSoup  

def extract_species_counts(file_path):
    with open(file_path, encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    species_map = {}

        
    for li in soup.find_all('li', class_='BirdList-list-list-item'):
        time_tag = li.find('time')
        if time_tag and time_tag.has_attr('datetime'):
            is_exotic = li.find('svg', class_='Icon--exoticEscapee') is not None
            if is_exotic:
                continue
            observer_div = li.find('div', class_='Obs-observer')
            english_name = li.find('span', class_='Species-common').get_text(strip=True)
            if 'sp.' in english_name or '/' in english_name:
                continue
            species_map[english_name] = 'OK'
    return species_map

# Usage
file1 = 'dic_2025'
file2 = 'juil_2026'


file_1_counts = extract_species_counts(f'files/azuay_list_{file1}.html')
print(f'{file1} : {len(file_1_counts)} species')
file_2_counts = extract_species_counts(f'files/azuay_list_{file2}.html')
print(f'{file2} : {len(file_2_counts)} species')

def compare_species_dicts(dict1, dict2):
    all_keys = set(dict1) | set(dict2)

    for key in sorted(all_keys):
        val1 = dict1.get(key)
        val2 = dict2.get(key)

        if val1 != val2:
            print(f"❌ {key}: {file1} → {val1}, {file2} → {val2}")
        #else:
        #    print(f"✅ {key}: {val1}")


compare_species_dicts(file_1_counts, file_2_counts)
