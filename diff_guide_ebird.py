from bs4 import BeautifulSoup  
from datetime import datetime, timedelta
import requests
import argparse
    
parser = argparse.ArgumentParser(
    description="Compare guide species with eBird"
)

parser.add_argument(
    "--guide",
    type=str,
    required=True,
    help="Guide name (e.g. guia_uda, ucuenca)"
)

args = parser.parse_args()

guide = args.guide

def extract_observation_dates(list_urls):
    result = {}
    for url in list_urls:
        website = requests.get(f'{url}?hs_sortBy=taxon_order&hs_o=asc')   
        soup = BeautifulSoup(website.text, 'html.parser')
        where = soup.find('div', class_='PlaceTitle-name').find('h1').get_text(strip=True)
        
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
                birder_tag = observer_div.select_one('span:not(.is-visuallyHidden), a')  
                birder = birder_tag.get_text(strip=True) if birder_tag else None
                last_seen = datetime.strptime(time_tag['datetime'], '%Y-%m-%d %H:%M')
                if name in result:
                    if last_seen > result[name]['last_seen']:
                        #Newest
                        result[name] = dict(
                            where=where,
                            last_seen=last_seen,
                            birder=birder)
                else:
                    result[name] = dict(
                        where=where,
                        last_seen=last_seen,
                        birder=birder)

    return result

if (guide == 'ucuenca'):
    list_urls = [
     'https://ebird.org/hotspot/L40907383/bird-list', #U. Cuenca
    ]
    file_guide = "ucuenca.txt"
elif guide == 'guia_uda':
    list_urls = [
     'https://ebird.org/hotspot/L8552768/bird-list', #Camino al Cielo
     'https://ebird.org/hotspot/L14176874/bird-list', #El Alto
     'https://ebird.org/hotspot/L20771755/bird-list', #Uchuloma
     'https://ebird.org/hotspot/L2763248/bird-list', #Putushi-Culebrillas
     'https://ebird.org/hotspot/L59238451/bird-list', #Cerro Minas
     'https://ebird.org/hotspot/L19673318/bird-list', #Represa Chanlud Road
     'https://ebird.org/hotspot/L62811993/bird-list', #Carretera Llaviucu
     'https://ebird.org/hotspot/L1899719/bird-list', #Llaviucu
     'https://ebird.org/hotspot/L2763237/bird-list', #Mazan
     'https://ebird.org/hotspot/L18929810/bird-list', #Pico de Pescado
     'https://ebird.org/hotspot/L2763250/bird-list', #Cubilan
    ]
    file_guide = "guia_uda.txt"
else:
    raise Error('GUIA DESCONOCIDA')

ebird_data = extract_observation_dates(list_urls)

uda_data = {}
order = 1
with open(file_guide) as fp:
    lines = fp.readlines()
    for species in lines:
        uda_data[species.strip()] = dict(order=order)
        order += 1

only_in_ebird = {k: ebird_data[k] for k in ebird_data.keys() - uda_data.keys()}
only_in_guide = {k: uda_data[k] for k in uda_data.keys() - ebird_data.keys()}


print(f'SOLO EBIRD ({len(only_in_ebird)})')
for species in only_in_ebird:
    print(species, ' : ', ebird_data[species])
print('')
print(f'SOLO GUIA ({len(only_in_guide)})')
for species in only_in_guide:
    print(species)
