from bs4 import BeautifulSoup
import requests

met = requests.get('https://www.metmuseum.org/exhibitions').text
soup = BeautifulSoup(met, 'lxml')
exhibitions = soup.find_all('div', class_='content-card_card__iiXut undefined content-card_hasBorder__Op_kV')

# print(exhibitions)
for exhibition in exhibitions:
    name = exhibition.find('span').text
    date_div = exhibition.find('div', string=lambda text: text and 'Through' in text)
    if date_div:
        date = date_div.text
    else:
        print("No date found.")
    
    print(name)
    print(date)