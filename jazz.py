from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json
import re

events = {}
# Get the current date and time
now = datetime.now()
current_year = now.year
current_month = now.month
#blue note nyc
bluenote_text = requests.get('https://www.bluenotejazz.com/nyc/shows/?calendar_view').text
bluenote_soup = BeautifulSoup(bluenote_text, 'lxml')
bluenote_shows = bluenote_soup.find_all('div', class_='inner')

for show in bluenote_shows:
    bluenote_band = show.find('h3')
    if bluenote_band:
        bluenote_band = bluenote_band.text.strip()
    else:
        bluenote_band = "No band information"

    bluenote_day = show.find('div', class_='day')
    if bluenote_day:
        day = bluenote_day.text.strip().zfill(2)
        bluenote_day = f'{current_year}-{current_month:02d}-{day}'
    else:
        bluenote_day = "No date info"

    bluenote_showtime = show.find('div', class_='showtimes')
    if bluenote_showtime:
        showtimes = re.findall(r'\d{1,2}:\d{2} [APM]{2}', bluenote_showtime.text)
        bluenote_showtime = ' & '.join(showtimes)
    else:
        bluenote_showtime = "No showtime info"
    
    event = {
        'band': bluenote_band,
        'date': bluenote_day,
        'time': bluenote_showtime,
        'link': 'https://www.bluenotejazz.com/nyc/shows/?calendar_view',
        'category': 'Music',
        'genre': 'Jazz'
    }
    if bluenote_day not in events:
        events[bluenote_day] = {}
    if 'Blue Note NYC' not in events[bluenote_day]:
        events[bluenote_day]['Blue Note NYC'] = []
    events[bluenote_day]['Blue Note NYC'].append(event)


# #smalls and mezzrow
# smalls_text = requests.get('https://www.smallslive.com/').text
# smalls_soup = BeautifulSoup(smalls_text, 'lxml')
# smalls_shows = smalls_soup.find_all('a',  attrs={'aria-label': True})

# for show in smalls_shows:
#     aria_label = show['aria-label']
#     href = show['href']
#     parts = aria_label.split('Live at')

#     band_name = parts[0].strip()

#     if len(parts) > 1:
#         venue_and_time = parts[1].strip()
#     else:
#         venue_and_time = ''
    
#     parts2 = venue_and_time.split('sets start at')
#     venue = parts2[0].strip()
#     time = parts2[1].strip()
#     event = {
#         'band' : band_name,
#         'venue': venue,
#         'time': time,
#         'link' : f"https://www.smallslive.com{href}"
        # 'category': 'Music',
        # 'genre': 'Jazz'
#     }

#     events.append(event)
# #NEED TO ADD DATES!
# # print(events)

# #village vanguard
# vanguard_text = requests.get('https://villagevanguard.com/').text
# vanguard_soup = BeautifulSoup(vanguard_text, 'lxml')
# vanguard_shows = vanguard_soup.find_all('div', 'event-listing')

# for show in vanguard_shows:
#     band = show.find('h2')
#     if band:
#         band = band.text.strip()
#     else:
#         band = "No band information"
#     date = show.find('h3')
#     if date:
#         date = date.text.strip()
#     else:
#         date = "No band information"
#     event = {
#         'band': band,
#         'venue': 'Village Vanguard',
#         'date': date,
#         'link': 'https://villagevanguard.com/',
#         'category': 'Music',
#         'genre': 'Jazz'
#     }
#     if 'Village Vanguard' not in events:
#         events['Village Vanguard'] = []
#     events['Village Vanguard'].append(event)

with open('JazzData.json', 'w') as json_file:
    json.dump(events, json_file, indent=4)

print("JSON file created successfully.")