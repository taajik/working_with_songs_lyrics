
import argparse
import json
import os

from lyricsgenius import Genius

from file_regularization import auto_regularize
from lyrics_attachment import auto_add_lyrics
from lyrics_manipulation import (
    create_lyrics_file,
    edit_lyrics,
    search_lyrics,
)
import utils


# All instructional texts for parsers are stored in this file:
with open("instructions.json") as insts:
    ts = json.load(insts)

parser = argparse.ArgumentParser(
    prog="lyricser",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["parser"]["desc"]
)
subparsers = parser.add_subparsers(title="Commands", dest="command", metavar="")

def add_common_arguments(parser, **helps):
    # These common arguments are needed for all of the parsres.
    # But the help messages can be customized.
    parser.add_argument("-r", "--recursive", action="store_true",
                        help=helps.get("recursive", ts["common"]["recursive"]))
    parser.add_argument("-I", "--ignore", metavar="PATTERN", type=str,
                        help=helps.get("ignore", ts["common"]["ignore"]))
    parser.add_argument("path", type=str,
                        help=helps.get("path", ts["common"]["path"]))

regular_parser = subparsers.add_parser(
    "regular",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["regular"]["desc"],
    epilog=ts["regular"]["epil"],
    help=ts["regular"]["help"]
)
add_common_arguments(regular_parser)
regular_parser.add_argument("-a", "--auto-names", action="store_true",
                            help=ts["regular"]["args"]["auto_names"])
regular_parser.add_argument("-n", "--no-rename",
                            action="store_false", dest="rename",
                            help=ts["regular"]["args"]["rename"])

set_parser = subparsers.add_parser(
    "set",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["set"]["desc"],
    epilog=ts["set"]["epil"],
    help=ts["set"]["help"]
)
add_common_arguments(set_parser)
set_parser.add_argument("-i", "--is-album", action="store_true",
                        help=ts["set"]["args"]["is_album"])

create_parser = subparsers.add_parser(
    "create",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["create"]["desc"],
    epilog=ts["create"]["epil"],
    help=ts["create"]["help"]
)
add_common_arguments(create_parser)
create_parser.add_argument("-o", "--output-path", dest="lyrics_path",
                           help=ts["create"]["args"]["lyrics_path"])

edit_parser = subparsers.add_parser(
    "edit",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["edit"]["desc"],
    epilog=ts["edit"]["epil"],
    help=ts["edit"]["help"]
)
add_common_arguments(edit_parser)

search_parser = subparsers.add_parser(
    "search",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=ts["search"]["desc"],
    help=ts["search"]["help"]
)
search_parser.add_argument("q_list", nargs="+", metavar="phrase",
                           help=ts["search"]["args"]["q_list"])
add_common_arguments(search_parser, path=ts["search"]["args"]["path"])


if __name__ == "__main__":

    args = parser.parse_args()

    # Print help if the program is run without any arguments.
    if args.command is None:
        parser.print_help()
        raise SystemExit

    assert hasattr(args, "path"), "path argument is required"
    origin_path = utils.format_path(args.path)
    if not utils.is_valid_dir(origin_path):
        print(" X Error: Invalid path!")
        raise SystemExit
    if not next(origin_path.iterdir(), None):
        print(" X Error: The folder is empty!")
        raise SystemExit

    # Regularize songs' tags and filename
    if args.command == "regular":
        auto_regularize(origin_path, args.recursive, args.ignore,
                        args.auto_names, args.rename)
        utils.print_report("modified", "not modified")

    # Search for lyrics in 'Genius.com' and add them to songs.
    elif args.command == "set":
        # genius = Genius(excluded_terms=["(Live)", "(Remix)"])
        genius = Genius(os.environ.get("API_TOKEN"), verbose=False)
        auto_add_lyrics(origin_path, genius, args.recursive,
                        args.ignore,args.is_album)
        utils.print_report("added", "not added")

    # For each folder, generate a text file containing all of its lyrics.
    elif args.command == "create":
        lyrics_path = None
        if args.lyrics_path is not None:
            lyrics_path = utils.format_path(args.lyrics_path)
            if not utils.is_valid_dir(lyrics_path):
                print(" X Error: Invalid lyrics path!")
                raise SystemExit
        create_lyrics_file(origin_path, lyrics_path,
                           args.recursive, args.ignore)
        utils.print_report("created", "not created")

    # Songs' lyrics editor.
    elif args.command == "edit":
        edit_lyrics(origin_path, args.recursive, args.ignore)

    # Search for a phrase in lyrics files.
    elif args.command == "search":
        search_lyrics(origin_path, args.q_list, args.recursive, args.ignore)

    print()
