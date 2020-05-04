def get_posts(reddit, directory, reddit_type, adult, limit):


    def post_generator(reddits, adult="none", limit=5):
        adult = adult
        for post_num in range(limit):
            post = reddits[post_num]
            if adult == "allowed" or adult == "yes" or adult == "true" or adult == True:
                yield post, post_num
            elif (adult == "only" or adult == "just") \
                and (post.whitelist_status == "promo_adult_adult" or post.thumbnail == "adult"):
                yield post, post_num
            elif (adult == "none" or adult == "safe" or adult == "off" or adult == "" or adult == None) \
                and post.whitelist_status != "promo_adult_adult" and post.thumbnail != "adult":
                yield post, post_num


    posts = []
    for post, post_num in post_generator(reddit, adult=adult, limit=limit):
        print(f"\n#{post_num}: {post.title}\n{post.url}")
        posts.append((post, post_num, directory, reddit_type))
    return posts
