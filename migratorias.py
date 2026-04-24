from bs4 import BeautifulSoup  
from datetime import datetime, timedelta
import requests
import json

def extract_observation_dates(list_urls, migratorias):
    results = {}
    for url in list_urls:
        website = requests.get(f'{url}?hs_sortBy=taxon_order&hs_o=asc')   
        soup = BeautifulSoup(website.text, 'html.parser')
        hotspot = soup.find('div', class_='PlaceTitle-name').find('h1').get_text(strip=True)
        results[hotspot] = {
            "url": url,
            "birds": []
        }

        for li in soup.find_all('li', class_='BirdList-list-list-item'):
            time_tag = li.find('time')
            if time_tag and time_tag.has_attr('datetime'):
                is_exotic = li.find('svg', class_='Icon--exoticEscapee') is not None
                if is_exotic:
                    continue
                name = li.find('span', class_='Species-common').get_text(strip=True)
                if 'sp.' in name:
                   continue
                   
                if name in migratorias:
                    results[hotspot]['birds'].append(name)
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
 'https://ebird.org/hotspot/L20491806/bird-list', #Tarqui Guzho
]
file_guide = "migratorias.txt"

migratorias = {}
with open(file_guide) as fp:
    lines = fp.readlines()
    for species in lines:
        migratorias[species.strip()] = True

ebird_data = extract_observation_dates(list_urls, migratorias)


html = """
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Aves Migratorias</title>
<style>
body { font-family: Arial; padding: 20px; }
.title a { font-weight: bold; font-size: 18px; text-decoration: none; }
.list { margin-left: 15px; }
</style>
</head>
<body>

<h1>Aves migratorias en Cuenca</h1>
"""

# sort hotspots
sorted_data = sorted(ebird_data.items(), key=lambda x: len(x[1]['birds']), reverse=True)

for hotspot, hotsport_info in sorted_data:
    if not hotsport_info:
        continue

    url = "birds"
    html += f"""
    <div>
        <div class="title">
            <a href="{hotsport_info['url']}" target="_blank">
                {hotspot} : {len(hotsport_info['birds'])} especies
            </a>
        </div>
        <div class="list">{", ".join(hotsport_info['birds'])}</div>
    </div>
    """

html += "</body></html>"

with open("migratorias.html", "w", encoding="utf-8") as f:
    f.write(html)

print('MIGRATORIAS.HTML : DONE!')
