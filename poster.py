#! /usr/bin/env python3
from mastodon import Mastodon
from auth import akkoma_access_token

def status(*args, **kwargs):
    akko = Mastodon(api_base_url = 'https://thisis.mylegendary.quest', access_token = akkoma_access_token)
    akko.feature_set = 'pleroma'
    akko.status_post(*args, visibility='direct', language='en', content_type='text/markdown', **kwargs)

status('check, please')
