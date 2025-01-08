from apis.doesthedogdie import get_info_for_movie
from apis.plex import get_movies_and_format
import json
import requests
import urllib.parse
import argparse

from tqdm import tqdm

use_memcache = False
use_dtdd_web_api = False
only_show_yes = True

#Arguement Parsing
parser = argparse.ArgumentParser(description="Add content warnings to Plex descriptions using data from DoesTheDogDie.com")

parser.add_argument("-u", "--update-all", action='store_true', help="Forces the script to update all movies found in Plex, instead of skipping movies already found.")
parser.add_argument("-v", "--verbose", action='store_true', help="Prints debugging messages to console")

args = parser.parse_args()

if args.verbose:
    print("Verbose mode enabled")
if args.update_all:
    print("Updating all items in library")

try:
    from config import use_short_names
except:
    print("⚠ Please set use_short_names in your config.py")
    use_short_names = False


def yes_or_no_formatter(topic):
    action = "Unsure"
    
    if topic['yes_votes'] > topic['no_votes']:
        action = "Yes"
    elif topic['no_votes'] > topic['yes_votes']:
        action = "No"
    return "{topic} : {action} (Yes: {yes_votes} | No : {no_votes})\n".format(topic=topic['topic'], yes_votes=topic['yes_votes'], no_votes=topic['no_votes'], action=action), action, topic['topic_short']

def main():
    movies_in_list=0
    movies_found=0
    print("⬇ Getting movies from Plex")
    movies = get_movies_and_format()
    to_write = []
    print("🐶 Getting data from DoesTheDogDie.com")
    for movie in tqdm(movies):
        if args.update_all is not True:
            if movie['has_tag'] == "True":
                if args.verbose is True:
                    print("Movie " + movie['title'] + " already has content warning. Skipping...")
                continue
        movies_in_list += 1
        if args.verbose is True:
            print("Running get info for movie on " + movie['title'])
        movie['dtdd'] = get_info_for_movie(movie['title'])
        movie['statuses'] = []
        if movie['dtdd'] != None:
            movies_found += 1
            for raw_status in movie['dtdd']:
                yes_or_no = yes_or_no_formatter(raw_status)
                if (not only_show_yes) or (yes_or_no[1] == "Yes"):
                    movie['statuses'].append(yes_or_no)
        to_write.append(movie)

    # all we need to do now is chuck it in a big ol' json file
    print("Found " + str(movies_found) + " Movies out of " + str(movies_in_list))
    print("✏ Writing to JSON file")
    with open("movies.json", "w") as f:
        f.write(json.dumps(to_write, indent=4))
    print("✅ Done!")


if __name__ == "__main__":
    main()
