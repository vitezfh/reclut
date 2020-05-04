from configparser import RawConfigParser
import os
import praw

# TODO: Improve this
config = RawConfigParser()
config.read(f'{os.path.join(os.environ["HOME"], ".config/reclut/config")}')
config = dict(config.items('account-info'))

reddit = praw.Reddit(client_id=config["client_id"], client_secret=config["client_secret"],
                     password=config["password"], user_agent=config["user_agent"],
                     username=config["username"])

def init_reddit(user="", subreddit="", limit=10, sorting="top", time_filter="all", **kwargs):
    choices = []
    user_posts = []
    time = (' | Time filter: ' + time_filter + " ") if time_filter else ""
    if subreddit:
        print(f"## Sub-Reddit: {subreddit} | Posts: {sorting} - {limit}{time}  ##\n")
        if sorting == "top":
            for count, submission in enumerate(reddit.subreddit(subreddit).top(limit=limit, time_filter=time_filter)):
                choices.append(submission)
        elif sorting == "hot":
            for count, submission in enumerate(reddit.subreddit(subreddit).hot(limit=limit)):
                choices.append(submission)
        elif sorting == "new":
            for count, submission in enumerate(reddit.subreddit(subreddit).new(limit=limit)):
                choices.append(submission)
        elif sorting == "rising":
            for count, submission in enumerate(reddit.subreddit(subreddit).rising(limit=limit)):
                choices.append(submission)

    if user:
        print(f"## User: {user} | Posts: {sorting} - {limit}{time} ##\n")
        if sorting == "top":
            for count, submission in enumerate(reddit.redditor(user).top(limit=limit, time_filter=time_filter)):
                user_posts.append(submission)
        elif sorting == "hot":
            for count, submission in enumerate(reddit.redditor(user).submissions.hot(limit=limit)):
                choices.append(submission)
        elif sorting == "new":
            for count, submission in enumerate(reddit.redditor(user).submissions.new(limit=limit)):
                choices.append(submission)

    if user and subreddit:
        print("User + subreddit combo are not supported yet")
        exit()

    return choices
