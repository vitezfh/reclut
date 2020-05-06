**recult** - a set of tools for reddit; for data-hoarding and avoidance of interaction with the site.
Can presently be used for downloading media (images, gifs, linked youtube vids with youtube-dl) from subreddits and users.
It downloads concurrently, and with a symple archiving system built in.
There's also a quick command for blocking many users at once (to, for example, to easily avoid downloading their posts)

# Installation

- Clone the repo: `git clone "https://github.com/vitezfh/reclut"`

- An empty config should be initialized upon installation to your default config folder. Usually `$HOME/.config/reclut/config`
- Fill it up by following this: https://praw.readthedocs.io/en/latest/getting_started/authentication.html
  
  **Make a new account for this**, unless you already have one just for this kind of purpose. Your username, password and tokens are all stored in **plaintext**. I'll get around to changing this, but until then.

# Examples

To download /r/wallpapers submissions; the top 10 of the past year; 4 at a time, and archiving to wallpapers.txt:
``


# Side Notes
Decoupling from authentication in PRAW is a priority for the future.
I develop this sporadically; and for my own purposes, meaning that breakage and interface changes are expected.
