**recult** - a set of tools for reddit; for data-hoarding and avoidance of interaction with the site.
Can presently be used for downloading media (images, gifs, linked youtube vids with youtube-dl) from subreddits and users.
It downloads concurrently, and with a symple archiving system built in.
There's also a quick command for blocking many users at once (to easily avoid downloading their posts, for example)

# Installation

- Clone repo and pip install: $ `git clone "https://github.com/vitezfh/reclut" && pip install reclut/`

- A default config should be initialized upon installation to your default config folder. Usually `$HOME/.config/reclut/config`
- Configure by following: https://praw.readthedocs.io/en/latest/getting_started/authentication.html
  
  **Make a new account for this**, unless you already have one just for this sort of purpose. Your username, password and tokens are all stored in **plaintext**. I'll get around to changing this, but until then.

# Examples

To see what actions are available: $ `reclut --help`

Help for individual actions: $ `reclut <action> --help`

To download /r/wallpapers submissions; the top 10 of the past month; 4 at a time, and archive to wallpapers.txt:

$ `reclut download --subreddit wallpapers --sorting top --time year --limit 10 --threads 4 --archive wallpapers.txt`

$ `reclut download -r wallpapers -s top -t year -n 10 -T 4 -A wallpapers.txt`

# Side Notes
This is developed sporadically; interface changes and breakage are to be expected.
