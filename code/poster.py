#! /usr/bin/env python3
import subprocess, json
from mastodon import Mastodon
from auth import akkoma_access_token
from upload import json_decorator
from pathlib import Path
from pprint import pprint as prettify

# set default parameters for a status
def status(*args, **kwargs):
    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akko.feature_set = 'pleroma'
    akko.status_post(*args, visibility='direct', language='en', content_type='text/markdown', **kwargs)

# check the load of the server to see if it is a good time to make a post.
# if the load average is over 100% for the last 5 minutes it will wait the post.

@json_decorator
def load_check(scraped_data, p):
    cmd = ['cat', '/proc/loadavg']
    load = subprocess.run(cmd, capture_output=True)

    if not load.stderr:
        load = load.stdout.decode('utf-8')
        load = load.split()
        load = float(load[0])
        print(f'System Load: {load}')
        if load < 3:
            for image_num, image_data in scraped_data.items():
                prettify(image_data)
                exit
            msg = f'''
'''
            status()
        else:
            if __name__ == '__main__':
                print("System load is too high")
            exit()
    else:
        if __name__ == '__main__':
            print("Couldn't get the system load")
        exit()

if __name__ == '__main__':
    load_check()
