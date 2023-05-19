#! /usr/bin/env python3
import os, json
from pathlib import Path
from pprint import pprint as prettify
from mastodon import Mastodon
from auth import akkoma_access_token

# checks whether the images have been scraped. scrapes them if they haven't
# uploads the scraped images to the server.
# outputs an updated json file containing media_ids to be used in posts.


# set default parameters for media uploads
def upload(*args, **kwargs):
    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    return akko.media_post(*args, mime_type='image', **kwargs)


# checks if the images have been scraped and scrapes them if not. 
# provides access to the json file containing all scraped info.
def json_decorator(f):
    def wrapper():
        p = Path(__file__).parents[2]

        if not os.path.exists(f'{p}/scraped'):
            import scraper

            if __name__ == '__main__':
                print('Scraping Data...')

            scraper.main()

        jFile = open(f'{p}/scraped/all_scraped_data.json', 'r')
        scraped_data = json.load(jFile)
        f(scraped_data, p)
    return wrapper


@json_decorator
def main(scraped_data, p):
    issues = list(scraped_data.keys())

    for i in issues:
        for image_num, image_data in scraped_data[i]['images'].items():
            full_image = image_data['full image']
            media_dict = upload(full_image, description = image_data['caption'])
            image_data.update(media_dict)
            del image_data['caption']

    prettify(scraped_data)

    jFile = open(f'{p}/scraped/all_scraped_data.json', 'w')
    json.dump(scraped_data, jFile)


if __name__ == "__main__":
    main()
