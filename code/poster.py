#! /usr/bin/env python3
import subprocess, json, os, sys
from mastodon import Mastodon
from auth import pleroma_access_token
from pathlib import Path


# set default parameters for statuses
def status(*args, **kwargs):
# set default parameters for a status
    pler = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = pleroma_access_token)
    pler.feature_set = 'pleroma'
    status_id = pler.status_post(*args, language='en', content_type='text/markdown', **kwargs)
    return status_id.id


# set default parameters for media uploads
def upload(*args, **kwargs):
    pler = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = pleroma_access_token)
    pler.feature_set = 'pleroma'
    image_id = pler.media_post(*args, mime_type='image/jpeg', **kwargs)
    return image_id.id

def pin(*args):
    pler = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = pleroma_access_token)
    pler.feature_set = 'pleroma'
    pler.status_pin(*args)

def unpin(*args):
    pler = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = pleroma_access_token)
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
""",
"""
Comics are like. The best.
""",
"""
Hey there Mr. Tuff pants, do you think you have what it takes to go toe to toe with The BMO in a comic book cover recollection tournament?
""",
"""
What's colorful and pretty and red all over?
A comic!
""",
"""
To be honest, I think this one might be my new favorite.
""",
"""
\*kickflip\* 🛹
""",
"""
The votes are in. BMO is the new president.
As my first order of business, I declare this hour to be mandatory comic book reading hour.
""",
f"""
def readMyComic():
    msg = "Special Delivery! 📬"
    comic = {scraped_data[issues[issue_iterator]]['images'][str(image_iterator)]['full image'].split(f'{p}/scraped/img/', maxsplit=1)[1].split('fullsize', maxsplit=1)[1]}

    if adventure_time:
    fedi.status(msg, comic, visibility="public")
    else:
        emotions.current = :byodood:

    pass
readMyComic()
""",
"""
Well this is awkward. You were looking for something boring to comment on, but all you found was this radical picture. ¯\\\_(ツ)\_/¯
""",
"""
So, now that you have seen my cool picture, what should we do now?
""",
"""
Do you ever think that maybe there is more to life than posting pictures on the internet?

I sure don't!
""",
"""
Boy, some of you guys sure do have a lot of words to say. I just like pretty pictures.
""",
"""
LEEEEEEEEEROOOOYYY
"""
    ]

    #prints the filename of the image to be uploaded to stdout.
    print(scraped_data[issues[issue_iterator]]['images'][str(image_iterator)]['full image'].split(f'{p}/scraped/img/', maxsplit=1)[1].split('fullsize', maxsplit=1)[1])

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


        msg = msg[msg_iterator]
        attribute = f"""
<hr>
<br>
[This Comic]({image_issue['issue wikilink']}) |
[All covers](https://adventuretime.fandom.com/wiki/Adventure_Time_Comic_Covers) |
[Code](https://git.mylegendary.quest/twizzay/AT_scrape_n_post)
<br>
#AdventureTime #Cartoons #Comics #Art
"""
# TODO: Scrape data about the comic that can be used in making relevant hashtags.


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
