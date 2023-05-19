#! /usr/bin/env python3
import os, re, requests, csv
from pathlib import Path
from bs4 import BeautifulSoup

def bonus():
    # get some cool bmo quotes and put them in a csv because bmo is awesome.

    p = Path(__file__).parents[2]
    url = 'https://adventuretime.fandom.com/wiki/BMO/Quotes'
    http = requests.get(url)
    soup = BeautifulSoup(http.text, 'html.parser')

    quote_tables = soup.find_all('table', class_='cquote')
    quotes = []

    for par in quote_tables:
        quotes.append(par.find('p').text)

    #format quotes for csv and print to file
    for q in quotes:
        q = q.replace('\n', '')
        q = q.replace('"', "'")
        q = f'"{q}",\n'
        with open(f'{p}/scraped/bmo-quotes.csv', 'a') as a:
            a.write(q)


def main():

    # path that scraped data will write out to will be the parent folder of this repo.
    p = Path(__file__).parents[2]

    if not param == 'testing':
        if not os.path.exists(f'{p}/scraped'):
            os.mkdir(f'{p}/scraped')
        else:
            print('Scrape directory already exists. Please move/rename the current directory.')
            exit()

    all_scraped = open(f'{p}/scraped/all_scraped_data.html', 'a')
    scraped_img_url = open(f'{p}/scraped/fullsize_covers.csv', 'a')
    scraped_url = open(f'{p}/scraped/comic_wiki_links.csv', 'a')

    html_skel = '''
<!DOCTYPE html>
<html lang="en-US">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      div {
        display: inline-block;
        padding: 16px;
      }
    </style>
  </head>
'''
    all_scraped.write(html_skel)

    all_scraped.write('<p>This page is meant to act as a gallery of all scraped data. The images you see here are sourcing from the wiki. Not local files.</p>')

    # Request the fandom page.
    root_url = "https://adventuretime.fandom.com"
    start_url = root_url + "/wiki/Volumes/Trade_Paperbacks"
    http = requests.get(start_url)
    soup = BeautifulSoup(http.text, 'html.parser')

    issues_a = soup.find_all('a', href=re.compile(r'.*issue', flags=re.I))
    issues = set()

    # Get all the url's for every AT issue in the wiki
    for i in issues_a:
        issues.add(root_url + i.get('href'))

    at_dict = {}

    for i in issues:
        #Writes the comic url's to a csv file
        scraped_url.write(i + ', \n')

        all_scraped.write(f'<h2>Link to Comic in the wiki <a href="{i}">here</a>.</h2><br>')

        http = requests.get(i)
        soup = BeautifulSoup(http.text, 'html.parser')

        # Find the Issue name
        page_title = soup.title
        issue_title = re.search(r'.+?(?= \|)', page_title.text).group()
        formatted_issue_title = issue_title.replace(' ', '_')
        formatted_issue_title = formatted_issue_title.replace('/', ':_')

        # find the cover art section for each issue
        cover_gallery_span = soup.find('span', id='Gallery')
        cover_gallery_h2 = cover_gallery_span.find_parent('h2')
        cover_gallery_h3 = cover_gallery_h2.find_next(id=re.compile(r'cover.*', flags=re.I))
        cover_gallery_div = cover_gallery_h3.find_next('div')
        cover_gallery_noscript = cover_gallery_div.find_all('noscript')

        # find the comic preview section for each issue
        preview_gallery_h3 = cover_gallery_div.find_next('h3')
        preview_gallery_div = preview_gallery_h3.find_next('div')
        preview_gallery_noscript = preview_gallery_div.find_all('noscript')

        # for loop which locates all of the attributions, thumbnails and full images for each
        # issue and places them in a dict
        img_dict = {}
        itemNo = 0
        for noscript in cover_gallery_noscript:

            #find the attribution for each image
            caption = noscript.find_next('div', class_='lightbox-caption')

            #find the src for each image thumbnail
            cover_img_thumb_url = noscript.img.get('src')
            get_cover_img_thumb = requests.get(cover_img_thumb_url)

            # format the image src url to get the full-size image.
            cover_url_split = re.split(r'(.png|.gif|.jpg|.jpeg|.webp)', cover_img_thumb_url,  maxsplit=1, flags=re.I)
            cover_fullsize_url = cover_url_split[0] + cover_url_split[1]
            get_cover_fullsize = requests.get(cover_fullsize_url)

            #Download all scraped images
            if not os.path.exists(f'{p}/scraped/img'):
                os.mkdir(f'{p}/scraped/img')
            if not os.path.exists(f'{p}/scraped/img/{formatted_issue_title}'):
                os.mkdir(f'{p}/scraped/img/{formatted_issue_title}')
            if not os.path.exists(f'{p}/scraped/img/{formatted_issue_title}/thumbs/'):
                os.mkdir(f'{p}/scraped/img/{formatted_issue_title}/thumbs/')
            if not os.path.exists(f'{p}/scraped/img/{formatted_issue_title}/fullsize/'):
                os.mkdir(f'{p}/scraped/img/{formatted_issue_title}/fullsize/')

            thumb_path = f'{p}/scraped/img/{formatted_issue_title}/thumbs/{formatted_issue_title}_item_{itemNo}_thumb{cover_url_split[1]}'
            fullsize_path = f'{p}/scraped/img/{formatted_issue_title}/fullsize/{formatted_issue_title}_item_{itemNo}_full{cover_url_split[1]}'

            with open(thumb_path, 'wb') as wb:
                wb.write(get_cover_img_thumb.content)

            with open(fullsize_path, 'wb') as wb:
                wb.write(get_cover_fullsize.content)

            #format scraped data into a dict object
            try:
                img_dict.update({itemNo:{'thumbnail':thumb_path, 'caption':caption.text, 'full image':fullsize_path}})
            except AttributeError:
                img_dict.update({itemNo:{'thumbnail':thumb_path, 'caption':"No Attribution Provided", 'full image':fullsize_path}})

            #if running from cli. Print info to console.
            if __name__ == '__main__':
                print(f'Scraped from: {i}.')
                print("Total comics scraped: " + str(len(at_dict)) + '\n')

    # Write scraped data out to files
            all_scraped.write(f'<div><a href={cover_fullsize_url}><img src ={cover_img_thumb_url}></a><p>{img_dict[itemNo]["caption"]}</p></div>')
            scraped_img_url.write(cover_fullsize_url + ', \n')

            itemNo += 1

        all_scraped.write('<br><hr><br>')
        at_dict.update({issue_title:{'issue wikilink':i, 'images':{**img_dict}}})

    import json

    with open(f'{p}/scraped/all_scraped_data.json', 'w') as w:
        json.dump(at_dict, w)

    # close all files
    all_scraped.close()
    scraped_img_url.close()
    scraped_url.close()

    bonus()


if __name__ == "__main__":
        bonus()
