# @PlanetaryBot

This repo contains the `PlanetaryBot.py` script that is used
by @PlanetaryBot to post random, raw images of the Solar System on Twitter.

## Usage

To generate a test tweet:
```
python PlanetaryBot.py test
```

To send an actual tweet:
```
python PlanetaryBot.py
```


## Requirements

This bot only supports Python 3.

You need to add a `secrets.py` file in the same directory containing your
Twitter API secrets.

You will also need the following Python packages:

* twython
* pandas
* astropy
