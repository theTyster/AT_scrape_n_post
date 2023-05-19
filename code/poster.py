#! /usr/bin/env python3
import subprocess, json
from mastodon import Mastodon
from auth import akkoma_access_token
from upload import json_decorator
from pathlib import Path
from pprint import pprint as prettify


def status(*args, **kwargs):
# set default parameters for a status

    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akko.feature_set = 'pleroma'
    akko.status_post(*args, visibility='direct', language='en', content_type='text/markdown', **kwargs)


def quote_of_the_day():
    # I have this running as a cronjob once a day.
    p = Path(__file__).parents[2]

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
        if r > 25:
            r = 0
            status(':at_bmo: 💬  ' + quotes[r] + '\r #bmoQuoteOfTheDay')
            with open(iterator_file, 'w') as w:
                w.write(str(r))
        else:
            status(':at_bmo: 💬  ' + quotes[r] + '\r #bmoQuoteOfTheDay')
            with open(iterator_file, 'w') as w:
                w.write(str(r+1))


def comic_post(scraped_data, p):


    def send(r):
        issues = list(scraped_data.keys())
        print(len(issues))
        print(issues[171])
        exit()
        issues.sort() # don't depend on the ordering of dict's to be consistent.
        for i in issues:
            for image_num, image_data in scraped_data[i]['images'].items():
                attribute = f"""
<br>
<hr>

\"{image_data['description']}\".

See more in the :at_AdventureTime: wiki at [this link.]({scraped_data[i]['issue wikilink']})
"""
                msg = [
f"""
oh my glob. :at_bongocatbmo:

Look. at this rad comic book cover I found. :at_JakeTheDog-heartEyes:
""",
f"""
Sometimes when I am sad like finn :at_FinnTheBoy-cry: ,
I just look at cool arts.
Here look at this cool thing I made you.

Just kidding it was made by someone eles.
But I still hope it makes you smile. :at_snailSnail:
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
Hello. word. 🏻

:at_bmoWave:

Have some cool comic book cover art!
""",
f"""
I shall never enjoy the pleasures of skinny dipping.

But, I do enjoy cool looking pictures. Here's one of my favorites.
""",
f"""
Did you know I have a brother named allmo :at_all-mo: ?
He's pretty cool.

They can't move or anything though.

Did you know that me and Air are still going steady?
Lorraine is so jealous. :chickenroll:
Don't tell ricky. 🐀 He's always trying to move in on my turf.

Anyway, here's a picture or something.
"""]

                if (r >= 0) and (r <= 18): #19
                    msg = msg[0]
                if (r >= 19) and (r <= 37): #19
                    msg = msg[1]
                if (r >= 38) and (r <= 56): #19
                    msg = msg[2]
                if (r >= 57) and (r <= 85): #19
                    msg = msg[3]
                if (r >= 86) and (r <= 94): #19
                    msg = msg[4]
                if (r >= 95) and (r <= 113): #19
                    msg = msg[5]
                if (r >= 114) and (r <= 132): #19
                    msg = msg[6]
                if (r >= 133) and (r <= 151): #19
                    msg = msg[7]
                if (r >= 152) and (r <= 171): #20 intentional.
                    msg = msg[8]

            print((msg + attribute), media_ids=image_data['id'])


    # every time a comic is posted it will be a different one.
    iterator_file = f'iterations/comic-post'

    try:
        with open(iterator_file, 'r') as r:
            pass
    except FileNotFoundError:
        with open(iterator_file, 'w') as w:
            w.write('0')

    with open(iterator_file, 'r') as r:
        r = int(r.read())
        if r > 171:
            r = 0
            send(r)
            with open(iterator_file, 'w') as w:
                w.write(r)
        else:
            send(r)
            with open(iterator_file, 'w') as w:
                w.write(r+1)


@json_decorator
def nice_comic_post(scraped_data, p):
# check the load of the server to see if it is a good time to make a post.
# if the load average is over 100% for the last 5 minutes it will wait the post.

    cmd = ['cat', '/proc/loadavg']
    load = subprocess.run(cmd, capture_output=True)

    if not load.stderr:
        load = load.stdout.decode('utf-8')
        load = load.split()
        load = float(load[0])
        print(f'System Load: {load}')
        if load < 3:
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
    nice_comic_post()
    #quote_of_the_day()
