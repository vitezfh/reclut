from reclut.reddit import reddit


class RedditQuery(object):
    """Processes a 'request' based on the parameters given"""
    def __init__(self, subreddit=None, user=None, limit=10,
                 adult=None, sorting="top", time_filter="year"):
        self.subreddit = subreddit
        self.user = user
        self.limit = limit
        self.adult = adult
        self.sorting = sorting
        self.time_filter = time_filter
        choices = []
        user_posts = []

        if self.user and self.subreddit:
            pass
        elif self.subreddit:
            reddit_sub = reddit.subreddit(subreddit)
            if sorting == "top":
                for submission in reddit_sub.top(limit=limit, time_filter=time_filter):
                    choices.append(submission)
            elif sorting == "hot":
                for submission in reddit_sub.hot(limit=limit):
                    choices.append(submission)
            elif sorting == "new":
                for submission in reddit_sub.new(limit=limit):
                    choices.append(submission)
            elif sorting == "rising":
                for submission in reddit_sub.rising(limit=limit):
                    choices.append(submission)
        elif self.user:
            reddit_user = reddit.redditor(user)
            if sorting == "top":
                for submission in reddit_user.top(limit=limit, time_filter=time_filter):
                    user_posts.append(submission)
            elif sorting == "hot":
                for submission in reddit_user.submissions.hot(limit=limit):
                    choices.append(submission)
            elif sorting == "new":
                for submission in reddit_user.submissions.new(limit=limit):
                    choices.append(submission)

        self.posts = choices

    def get_posts(self):
        """Returns a list of filtered post tuples.
        [
            (Submission(id='7mjw12'), 0),
            (Submission(id='5gn8ru'), 1),
            (Submission(id='7431qq'), 2),
            (Submission(id='7kvjuz'), 3)
        ]
        """
        def generate_posts(posts, adult):
            """Yields posts, filtered by their rating"""
            for post_num, post in enumerate(posts):
                post = posts[post_num]
                if adult == "allowed" or adult == "yes" or adult == "true" or adult == True:
                    yield post, post_num
                elif (post.whitelist_status == "promo_adult_adult" or post.thumbnail == "adult") \
                        and (adult == "only" or adult == "just"):
                    yield post, post_num
                elif (adult == "none" or adult == "safe" or adult == "off" or adult == "" or adult is None) \
                        and post.whitelist_status != "promo_adult_adult" and post.thumbnail != "adult":
                    yield post, post_num

        posts = []
        for post, post_num in generate_posts(self.posts, self.adult):
            print(f"\n#{post_num}: {post.title}\n{post.url}")
            posts.append((post, post_num))
        return posts
