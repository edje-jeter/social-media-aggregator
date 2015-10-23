#!/usr/bin/env python

# system tools
import os
import sys
import pprint

# api tools
import requests
import base64
import json

# other useful stuff
from unidecode import unidecode
from PIL import Image

sys.path.append('..')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

import django
from django.conf import settings
django.setup()

from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from main.models import Tweet

CONSUMER_KEY = 'OaLXymYrM64XqQsfqBmELv5rY'
CONSUMER_SECRET = '7Z4eazrTISyHg1jobkU1JjAPpQg7F2vu5KaP7Tv2iAlaesQywp'

# the base twitter url for sending api requests
URL = 'https://api.twitter.com/oauth2/token'

# the search term to be used
SEARCH_TERM = 'Brandon Sanderson'

# base64 encode credentials
credentials = base64.urlsafe_b64encode('%s:%s'
                                       % (CONSUMER_KEY, CONSUMER_SECRET))

# custom headers for the formatted api keys
custom_headers = {
                  'Authorization': 'Basic %s' % (credentials),
                  'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
                 }

# post variable declaring the type of authentication or 'grant type' being used
grant_type_data = 'grant_type=client_credentials'

# Put it all together: send a post request to the base twitter URL with the
# custom headers and post variable
response = requests.post(URL, headers=custom_headers, data=grant_type_data)

# Verify the contents: ie, print the response to see what we are getting back
# print response.json()

# dump the token in a variable (after extracting the value from the dictionary)
access_token = response.json().get('access_token')

# new custom header that passes the access token to twitter
search_headers = {'Authorization': 'Bearer %s' % (access_token), }

# sending a get request to the twitter search api url with the search term
# and search headers
response = requests.get('https://api.twitter.com/1.1/search/tweets.json?q=%s&count=100'
                        % SEARCH_TERM, headers=search_headers)

# print the response to see what we got
# print response.json()

# make a pretty-print object # *** Uncomment this one to explore options **
# pp = pprint.PrettyPrinter(indent=2)

# print response.json().get('statuses')[0].keys()
# pp.pprint(response.json().get('statuses'))

# print response.json().get('statuses')[0]

# *** Uncomment this one to explore options *******************************
# pp.pprint(response.json().get('statuses')[0])

# profile_image_url, screen_name, created_at, time_zone, location

# === begin actual import stuff ============================================

tweet_list = response.json().get('statuses')

Tweet.objects.all().delete()
for tweet_l in tweet_list:
    try:
        tweet_location = base64.b64encode(tweet_l.get('user').get('location'))
    except Exception, e:
        continue

    if tweet_location is not "" and tweet_location is not None:
        new_tweet, created = Tweet.objects.get_or_create(tweet_text=str(unidecode(tweet_l.get('text'))))

        new_tweet.time_stamp = tweet_l.get('user').get('created_at')

        new_tweet.time_handle = new_tweet.time_stamp.replace(" ", "_")

        new_tweet.screen_name = tweet_l.get('user').get(str(unidecode('screen_name')))
        new_tweet.location = base64.b64decode(tweet_location)
        new_tweet.search_term = SEARCH_TERM

        try:
            new_tweet_image = requests.get(tweet_l.get('user').get('profile_image_url'))
            temp_image = NamedTemporaryFile(delete=True)
            temp_image.write(new_tweet_image.content)
            img_name = "%s_tweet_img.jpg" % new_tweet.time_handle
            new_tweet.profile_image_url.save(img_name, File(temp_image))
        except Exception, e:
            print e

        new_tweet.save()
        print "==============================================================="
        # print new_tweet.tweet_text
        # print new_tweet.time_stamp
        # print new_tweet.screen_name
        # print new_tweet.location



        # print "TWEET-----------------------------------"
        # print tweet.get('user').get('profile_image_url')
