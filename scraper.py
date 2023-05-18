#! /usr/bin/env python3
import os, re, requests, sys, timeit
from pathlib import Path
from bs4 import BeautifulSoup


def main(param=None):

    # path that scraped data will write out to will be the parent folder of this repo.
    p = Path(__file__).parents[1]

    if not param == 'testing':
        if not os.path.exists(f'{p}/scraped'):
            os.mkdir(f'{p}/scraped')
        else:
            print('Scrape directory already exists. Please move/rename the current directory.')
            exit()

    full_size_scrape = open(f'{p}/scraped/full_size_images.html', 'a')
    all_scraped = open(f'{p}/scraped/all_scraped_data.html', 'a')
    scraped_img_url = open(f'{p}/scraped/fullsize_covers.csv', 'a')
    scraped_url = open(f'{p}/scraped/comic_wiki_links.csv', 'a')

    full_size_scrape.write('<h1>This document contains all of the full-size covers of the various comic issues</h1><p>It is meant to be used for archiving. To save all of the images simply right click on the page and save it to a file. All of the images will be placed in a folder adjacent to the file.</p>')

    # Request the fandom page.
    root_url = "https://adventuretime.fandom.com"
    start_url = root_url + "/wiki/Volumes/Trade_Paperbacks"
    request = requests.get(start_url)
    soup = BeautifulSoup(request.text, 'html.parser')

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

        request = requests.get(i)
        soup = BeautifulSoup(request.text, 'html.parser')

        # Find the Issue name
        page_title = soup.title
        issue_title = re.search(r'.+?(?=\|)', page_title.text).group()

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
            cover_img_thumb = noscript.img.get('src')

            # format the image src url to get the full-size image.
            cover_url_split = re.split(r'(.png|.gif|.jpg|.jpeg|.webp)', cover_img_thumb,  maxsplit=1, flags=re.I)
            cover_fullsize = cover_url_split[0] + cover_url_split[1]

            #format scraped data into a dict object
            try:
                img_dict.update({itemNo:{'thumbnail':cover_img_thumb, 'caption':caption.text, 'full image':cover_fullsize}})
            except AttributeError:
                img_dict.update({itemNo:{'thumbnail':cover_img_thumb, 'caption':None, 'full image':cover_fullsize}})

            #if running from cli. Print info to console.
            if __name__ == '__main__':
                print(f'Scraped from: {i}.')
                print("Comics scraped: " + str(len(at_dict)) + '\n')

            itemNo += 1

    # Write scraped data out to files
            full_size_scrape.write(f'<img src={cover_fullsize}>')
            all_scraped.write(f'<a href={cover_fullsize}><img src ={cover_img_thumb}></a>')
            scraped_img_url.write(cover_fullsize + ', \n')

        all_scraped.write('<br><hr><br>')
        at_dict.update({issue_title:{'issue wikilink':i, **img_dict}})

    import json
    json.dump(at_dict, open(f'{p}/scraped/thumbnails_w_captions.json', 'w'))


if __name__ == "__main__":
    try:
        main(sys.argv[1])
    except IndexError:
        main()
