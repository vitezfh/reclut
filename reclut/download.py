# config file is stored in $HOME/.config/reclut/config
import argparse
import os

from reclut.reddit_query import RedditQuery


def main(*args, **kwargs):
    p = argparse.ArgumentParser(prog="reclut download",
                                description="Downloads media from subreddit or user, according to options",
                                epilog="Needs authorization, see github.com/vitezfh/reclut")
    add_arg = p.add_argument
    p.add_argument("-r", "--subreddit",
                   help="subreddit to fetch from", type=str)
    p.add_argument("-u", "--user",
                   help="user to fetch from, doesn't yey work with --subreddit", type=str)
    p.add_argument("-n", "--limit",
                   help="limit number of posts to fetch, defaults to 10", type=int)
    p.add_argument("-d", "--directory",
                   help="directory to store into", type=str)
    p.add_argument("-a", "--adult", "--nsfw",
                   help="nsfw: none, allowed or only. Defaults to none", type=str)
    p.add_argument("-s", "--sorting",
                   help="sorting: top, hot or rising. Defaults to top", type=str)
    p.add_argument("-t", "--time",
                   help="only if sorting by top: 'all', 'month', 'year' (default)", type=str)
    p.add_argument("-T", "--threads",
                   help="num of simultaneous downloads, defaults to 5", type=int)
    p.add_argument("-A", "--archive",
                   help="<path> to archive file", type=str)
    p.add_argument("--dry-run",
                   help="skips downloading", action="store_true")
    p.add_argument("-q", "--quiet",
                   help="silent, doesn't print to stdout", action="store_true")
    args = p.parse_args(*args, **kwargs)
    # setup_args() # Look into this

    reddit_kwargs = {}

    if args.subreddit:
        reddit_kwargs["subreddit"] = args.subreddit

    if args.user and not args.subreddit:
        reddit_kwargs["user"] = args.user

    if args.adult:
        reddit_kwargs["adult"] = args.adult

    quiet = False
    if args.quiet:
        quiet = args.quiet

    if args.limit:
        reddit_kwargs["limit"] = args.limit

    if args.sorting:
        reddit_kwargs["sorting"] = args.sorting
    else:
        reddit_kwargs["sorting"] = "top"

    if args.time:
        reddit_kwargs["time_filter"] = args.time
    if not args.time and reddit_kwargs["sorting"] == "top":
        reddit_kwargs["time_filter"] = "all"

    # Download-specific settings #
    download_kwargs = {}
    if args.archive:
        download_kwargs["archive_file"] = args.archive

    threads = 5
    if args.threads:
        threads = args.threads

    dry_run = False
    if args.dry_run:
        dry_run = True

    # Init directory #
    directory = None
    if args.directory:
        directory = args.directory
    if "user" in reddit_kwargs:
        if not args.directory:
            directory = reddit_kwargs["user"]
    else:
        if not args.directory:
            directory = reddit_kwargs["subreddit"]

    reddit_query = RedditQuery(**reddit_kwargs)

    if not dry_run:
        if not os.path.isabs(directory):
            directory = os.path.join(os.getcwd(), directory)
        if not os.path.exists(directory):
            os.makedirs(directory)
        from reclut.downloader import Downloader
        Downloader(reddit_query, directory, **download_kwargs).download(threads)
