
import fnmatch
import re

from song import Song
from utils import report, get_header, format_lyrics


def get_song_lyrics(t, aa, genius):
    """Search for lyrics of a song in Genius
    according to its title and artist.
    """

    if t is None:
        print("X Title not found.")
        t = input("  title: ")
    else:
        t = re.sub(" \(.*\)", "", t)
    if aa is None:
        print("X Artist not found.")
        aa = input("  artist: ")

    try:
        # lyrics = genius.lyrics( input(f"{t} - {aa}\n  url: ") )
        song = genius.search_song(t, aa, get_full_info=False)
        print(song.path)
        lyrics = song.lyrics
    except KeyboardInterrupt:
        raise SystemExit

    return lyrics


def auto_add_lyrics(path, genius, recursive=False, ignore_ptrn=None,
                    is_album=False):
    """Loop through the songs in one folder and add lyrics to them."""

    print(get_header(path))
    inner_folders = []

    if is_album:
        folder = path.name.split(" - ")
        if len(folder) == 2:
            try:
                print(" Searching for album lyrics...")
                # album = genius.search_album(album_id=, get_full_info=False)
                album = genius.search_album(folder[1], folder[0],
                                            get_full_info=False)
                print(album.url)
            except KeyboardInterrupt:
                raise SystemExit

    i = 0
    for file in sorted(path.iterdir()):
        if ignore_ptrn and fnmatch.fnmatch(file.name, ignore_ptrn):
            continue
        if file.is_file():# and " - " in path.name:
            print("\n" + str(i+1).rjust(3), end=". ")

            try:
                song = Song(file)
            except Exception as e:
                report(False, e)
                return
            t = song.title
            aa = song.album_artist
            print(f'"{t}" by {aa}')

            # Get the lyrics of this song.
            success_msg = "Done."
            try:
                if is_album:
                    trk = album.tracks[i].song
                    # Make sure the correct lyrics is being put on the song.
                    if trk.title.replace("’", "'").casefold() != t.casefold():
                        success_msg = f"Done. {trk.title} added."
                    lyrics = trk.lyrics
                else:
                    lyrics = get_song_lyrics(t, aa, genius)
            except Exception as e:
                report(False, f" X Lyrics Error: {e}")
                continue
            lyrics = format_lyrics(lyrics)

            # Set the lyrics and save the file.
            try:
                song.lyrics = lyrics
                song.save()
                report(True, success_msg)
            except Exception:
                report(False, " X Lyrics Error.")
            i += 1

        # if 'file' is a folder, store it to call the function on it later.
        elif file.is_dir():
            inner_folders.append(file)
    print()

    # Call the function again for folders inside this one.
    if recursive:
        for inner_path in inner_folders:
            auto_add_lyrics(inner_path, genius, recursive,
                            ignore_ptrn, is_album)
