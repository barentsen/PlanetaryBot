# @PlanetaryBot

This repo contains the `PlanetaryBot.py` script that is used
by [@PlanetaryBot](https://twitter.com/PlanetaryBot) to share random, raw images from the Outer Solar System on Twitter.
This bot is made possible by the API offered by the [Ring-Moon Systems Node](http://pds-rings.seti.org/)
of NASA's Planetary Data System.

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
