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

for i in issues:
    request = requests.get(i)
    soup = BeautifulSoup(request.text, 'html.parser')

    cover_gallery_span = soup.find_all('span', id=re.compile('cover.*', flags=re.I))
    print(i)
    print(cover_gallery_span)
    print('')
    

