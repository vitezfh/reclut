import sys

from reclut.reddit import reddit


def main(*args, **kwargs):
    for user in sys.argv[2:]:
        try:
            print(f"blocking {user} ... ")
            reddit.redditor(user).block()
            print("done\n")
        except:
            print("FAILED\n")
