from bs4 import BeautifulSoup  
from datetime import datetime, timedelta
import requests

def extract_observation_dates(list_urls):

    result = {}
    for url in list_urls:
        website = requests.get(f'{url}?yr=cur&hs_sortBy=taxon_order&hs_o=asc')   
        soup = BeautifulSoup(website.text, 'html.parser')
        
        for li in soup.find_all('li', class_='BirdList-list-list-item'):
            time_tag = li.find('time')
            if time_tag and time_tag.has_attr('datetime'):
                is_exotic = li.find('svg', class_='Icon--exoticEscapee') is not None
                if is_exotic:
                    continue
                ebird_id = li.get('id')
                observer_div = li.find('div', class_='Obs-observer')
                english_name = li.find('span', class_='Species-common').get_text(strip=True)
                if 'sp.' in english_name:
                   continue
                birder_tag = observer_div.select_one('span:not(.is-visuallyHidden), a')  
                birder = birder_tag.get_text(strip=True) if birder_tag else None
                result[ebird_id] = dict(
                    english_name=english_name,
                    last_seen=datetime.strptime(time_tag['datetime'], '%Y-%m-%d %H:%M'),
                    birder=birder)

    return result

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
 'https://ebird.org/hotspot/L20491806/bird-list', #Tarqui Guzho
]

azuay_data = extract_observation_dates(list_urls)

for ebird_id in azuay_data:
    print(azuay_data[ebird_id]['english_name'])

print(f'{len(azuay_data)} birds found in Cuenca this year.')
