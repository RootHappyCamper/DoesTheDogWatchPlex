from bs4 import BeautifulSoup
import urllib.parse
import requests
import time
import json

use_memcache = False

try:
    from config import dtdd_api_enabled
    try:
        from config import dtdd_api_key
        api_headers = {'Accept' :'application/json', 'X-API-KEY': dtdd_api_key}
        check_request = requests.get('https://www.doesthedogdie.com/dddsearch?q=old%20yeller', headers=api_headers)
        try:
            json.loads(check_request.text)
            print("Connection to DTDD API established. Moving forward...")
        except json.decoder.JSONDecodeError:
            print("Failed to connect to DTDD's official api. Please check your API key.")
            exit(1)
    except ImportError:
        print("API key not set. Please set your API key in config.py.")
        exit(1)
except ImportError:
    dtdd_api_enabled = False
    print("If this has printed, you have run into an unknown error related to importing your API key or connecting to the DTDD official API.")


base_string = "https://www.doesthedogdie.com/{media_id}"

def get_topics(media_id):
    resp = requests.get(base_string.format(media_id=media_id))
    soup = BeautifulSoup(resp.text, 'lxml')
    try:
        return(soup.find("div", {"id": "topics"}).select('.topicRow'))
    except AttributeError:
        print("❌ Could not find topics for {}".format(media_id))
        return []

def get_topics_api(media_id):
    resp = requests.get(base_string.format(media_id=media_id), headers=api_headers)
    resp = json.loads(resp.text)
    return resp.get('topicItemStats')

def get_info(media_id):
    to_return = []
    if dtdd_api_enabled:
        topics = get_topics_api(media_id)
        print(topics)
        for topic in topics:
            print(topic)
            name = topic.get('topic').get('doesName') + "?"
            short_name = topic.get('topic').get('smmwDescription')
            yes_votes = topic.get('yesSum')
            no_votes = topic.get('noSum')
            to_return.append(dict(topic=name, topic_short=short_name, yes_votes=yes_votes, no_votes=no_votes))
    else:
        topics = get_topics(media_id)
        for topic in topics:
            
            name = topic.select('.name>a')[0].text

            # the yesNo container is the little box which highlights red or green for a specific topic

            yesNo = topic.select('.yesNo')[0]

            # extract votes from the yesNo container
            yes_votes = int(yesNo.select('.yes')[0].select('.count')[0].text)
            no_votes = int(yesNo.select('.no')[0].select('.count')[0].text)
            to_return.append(dict(topic=name, yes_votes=yes_votes, no_votes=no_votes))
    return to_return
    
def search(search_string):
    search_string = search_string.lower()
#    search_string = urllib.parse.quote(search_string)
    url = 'https://www.doesthedogdie.com/dddsearch?q={}'.format(search_string)
    search_request = requests.get(url, headers=api_headers)
    resp = json.loads(search_request.text).get('items', [])
    #print(url)
    #print(search_request)
    if len(resp) == 0:
        return None
    return "media/{}".format(resp[0].get('id', None))

    
def get_info_for_movie(movie_name, use_cache=True):
    movie_name = movie_name.lower()
    movie_name = urllib.parse.quote_plus(movie_name)
#    print("Movie name for get info for movie is:" + movie_name)

    print("Looking for " + movie_name)
    key = search(movie_name)
    if key is not None:
        data = get_info(key)
 #       if use_memcache: # this allows us to force refresh data if we want # Old code. Might be useful for SQL database.
 #           client.set(movie_name, json.dumps(dict(data=data, time_retrieved=int(time.time()))))
    else:
        data = None
    return data
