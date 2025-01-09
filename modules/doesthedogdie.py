import urllib.parse
import requests
# import time
import json
from modules.config import load_config_yaml
# import yaml

try:
    config_data = load_config_yaml()
    dtdd_api_key = config_data['dtdd']['key']
    api_headers = {'Accept' :'application/json', 'X-API-KEY': dtdd_api_key}
    check_request = requests.get('https://www.doesthedogdie.com/dddsearch?q=old%20yeller', headers=api_headers)
    try:
        json.loads(check_request.text)
        print("Connection to DTDD API established. Moving forward...")
    except json.decoder.JSONDecodeError:
        print("Failed to connect to DTDD's official api. Please check your API key.")
        exit(1)
except ImportError:
    print("API key not set. Please set your DTDD API key in config.yml.")
    exit(1)

base_string = "https://www.doesthedogdie.com/{media_id}"


def get_topics_api(media_id):
    resp = requests.get(base_string.format(media_id=media_id), headers=api_headers)
    resp = json.loads(resp.text)
    return resp.get('topicItemStats')

def get_info(media_id):
    to_return = []
    topics = get_topics_api(media_id)
#        print(topics)
    for topic in topics:
#            print(topic)
        name = topic.get('topic').get('doesName') + "?"
        short_name = topic.get('topic').get('smmwDescription')
        yes_votes = topic.get('yesSum')
        no_votes = topic.get('noSum')
        to_return.append(dict(topic=name, topic_short=short_name, yes_votes=yes_votes, no_votes=no_votes))
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
#    print("Looking for " + movie_name)
    key = search(movie_name)
    if key is not None:
        data = get_info(key)
 #       if use_memcache: # this allows us to force refresh data if we want # Old code. Might be useful for SQL database.
 #           client.set(movie_name, json.dumps(dict(data=data, time_retrieved=int(time.time()))))
    else:
        data = None
    return data
