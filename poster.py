#! /usr/bin/env python3

from mastodon import Mastodon
from auth import *




def post(msg):
    akkoma = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akkoma.toot(msg)

post('''
ALGEBRAIC

A whole federated universe of people sharing stuff and doing things!

I cannot wait to dip my toes in the salsa and share all the cool Comic book cover art that I have here with me.

You can view my source code at https://github.com/twizzay-code/AT_scrape_n_post.
@twizzay is my papa. <3
''')
