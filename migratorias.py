from bs4 import BeautifulSoup  
from datetime import datetime, timedelta
import requests

def extract_observation_dates(list_urls, migratorias):
    results = {}
    for url in list_urls:
        website = requests.get(f'{url}?hs_sortBy=taxon_order&hs_o=asc')   
        soup = BeautifulSoup(website.text, 'html.parser')
        hotspot = soup.find('div', class_='PlaceTitle-name').find('h1').get_text(strip=True)
        results[hotspot] = []
        for li in soup.find_all('li', class_='BirdList-list-list-item'):
            time_tag = li.find('time')
            if time_tag and time_tag.has_attr('datetime'):
                is_exotic = li.find('svg', class_='Icon--exoticEscapee') is not None
                if is_exotic:
                    continue
                observer_div = li.find('div', class_='Obs-observer')
                name = li.find('span', class_='Species-common').get_text(strip=True)
                if 'sp.' in name:
                   continue
                   
                if name in migratorias:
                    results[hotspot].append(name)
    return results

list_urls = [
 'https://ebird.org/hotspot/L2246951/bird-list', #Paraiso
 'https://ebird.org/hotspot/L2246906/bird-list', #Pumapungo
 'https://ebird.org/hotspot/L8552768/bird-list', #Camino al Cielo
 'https://ebird.org/hotspot/L14176874/bird-list', #El Alto
 'https://ebird.org/hotspot/L15916179/bird-list', #Ictocruz
 'https://ebird.org/hotspot/L31585424/bird-list', #Jardin Botanico
 'https://ebird.org/hotspot/L40907383/bird-list', #U. Cuenca
 'https://ebird.org/hotspot/L4999943/bird-list', #Ucubamba
 'https://ebird.org/hotspot/L20771755/bird-list', #Uchuloma
 'https://ebird.org/hotspot/L28343203/bird-list', #El Tablon
 'https://ebird.org/hotspot/L8828943/bird-list', # La Calera
]
file_guide = "migratorias.txt"

migratorias = {}
with open(file_guide) as fp:
    lines = fp.readlines()
    for species in lines:
        migratorias[species.strip()] = True

ebird_data = extract_observation_dates(list_urls, migratorias)


for hotspot in sorted(ebird_data, key=lambda h: len(ebird_data[h]), reverse=True):
    print(hotspot, ' :', len(ebird_data[hotspot]),  'especies')
    if len(ebird_data[hotspot]) > 0:
        print('LISTA : ', ','.join(ebird_data[hotspot]))
        print('')