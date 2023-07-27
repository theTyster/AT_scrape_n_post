#! /usr/bin/env python3
import subprocess, json, os, sys
from mastodon import Mastodon
from auth import akkoma_access_token
from upload import json_decorator
from pathlib import Path


def status(*args, **kwargs):
# set default parameters for a status

    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akko.feature_set = 'pleroma'
    akko.status_post(*args, language='en', content_type='text/markdown', **kwargs)


def quote_of_the_day():
    # I have this running as a cronjob once a day.
    p = Path(__file__).parents[2]

    with open(f'{p}/scraped/bmo-quotes.csv', 'r') as quotes_csv:
        quotes_len = len(quotes_csv.readlines())

    with open(f'{p}/scraped/bmo-quotes.csv', 'r') as quotes_csv:
        quotes = quotes_csv.read().split(',\n')
        quotes.pop() # removes the weird space that appears as the last item in the list.

    iterator_file = f'iterations/bmo-quote-of-the-day'

    try:
        with open(iterator_file, 'r') as r:
            pass
    except FileNotFoundError:
        with open(iterator_file, 'w') as w:
            w.write('0')

    with open(iterator_file, 'r') as r:
        r = int(r.read())
        if r > quotes_len:
            r = 0
            status(':at_bmo: 💬  ' + quotes[r] + '\r #bmoQuoteOfTheDay')
            with open(iterator_file, 'w') as w:
                w.write(str(r))
        else:
            status(':at_bmo: 💬  ' + quotes[r] + '\r #bmoQuoteOfTheDay')
            with open(iterator_file, 'w') as w:
                w.write(str(r+1))


def comic_post(scraped_data, p):
    msg = [
f"""
oh my glob. :at_bongocatbmo:

Look. at this rad comic book cover I found. :at_JakeTheDog-heartEyes:
""",
f"""
Sometimes when I am sad like finn :at_FinnTheBoy-cry: ,
I just look at cool arts.

I hope this makes you smile, atleast.
""",
f"""
I am beemo.
One day you will be old and also you will be dead.

But it's ok, because I will still be here posting cool pictures for you.
""",
f"""
What time is it??
It's not adventure time.
That's not what the internet is for I dont think.

But, that is ok because it is comic book time!
:at_AdventureTime:
:at_FinnJake-fistbump:
""",
f"""
I do not post anything that is not either cool and/or awesome.
""",
f"""
Did you know that I can ollie over a sandwhich *while* looking awesome.
Ok, I only did that one time. And, yes,  there was a ramp. >.>

Stop looking at me like that and look at this instead.
""",
f"""
Hello. word.

:at_bmoWave:

Have some cool comic book cover art!
""",
f"""
I shall never enjoy the pleasures of skinny dipping.

But, I do enjoy cool looking pictures. Here's one of my favorites.
""",
f"""
Did you know I have a brother named allmo? :at_all-mo:
He's pretty cool.

Anyway, here's a picture or something.
"""]


    # every time a comic is posted it will be a different one.
    iterator_file = f'iterations/comic-post'
    if not os.path.exists('iterations'):
        os.mkdir('iterations')

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

    if msg_iterator == len(msg):
        msg_iterator = 0

    def send(msg, issue_iterator, image_iterator, msg_iterator):

        issues = list(scraped_data.keys())
        issues.sort() # don't depend on the ordering of dict's to be consistent.

        try:
            image_issue = scraped_data[issues[issue_iterator]]
            images = scraped_data[issues[issue_iterator]]['images']
            image_id = scraped_data[issues[issue_iterator]]['images'][str(image_iterator)]['id']
        except KeyError as e:
            print(f'Dict Key Error for: {e}. Did you run upload.py??')
            exit()


        msg = msg[msg_iterator]
        attribute = f"""
<hr>
<br>
[This Comic]({image_issue['issue wikilink']}) |
[All covers](https://thisis.mylegendary.quest/images/AdventureTime/index.html) |
[Code](https://github.com/twizzay-code/AT_scrape_n_post)
"""


        status((msg + attribute), media_ids=image_id)
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
