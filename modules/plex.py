from plexapi.server import PlexServer
from modules.config import load_config_yaml
#import yaml
#from config import token, url
plex_url = None
plex_token = None

try: #Try importing keys and url from YAML configuration.
    config_data = load_config_yaml()
    plex_token = config_data['plex']['token']
    if plex_token == None:
        raise Exception("The token retrieved from the YAML file is empty!")
    plex_url = config_data['plex']['url']
    if plex_url == None:
        raise Exception("The token retrieved from the YAML file is empty!")
    plex = PlexServer(plex_url, plex_token)
except Exception as e:
    print(f"Ran into exception... Something is wrong with Plex loading configuration from YAML: {e}" )
    exit(1)
except:
    print("Ran into an unknown exception while importing yaml configuration file for Plex...")
    exit(1)

def get_movie_libraries():
#    plex_library_list = plex.library.sections()
    plex_movie_library_ids = [int(str(section).split(':')[1]) for section in plex.library.sections() if "MovieSection" in str(section)]
    return plex_movie_library_ids

def get_movies(library_id):
    movie_list = []
    working_library = plex.library.sectionByID(library_id)
    print("Requesting movies from {}".format((str(working_library).split(':')[2]).replace(">","").replace("-"," ")))
    for video in working_library.search():
        movie_list.append(video)
    return movie_list

def get_movies_and_format():
    movies = []
    has_tag_counter = 0
    movie_counter = 0
    for library in get_movie_libraries():
        for movie in get_movies(library):
            if "Content Warnings:" in movie.summary:
                has_tag = "True"
                has_tag_counter += 1
            else:
                has_tag = "False"
            movies.append(dict(library=library, key=movie.key, title=movie.title, desc=movie.summary, has_tag = has_tag))
            movie_counter += 1
    print(f"Grabbed {movie_counter} movies from Plex. {has_tag_counter} of them already have content warnings.")
    return movies


def write_data(movie):
    # the value movie should be structured like one generated by build_json.py
    working_library = plex.library.sectionByID(movie['library'])
    desc_cut = movie['desc'].split("\r\n\r\nContent Warnings: \r\n\r\n")[0] #Removes Content Warnings if it is already there. Useful for ensuring there isn't duplication, and for update-all arg
    statuses = []
    if len(movie['statuses']) == 0:
        ddtd_status = "No content warnings could be retrieved for this film\nThis means either this film is fine, or it isn't present on DTDD"
    else:
        for status in movie['statuses']:
            if status[1] == "Yes":
                statuses.append(status[2])
        statuses.sort()
        ddtd_status = "This may contain: {}".format(', '.join(statuses))
    movie['desc'] = "{}\r\n\r\nContent Warnings: \r\n\r\n{}".format(desc_cut, ddtd_status)
    movie['id']=movie['key'].strip('/library/metadata/')
    working_movie = working_library.search(id=movie['id'])[0]
    try:
        working_movie.editSummary(movie['desc'])
    except:
        print("There was an error writing the movie description for Movie:" + movie['title'])

if __name__ == "__main__":
    # for testing only
    # show all movie libraries

    print("🎬 Film library IDs")
    for library in get_movie_libraries()[0]:
        print(library['key'])
