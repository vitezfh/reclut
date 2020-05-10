import sys

from reclut.reddit import reddit


def main():
    for user in sys.argv[2:]:
        print(f"blocking {user} ... ")
        try:
            reddit.redditor(user).block()
            print("done\n")
        except:
            print("FAILED\n")
