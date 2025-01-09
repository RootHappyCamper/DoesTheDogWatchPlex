Fork of Valknight's original [DoesTheDogWatchPlex](https://github.com/valknight/DoesTheDogWatchPlex) script 

I loved Valknight's idea of adding trigger warnings to Plex descriptions. However, the code didn't correctly interact with DTDD.com's updated API anymore. As a newly expecting father, having easy to find content warnings within Plex will be a huge boon.

# DoesTheDogWatchPlex

> An integration of DoesTheDogDie.com and Plex Media Server

![Demonstration of DoesTheDogWatchPlex using All Dog's Go To Heaven](/screenshots/2.png)
## What does this do?

This modifies the summaries of movies within Plex to contain content warnings from DoesTheDogDie.com.

## Why?
Sometimes, there isn't a theme I want to watch at a given time. Movies don't always clearly communicate what content they have inside of them and while I may be in the mood one day to watch specific content that allows me to think critically of the themes being potrayed, other days I just want to watch a feel good story void of heavy themes. This tool allows users to view at a glance what themes are in a movie without major changes to the Plex interface.

### Original Description: ###
Some of the people using my Plex server (myself included) sometimes go through rough patches, and don't want to stumble into a movie that happens to contain something like, a pet dying, sexual assault, or other things. However, alt-tabbing to DoesTheDogDie.com can get tiresome, so this exists, meaning you can see brief previews of the data from DoesTheDogDie.com without ever leaving the Plex interface.

## What is the web API?

The Web API is provided directly by [DoesTheDogDie.com](https://www.doesthedogdie.com/api). You will have to create an account and find your API token on your profile page. Once you do you will have to copy and paste your API token into the config.py file under dtdd_api_key.

## How to get started (CLI tools)

0. Install python 3.12+ and create a virtual environment for this
1. Execute `pip install -r requirements.txt`
2. Copy config.yml.template to config.yml, and fill out the data with what is relevant to your setup
3. Execute `python build_json.py`, and sit back and wait for the movies.json file to be generated 
4. Once this file is generated, check over it, and **make a Plex Media Server database backup** (from this point on, all metadata changes will be permanent to your server)
5. Run `python write_to_plex.py`

To update the content warnings, run build_json.py again, and then write_to_plex.py - anything below the line reading `Content Warnings: ` will simply be removed, and replaced with the new updated content warnings (anything above shouldn't be touched)

## Plans

- [X] Cleaning up original code to remove memcaching via Flask app
- [ ] Adding SQL database so API doesn't have to be called for every movie every time script is run
- [ ] Deployment via Docker container
- [ ] Allow user to run daily, weekly, or on a set schedule
- [ ] Allow user to only be warned about content they specficy instead of all "yes's" from doesthedogdie.com
- [ ] Jellyfin Support
- [ ] ~~IMDB parental support~~ IMDB API seems to be a paid for service
- [ ] TV Series Support

## LICENSE

This project is licensed under the MIT license.

## Credit
[Valknight](https://github.com/valknight) for the original script and idea <br />
[Yacn](https://github.com/yacn) for original dockerfile for Valknight's script <br /> 
