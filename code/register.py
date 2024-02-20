#! /usr/bin/env python3
from mastodon import Mastodon
from auth import *

Mastodon.create_app('Adventure Time Comics', api_base_url = 'https://behold.mylegendary.quest', to_file = 'clientcreds.secret')

Mastodon(client_id = 'clientcreds.secret').log_in('bmo', password, to_file = 'usercred.secret')
