#! /usr/bin/env python3

from mastodon import Mastodon
from auth import (password, akkoma_access_token, client_secret)




def post(msg):
    #log in
    akkoma = Mastodon(client_id = client_secret)
    akkoma.log_in('cover_art_time', password, to_file = akkoma_access_token)

    akkoma = Mastodon(access_token = akkoma_access_token)
    akkoma.toot(msg)

post('''
ALGEBRAIC
A whole federated universe of people sharing stuff and doing things!
I can't wait to share all the cool Comic book cover art that I have here with me.
You can view my source code at https://github.com/twizzay-code/AT_scrape_n_post.
@twizzay is my papa. <3
''')
