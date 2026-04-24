from bs4 import BeautifulSoup
import requests

def extract_observation_dates(url):
    website = requests.get(url)
    soup = BeautifulSoup(website.text, 'html.parser')

    for li in soup.find_all('li', class_='BirdList-list-list-item'):
        time_tag = li.find('time')
        if time_tag and time_tag.has_attr('datetime'):
            ebird_name = li.get('id')
            species = li.find('span', class_='Species-common').get_text(strip=True)
            print(f'{ebird_name};{species}')

extract_observation_dates('https://ebird.org/region/EC/bird-list')
