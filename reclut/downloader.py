from reclut.reddit import init_reddit
from reclut.fetchers import fetch_file, fetch_yt_video, fetch_mimes, download
from reclut.posts import get_posts

#"config file is stored in $HOME/.config/reclut/config"

import requests
import glob, os, sys
import youtube_dl
import argparse

from time import time

from multiprocessing.pool import ThreadPool
import concurrent.futures

global archive_file


def main(*args, **kwargs):

    p = argparse.ArgumentParser(prog="reclut download",
                                description="Downloads media from subreddit or user, according to options",
                                epilog="Needs authorization, see github.com/vitezfh/reclut")
    p.add_argument("-r", "--subreddit",       help="subreddit to fetch from",                        type=str)
    p.add_argument("-u", "--user",            help="user to fetch from, doesn't yey work with --subreddit",
                                                                                                     type=str)
    p.add_argument("-n", "--limit",           help="limit number of posts to fetch, defaults to 10", type=int)
    p.add_argument("-d", "--directory",       help="directory to store into",                        type=str)
    p.add_argument("-a", "--adult", "--nsfw", help="nsfw: none, allowed or only. Defaults to none",  type=str)
    p.add_argument("-s", "--sorting",         help="sorting: top, hot or rising. Defaults to top",   type=str)
    p.add_argument("-t", "--time-filter",     help="only if sorting by top: 'all', 'month', 'year' (default)",
                                                                                                     type=str)
    p.add_argument("-A", "--archive",         help="<path> to archive file [NOT WORKING]",                         type=str)
    p.add_argument("--dry-run",               help="skips downloading",                 action="store_true")
    p.add_argument("-v", "--verbose",         help="increases output verbosity",        action="store_true")
    args = p.parse_args(*args, **kwargs)
    #setup_args() # Look into this

    archive_file = None
    if args.archive:
        archive_file = args.archive

    reddit_kwargs = {}
    for key in vars(args):
        value = vars(args)[key]
        if value:
            reddit_kwargs[key] = value

    if args.subreddit:
        reddit_kwargs["subreddit"] = args.subreddit
        reddit_kwargs["reddit_type"] = args.subreddit

    if args.user and not args.subreddit:
        reddit_kwargs["user"] = args.user
        reddit_kwargs["reddit_type"] = args.user
    elif args.user and args.subreddit:
        raise IOError("Not implemented")

    if args.adult:
        reddit_kwargs["adult"] = args.adult
    else:
        reddit_kwargs["adult"] = None

    verbose = True
    if args.verbose:
        verbose = args.verbose

    limit = None
    if args.limit:
        limit = args.limit
    reddit_kwargs["limit"] = limit

    if args.sorting:
        reddit_kwargs["sorting"] = args.sorting
    else:
        reddit_kwargs["sorting"] = "top"

    if args.time_filter:
        reddit_kwargs["time_filter"] = args.time_filter
    if not args.time_filter and reddit_kwargs["sorting"] == "top":
        reddit_kwargs["time_filter"] = "all"

    dry_run = False
    if args.dry_run:
        dry_run = True # Corresponds to --dry-run

    directory = None
    if args.directory:
        directory = args.directory
    ######################
    #   Init directory   #
    #                    #

    if "user" in reddit_kwargs:
        if not args.directory:
            directory = reddit_kwargs["user"]
    else:
        if not args.directory:
            directory = reddit_kwargs["subreddit"]
    reddit_kwargs["directory"] = directory

    if not dry_run:
        if not os.path.isabs(directory):
            directory = os.path.join(os.getcwd(), directory)
        if not os.path.exists(directory):
            os.makedirs(directory)

    reddit = init_reddit(**reddit_kwargs)

    # Quick benchmark:
    #   Multi-threaded(6): 18.5s
    #   Single-threaded: 42.5s
    if not dry_run:
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
            executor.map(download, get_posts(reddit, directory,
                                             reddit_kwargs["reddit_type"],
                                             reddit_kwargs["adult"],
                                             limit))

