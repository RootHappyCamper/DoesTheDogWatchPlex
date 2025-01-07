from apis.plex import write_data
import json
from tqdm import tqdm


def get_movies_from_json():
    with open("movies.json", "r") as f:
        return json.loads(f.read())


if __name__ == "__main__":
    print("✏ Writing update values from movies.json to Plex")
    for movie in tqdm(get_movies_from_json()):
        if movie['desc'] in "Content Warnings:":
            print("Movie" + movie['title'] + "already has content warnings. skipping...")
            tqdm+1
        else:
            print("Adding content warnings for movie: " + movie['title'])
            write_data(movie)

    print("✅ All done!")
