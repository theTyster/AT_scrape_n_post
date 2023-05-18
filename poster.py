#! /usr/bin/env python3
import subprocess, os, json
from mastodon import Mastodon
from auth import akkoma_access_token
from pathlib import Path

# set default parameters for a status
def status(*args, **kwargs):
    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akko.feature_set = 'pleroma'
    akko.status_post(*args, visibility='direct', language='en', content_type='text/markdown', **kwargs)


def load_check():
    cmd = ['cat', '/proc/loadavg']
    load = subprocess.run(cmd, capture_output=True)

    if not load.stderr:
        load = load.stdout.decode('utf-8')
        load = load.split()
        load = float(load[0])
        print(f'System Load: {load}')
        if load < 3:
            print("Placeholder for running the actual script")
            #status("check, please")
        else:
            if __name__ == '__main__':
                print("System load is too high")
            exit()
    else:
        if __name__ == '__main__':
            print("Couldn't get the system load")
        exit()


def parse_scraped_JSON():
    p = Path(__file__).parents[1]

    if not os.path.exists(f'{p}/scraped'):
        import scraper
        scraper.main()

    jFile = open(f'{p}/scraped/all_scraped_data.json', 'r')
    scraped_data = json.load(jFile)



    print('\n\n')
    for key, val in scraped_data.items():
        print(f'{key} ==> \n')
        for key0, val0 in val.items():
            if len([item for item in val0 if item]) == 3:
                print(f'\t{key0} ==> ')
                for key1, val1 in val0.items():
                    print(f'\t\t{key1} ==> {val1}\n')
            else:
                print(f'\t{key0} ==> {val0}\n')

        exit()


if __name__ == '__main__':
    load_check()
    parse_scraped_JSON()

