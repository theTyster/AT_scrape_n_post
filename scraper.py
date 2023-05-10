#! /usr/bin/env python3

import os, re, requests
from pathlib import Path
from bs4 import BeautifulSoup

# path that scraped data will write out to will be the parent folder of this repo.
p = Path(__file__).parents[1]
if os.path.exists(f'{p}/scraped'):
    print('Scrape directory already exists. Please move/rename the current directory.')
    exit()
else:
    os.mkdir(f'{p}/scraped')


# Request the fandom page.
root_url = "https://adventuretime.fandom.com"
start_url = root_url + "/wiki/Volumes/Trade_Paperbacks"
request = requests.get(start_url)
soup = BeautifulSoup(request.text, 'html.parser')

issues_a = soup.find_all('a', href=re.compile(r'.*issue', flags=re.I))
issues = set()


full_size_scrape = open(f'{p}/scraped/full_size_images.html', 'a')
all_scraped = open(f'{p}/scraped/all_scraped_data.html', 'a')
scraped_img = open(f'{p}/scraped/fullsize_covers.csv', 'a')
scraped_url = open(f'{p}/scraped/comic_wiki_links.csv', 'a')

full_size_scrape.write('<h1>This document contains all of the full-size covers of the various comic issues</h1><p>It is meant to be used for archiving. To save all of the images simply right click on the page and save it to a file. All of the images will be placed in a folder adjacent to the file.</p>')


for i in issues_a:
    issues_a_href = i.get('href')
    issues.add(issues_a_href.replace('/wiki/', root_url + '/wiki/'))


for i in issues:
    #Writes the comic url's to a file
    scraped_url.write(i + ', \n')

    all_scraped.write(f'<h2>Link to Comic in the wiki <a href="{i}">here</a>.</h2><br>')

    request = requests.get(i)
    soup = BeautifulSoup(request.text, 'html.parser')

    cover_gallery_span = soup.find('span', id='Gallery')
    cover_gallery_h2 = cover_gallery_span.find_parent('h2')
    cover_gallery_h3 = cover_gallery_h2.find_next(id=re.compile(r'cover.*', flags=re.I))
    cover_gallery_div = cover_gallery_h3.find_next('div')
    cover_gallery_noscript = cover_gallery_div.find_all('noscript')


    for noscript in cover_gallery_noscript: 
        cover_img_thumb = noscript.img.get('src')
        cover_url_split = re.split(r'(.png|.gif|.jpg|.jpeg|.webp)', cover_img_thumb,  maxsplit=1, flags=re.I)
        cover_fullsize = cover_url_split[0] + cover_url_split[1]

        full_size_scrape.write(f'<img src={cover_fullsize}>')
        all_scraped.write(f'<a href={cover_fullsize}><img src ={cover_img_thumb}></a>')
        scraped_img.write(cover_fullsize + ', \n')
    all_scraped.write('<br><hr><br>')
