# Note: this does require music to already be in a two-directory format, of ~/Music/<some text>/<some text>/track-name.file-format
# if the directory depth in ~/Music/ is greater than 2, this script will malfunction.
import os
from tinytag import TinyTag

print("Valid responses:\nY: Rename\nS: Skip album\nN: Do nothing\n")

continuing = False
for (path, directories, files) in os.walk("/home/daboross/Music"):
    if continuing:
        print("\n")
    continuing = False
    split = path.rsplit("/", 2)
    if len(split) < 3:
        continue
    rest = split[0]
    artist = split[1]
    album = split[2]
    for file in files:
        try:
            tag = TinyTag.get(os.path.join(path, file))
        except LookupError as e:
            continue
        if tag.artist is None or tag.artist[:30] == artist[:30] and len(artist) > len(tag.artist):
            new_artist = artist.replace('/', '_')
        else:
            new_artist = tag.artist.replace('/', '_')
        if tag.album is None or tag.artist[:30] == artist[:30] and len(album) > len(tag.album):
            new_album = album.replace('/', '_')
        else:
            new_album = tag.album.replace('/', '_')


        if new_album != album:
            print_album = "({} -> {})".format(album, new_album)
        else:
            print_album = album
        if new_artist != artist:
            print_artist = "({} -> {})".format(artist, new_artist)
        else:
            print_artist = artist

        if new_artist != artist or new_album != album:
            print("{} - {} :: {}".format(print_artist, print_album, file))
            if continuing:
                continue
            response = input("?> ")
            if response.startswith('y'):
                os.makedirs(os.path.join(rest, new_artist, new_album), exist_ok=True)
                os.rename(os.path.join(path, file), os.path.join(rest, new_artist, new_album, file))
            elif response.startswith('sh'):
                continuing = True
            elif response.startswith('s'):
                break
            elif response.startswith('q'):
                exit(0)
