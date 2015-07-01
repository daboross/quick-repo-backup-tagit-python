import os
from tinytag import TinyTag

print("Valid responses:\nY: Rename\nSh: Skip album, but show all possibilities\nS: Skip album\nQ: Quit\nN: Do nothing\n")

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
    for file in sorted(files):
        try:
            tag = TinyTag.get(os.path.join(path, file))
        except LookupError as e:
            continue

        if file.startswith("02"):
            # we can't actually get the disk number - but in the case this is being used, all files which have two disks
            # and are on the second disk are already in the right name format - so let's ignore them. The files who's names
            # start with 02 and aren't the second disk of an album have to be dealt with manually before running
            continue

        # format example
        # 01.07 - Gazette.ogg

        new_file_name = "01.{} - {}{}".format(
            tag.track.zfill(2),
            tag.title.replace('/', '_'),
            os.path.splitext(file)[1],
        )

        if new_file_name[:38] == file[:38] and len(file) > len(new_file_name):
            continue

        if file != new_file_name:
            print("{} - {}:\n\t{} -> {}".format(artist, album, file, new_file_name))
            if continuing:
                continue
            response = input("?> ")
            if response.startswith('y'):
                os.rename(os.path.join(path, file), os.path.join(path, new_file_name))
            elif response.startswith('sh'):
                continuing = True
            elif response.startswith('s'):
                break
            elif response.startswith('q'):
                exit(0)