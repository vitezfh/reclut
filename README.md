**recult** - a set of tools for reddit

It's written in Python3 and leverages PRAW, youtube-dl (only for YT videos), concurrent.futures, and requests.

Since reclut is meant for everyday use, a simple config file is available.

# Uses
Currently, reclut can be used for:
- Downloading, media (images, gifs, linked youtube vids with youtube-dl) from subreddits and users
- Blocking users, in bulk (useful as this blocks posts from these users, avoiding downloading them)

# Ambitions and Flaws

This is a tool I hope it will get used regularly once at a fleshed-out, stable state.

It will particularly be useful to those who are:
- with an intermittent internet connection
- working with limited hardware
- into automation or data-hoarding
- looking to reduce their exposure to the internet

Presently, it's at an early stage in development and lacking key features:

Unit tests haven't been written as this evolved from a script I used for fetching wallpapers, back when I didn't know how to code.

It makes sense now, however, to include some basic ones as the project is at a stage where maintaining these is trivial and particularly useful. So, I will be doing that.

No error handling for passed arguments is present. Some arguments aren't enforced.

youtube-dl is a huge library, and is loaded on demand for performance, but I ought to make it optional.

I'm packaging the project manually, so the versioning is slightly out of whack. That's at a low priority as this is yet to be used in scenarios where that would matter.

# Installation

Clone repo and pip install: $ `git clone "https://github.com/vitezfh/reclut" && pip install reclut/`

A default config should be initialized upon installation to your default config folder. Usually `$HOME/.config/reclut/config`

Configure by following: https://praw.readthedocs.io/en/latest/getting_started/authentication.html
  
  **Make a new account for this**, unless you already have one just for this sort of purpose. Your username, password and tokens are all stored in your config folder. I'm thinking of ways to change this.
  
# Examples

To see what actions are available: $ `reclut --help`

Help for individual actions: $ `reclut <action> --help`

To download /r/wallpapers submissions; the top 10 of the past month; 4 at a time, and archive to wallpapers.txt:

$ `reclut download --subreddit wallpapers --sorting top --time year --limit 10 --threads 4 --archive wallpapers.txt`

$ `reclut download -r wallpapers -s top -t year -n 10 -T 4 -A wallpapers.txt`

# Side Notes
This is developed sporadically; interface changes and breakage are to be expected.
