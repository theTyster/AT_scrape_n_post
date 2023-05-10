#! /usr/bin/env python3

import os, re, requests
from pathlib import Path
from bs4 import BeautifulSoup

# path that scraped data will write out to will be the parent folder of this repo.
p = Path(__file__).parents[1]
if os.path.exists(f'{p}/scraped'):
    print('Scrape directory already exists, overwriting.')
else:
    os.mkdir(f'{p}/scraped')


# Request the fandom page.
root_url = "https://adventuretime.fandom.com"
start_url = root_url + "/wiki/Volumes/Trade_Paperbacks"
request = requests.get(start_url)
soup = BeautifulSoup(request.text, 'html.parser')

issues_a = soup.find_all('a', href=re.compile(r'.*issue', flags=re.I))
issues = set()


for i in issues_a:
    issues_a_href = i.get('href')
    issues.add(issues_a_href.replace('/wiki/', root_url + '/wiki/'))


for i in issues:
    request = requests.get(i)
    soup = BeautifulSoup(request.text, 'html.parser')

    cover_gallery_span = soup.find('span', id='Gallery')
    cover_gallery_h2 = cover_gallery_span.find_parent('h2')
    cover_gallery_h3 = cover_gallery_h2.find_next(id=re.compile(r'cover.*', flags=re.I))
    cover_gallery_div = cover_gallery_h3.find_next('div')
    cover_gallery_noscript = cover_gallery_div.find_all('noscript')


    for noscript in cover_gallery_noscript: 
        cover_img = noscript.img.get('src')
        cover_url_split = re.split(r'(.png|.gif|.jpg|.jpeg|.webp)', cover_img,  maxsplit=1, flags=re.I)
        cover_fullsize = cover_url_split[0] + cover_url_split[1]

        scraped = open(f'{p}/scraped/fullsize_covers.csv', 'a')
        scraped.write(cover_fullsize + ', \n')
