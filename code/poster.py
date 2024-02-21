#! /usr/bin/env python3
import subprocess, json, os, sys
from mastodon import Mastodon
from auth import pleroma_access_token
grom pathlib import Path
from msg import msg_text

pler = Mastodon(api_base_url = 'https://behold.mylegendary.quest', access_token = pleroma_access_token)

# set default parameters for statuses
def status(*args, **kwargs):
# set default parameters for a status
    pler.feature_set = 'pleroma'
    status_id = pler.status_post(*args, language='en', content_type='text/markdown', **kwargs)
    return status_id.id


# set default parameters for media uploads
def upload(*args, **kwargs):
    pler.feature_set = 'pleroma'
    image_id = pler.media_post(*args, mime_type='image/jpeg', **kwargs)
    return image_id.id

def pin(*args):
    pler.feature_set = 'pleroma'
    pler.status_pin(*args)

def unpin(*args):
    pler.feature_set = 'pleroma'
    pler.status_unpin(*args)

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


def quote_of_the_day():
    # I have this running as a cronjob once a day.
    p = Path(__file__).parents[2]
    p_iter = Path(__file__).parent

    with open(f'{p}/scraped/bmo-quotes.csv', 'r') as quotes_csv:
        quotes_len = len(quotes_csv.readlines())

    with open(f'{p}/scraped/bmo-quotes.csv', 'r') as quotes_csv:
        quotes = quotes_csv.read().split(',\n')
        quotes.pop() # removes the weird space that appears as the last item in the list.

    iterator_file = f'{p_iter}/iterations/bmo-quote-of-the-day'

    # creates the iterator file if it doesn't exist
    try:
        with open(iterator_file, 'r') as r:
            pass
    except FileNotFoundError:
        with open(iterator_file, 'w') as w:
            w.write('0')

    # gets the iteration for the quote and the id for yesterdays pinned quote
    with open(iterator_file, 'r') as r:
        i = int(r.readline())
        try:
            pin_current = r.readline()
        except ValueError:
            pin_current = None

    # posts todays quote and writes the id and iteration out to file.
    if i == quotes_len:
        i = 0
        pin_next = status(':at_bmo: 💬  ' + quotes[i] + '\r #bmoQuoteOfTheDay')
        print(quotes[i])
        with open(iterator_file, 'w') as w:
            w.write(str(i))
            w.write('\n' + str(pin_next))
    else:
        pin_next = status(':at_bmo: 💬  ' + quotes[i] + '\r #bmoQuoteOfTheDay')
        print(quotes[i])
        with open(iterator_file, 'w') as w:
            w.write(str(i+1))
            w.write('\n' + str(pin_next))

    # unpins yesterdays quote and pins todays
    if pin_current:
        unpin(pin_current)
        pin(pin_next)
    else:
        pin(pin_next)


def comic_post(scraped_data, p):

    #path to iteration file
    p_iter = Path(__file__).parent

    # every time a comic is posted it will be a different one.
    iterator_file = f'{p_iter}/iterations/comic-post'
    if not os.path.exists(f'{p_iter}/iterations'):
        os.mkdir(f'{p_iter}/iterations')

    # checks if the file already exists. Creates them if they don't.
    try:
        with open(iterator_file, 'r') as r:
            int(r.readline())
            int(r.readline())
            int(r.readline())
    except (FileNotFoundError, ValueError):
        with open(iterator_file, 'w') as w:
            w.write('0\n0\n0')

    # reads the current iteration.
    with open(iterator_file, 'r') as r:
        issue_iterator = int(r.readline())
        image_iterator = int(r.readline())
        msg_iterator = int(r.readline())

    if issue_iterator >= len(scraped_data.keys()):
        issue_iterator = 0

    issues = list(scraped_data.keys())
    issues.sort() # don't depend on the ordering of dict's to be consistent.

    #prints the filename of the image to be uploaded to stdout.
    print(scraped_data[issues[issue_iterator]]['images'][str(image_iterator)]['full image'].split(f'{p}/scraped/img/', maxsplit=1)[1].split('fullsize', maxsplit=1)[1])

    msg = msg_text

    if msg_iterator == len(msg):
        msg_iterator = 0


    def send(msg, issue_iterator, image_iterator, msg_iterator):

        try:
            image_issue = scraped_data[issues[issue_iterator]]
            images = scraped_data[issues[issue_iterator]]['images']
            full_image = scraped_data[issues[issue_iterator]]['images'][str(image_iterator)]['full image']
            image_id = str(upload(full_image, description = images[str(image_iterator)]['caption']))

        except KeyError as e:
            print(f'Dict Key Error for: {e}. Image upload failed.')
            exit()

        attribute = f"""
<hr>
<br>
[This Comic]({image_issue['issue wikilink']}) |
[All covers](https://adventuretime.fandom.com/wiki/Adventure_Time_Comic_Covers) |
[Code](https://git.mylegendary.quest/twizzay/AT_scrape_n_post) |
[BMO's Comic Memory Game](https://mylegendary.quest/unlisted/Memory_Game/index.html)
<br>
#AdventureTime #Cartoons #Comics #Art
"""

        msg = msg[msg_iterator]
        msg = msg + attribute

        status((msg), media_ids=image_id)
        return images


    images = send(msg, issue_iterator, image_iterator, msg_iterator)

    image_keys = [int(key) for key in images.keys()]
    if (image_iterator + 1) in image_keys:
        image_iterator = (image_iterator + 1)
    else:
        image_iterator = '0'
        issue_iterator += 1

    msg_iterator += 1

    with open(iterator_file, 'w') as w:
        w.write(str(issue_iterator) + '\n')
    with open(iterator_file, 'a') as a:
        a.write(str(image_iterator) + '\n')
    with open(iterator_file, 'a') as a:
        a.write(str(msg_iterator))


@json_decorator
def nice_post(scraped_data, p):
# check the load of the server to see if it is a good time to make a post.
# if the load average is over 100% for the last 5 minutes it will wait the post.

    cmd = ['cat', '/proc/loadavg']
    load = subprocess.run(cmd, capture_output=True)

    if not load.stderr:
        load = load.stdout.decode('utf-8')
        load = load.split()
        load = float(load[0])
        print(f'System Load: {load}')
        if load < 2:
            try:
                sys.argv[1] == 'quote_of_the_day'
                quote_of_the_day()
            except IndexError:
                comic_post(scraped_data, p)

        else:
            if __name__ == '__main__':
                print("System load is too high")
            exit()
    else:
        if __name__ == '__main__':
            print("Couldn't get the system load")
        exit()


if __name__ == '__main__':
    nice_post()
