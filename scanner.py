import sys
import os
import re
import pymongo
import pymongo.errors

path = sys.argv[1]

try:
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["test_songs"]
except pymongo.errors.PyMongoError as e:
    print(e)


pattern = re.compile(r'(?P<tag>[a-zA-Z0-9a-яА-ЯёЁ ]+?)/(?P<artist>[a-zA-Z0-9a-яА-ЯёЁ ]+?)/(?P<title>[a-zA-Z0-9a-яА-ЯёЁ ]+?).mp3$')


def scan_and_insert(path):
    count = 0  # quantity of added songs
    for d, dirs, files in os.walk(path):
        for file in files:
            if '.mp3' in file:
                song_path = os.path.join(d, file)
                m = pattern.search(song_path)
                song = {
                    'title': m.group('title'),
                    'artist': m.group('artist'),
                    'filename': song_path,
                    'tag': m.group('tag'),
                    'playlists': ['all']
                }
                try:
                    mycol.insert_one(song)
                    count += 1
                except:
                    print("Some problem to add record into Mongodb.")

    if count:
        print("{} songs were successfully added to Mongodb".format(count))
    else:
        print("There is nothing to add. Please check path of scanning directory.")


if __name__ == '__main__':
    scan_and_insert(path)
