Fork of Valknight's original DoesTheDogWatchPlex script https://github.com/valknight/DoesTheDogWatchPlex

I loved Valknight's idea of adding trigger warnings to Plex descriptions. However, the code was a bit outdated and didn't correctly interact with DTDD.com's updated API anymore. As a newly expecting father, having easy to find content warnings within Plex will be a huge boon.

# DoesTheDogWatchPlex

> An integration of DoesTheDogDie.com and Plex Media Server

![Demonstration of DoesTheDogWatchPlex using Marvel's Infinity War](/screenshots/1.png)
## What does this do?

This modifies the summaries of movies within Plex to contain content warnings from DoesTheDogDie.com.

## Why?

Some of the people using my Plex server (myself included) sometimes go through rough patches, and don't want to stumble into a movie that happens to contain something like, a pet dying, sexual assault, or other things. However, alt-tabbing to DoesTheDogDie.com can get tiresome, so this exists, meaning you can see brief previews of the data from DoesTheDogDie.com without ever leaving the Plex interface.

## What is the web API?

To speed up requests, a web API wrapper can be used - this is so that, if many different versions of this app are hitting the same API, only one request will need to hit the original DTDD, without having all the different versions have access to the memcache. It also means other tools that wish to use DTDD can also call upon the API, whether that be a proper Plex agent, or some other tool for you Jellyfin weirdos.

## How to get started (CLI tools)

0. Install python 3.4+ and create a virtual environment for this
1. Execute `pip install -r requirements.txt`
2. Copy config.py.example to config.py, and fill out the data with what is relevant to your setup
3. Execute `python build_json.py`, and sit back and wait for the movies.json file to be generated 
4. Once this file is generated, check over it, and **make a Plex Media Server database backup** (from this point on, all metadata changes will be permanent to your server)
5. Run `python write_to_plex.py`

To update the content warnings, run build_json.py again, and then write_to_plex.py - anything below the line reading `doesthedogdie: ` will simply be removed, and replaced with the new updated content warnings (anything above shouldn't be touched)

## Plans

- TV series support
- Cleaning up original code to remove memcaching via Flask app
- Adding SQL database so API doesn't have to be called for every movie every time script is run
- Deployment via Docker container
- Allow user to run daily, weekly, or on a set schedule
- Jellyfin support
- IMDB parental support

## LICENSE

This project is licensed under the MIT license.
