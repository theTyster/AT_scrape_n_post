#! /usr/bin/env python3

import os, re, requests
from bs4 import BeautifulSoup

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

check = []
for i in issues:
    print(i)
    request = requests.get(i)
    soup = BeautifulSoup(request.text, 'html.parser')

    cover_gallery_span = soup.find('span', id='Gallery')
    for span in cover_gallery_span:
        cover_gallery_h2 = span.find_parent('h2')
        cover_gallery_h3 = cover_gallery_h2.find_next(id=re.compile(r'cover.*', flags=re.I))
        cover_gallery_div = cover_gallery_h3.find_next('div')
        cover_gallery_noscript = cover_gallery_div.find_all('noscript')
        for noscript in cover_gallery_noscript: 
            cover_img = noscript.img.get('src')
            cover_url_split = cover_img.split('jpg', maxsplit=1)
            print(cover_url_split)
            cover_fullsize = cover_url_split[0] + cover_url_split[1]


            check.append(cover_img)
        print(len(check))

print('Issues: ' + str(len(issues)))
print('Items: ' + str(len(issues)))
