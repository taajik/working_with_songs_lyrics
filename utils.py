
from pathlib import Path
import re


# Number of
_successful = 0
_unsuccessful = 0


def report(is_successful, message=""):
    """Count the number of successful and
    unsuccessful lyrics attachments.
    """

    global _successful, _unsuccessful
    if is_successful:
        _successful += 1
    else:
        _unsuccessful += 1

    if message:
        print(message)


def print_report(suc_title, unsuc_title):
    print(
        f"\n\n\n {suc_title}: {_successful}"
        f"\n {unsuc_title}: {_unsuccessful}"
    )


def format_path(path):
    path = path.strip(" '\"").replace("'\\''", "'")
    path = Path(path).expanduser().resolve()
    return path


def is_valid_dir(path):
    if (not isinstance(path, Path)
        or not path.is_dir()
        or path.samefile("/")
        or path.samefile(Path())
        or path.samefile(Path.home())):
        return False
    return True


def get_header(path, full_path=True):
    files_num = sum(file.is_file() for file in path.iterdir())
    title = path.name
    if full_path:
        title = str(path)
    return (f"\n┌─{'─'*len(title)}─┐" +
            f"\n│ {title} │ {files_num}" +
            f"\n└─{'─'*len(title)}─┘")


def format_lyrics(lyrics: str):
    """Tidy up the lyrics befor adding them to songs."""

    lyrics = lyrics.replace("[?]", "")
    lyrics = lyrics.replace("You might also like", "")
    lyrics = re.sub("^.*Lyrics", "", lyrics)
    lyrics = re.sub("See [\w ]+ LiveGet tickets as low as \$\d*", "", lyrics)
    lyrics = re.sub("\n*\[", "\n\n[", lyrics).strip()
    lyrics = lyrics.replace("\n\n\n", "\n\n")
    lyrics = lyrics.replace("’", "'").replace(" ", " ")
    lyrics = re.sub("\d*Embed$", "", lyrics)
    return lyrics
