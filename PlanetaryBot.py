"""Posts a random image from the PDS Planetary Rings Node using their API.

Usage
-----
To generate a test status without posting to Twitter:

    $ python planetarybot.py test

To send a real tweet:

    $ python planetarybot.py
"""
import sys
import random
import json
from urllib.request import urlopen, urlretrieve
from astropy.time import Time
import pandas as pd

from twython import Twython
from secrets import *


# Index of images obtained manually though the OPUS search interface
IMAGES = pd.read_csv('opus-images.csv')

NICE_MISSION_NAMES = {'VG1': 'Voyager 1',
                      'VG2': 'Voyager 2',
                      'HST': 'Hubble',
                      'GO': 'Galileo',
                      'CO': 'Cassini',
                      'NH': 'New Horizons'}
NICE_TARGET_NAMES = {'S RINGS': 'Rings of Saturn',
                     'J RINGS': 'Rings of Jupiter',
                     'N RINGS': 'Rings of Neptune'}


def select_image():
    """Select a random image from the PDS Planetary Rings Node."""
    # First randomly select a mission to avoid all tweets being from
    # Cassini, which dominates the dataset.
    missions = set(IMAGES['Instrument Host Name'])
    missions.remove('HST')  # Show images from deep space missions only (sorry Hubble)
    missions.remove('NH')  # New Horizons pre-Pluto data is a bit dull?
    mask_mission = IMAGES['Instrument Host Name'] == random.sample(missions, 1)[0]
    # Having selected a mission, select a random image from that mission
    idx = random.randint(0, mask_mission.sum())
    return IMAGES[mask_mission].iloc[idx]


def get_preview_image(observation_id):
    """Download a full-sized preview image for a given observation ID."""
    metadata_url = ('http://pds-rings-tools.seti.org/opus/api/image/med/'
                    '{}.json'.format(observation_id))
    jsonstr = urlopen(metadata_url).read().decode('utf-8')
    jsonobj = json.loads(jsonstr)['data'][0]
    image_url = jsonobj['path'] + jsonobj['img']
    print('Downloading {}'.format(image_url))
    image_path, msg = urlretrieve(image_url)
    return image_path


def generate_tweet():
    """Returns a status message and path to a JPG."""
    img = select_image()
    timestr = img['Observation Time 1 (UTC)']
    if timestr.count('-') < 2:  # Sometimes day of year notation is used
        isotime = Time(timestr.replace('-', ':').replace('T', ':'),
                       format='yday').iso
    else:
        isotime = timestr
    try:
        target = NICE_TARGET_NAMES[img['Intended Target Name']]
    except KeyError:
        target = img['Intended Target Name'].title()
    try:
        mission = NICE_MISSION_NAMES[img['Instrument Host Name']]
    except KeyError:
        mission = img['Instrument Host Name']
    url = ("http://pds-rings-tools.seti.org/opus#/view=detail"
           "&detail={}".format(img['Ring Observation ID']))
    status = ('📷 {}\n'
              '🛰 {}\n'
              '🗓 {}\n'
              '🔗 {}'.format(target,
                            mission,
                            isotime[:19].replace('T', ' '),
                            url))
    img_path = get_preview_image(img['Ring Observation ID'])
    return (status, img_path)


def post_tweet(status, gif):
    """Post an animated gif and associated status message to Twitter."""
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    upload_response = twitter.upload_media(media=open(gif, 'rb'))
    response = twitter.update_status(status=status, media_ids=upload_response['media_id'])
    print(response)
    return twitter, response


if __name__ == '__main__':
    attempt_no = 0
    while attempt_no < 5:
        attempt_no += 1
        try:
            status, jpg = generate_tweet()
            if 'test' in sys.argv:
                print(status)
                print('Running in test mode -- not posting to Twitter.')
            else:
                twitter, response = post_tweet(status, jpg)
            break
        except Exception as e:
            print(e)
