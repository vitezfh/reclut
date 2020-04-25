# reclut

Recult is meant to be a set of tools for reddit for data-hoarding, avoiding repetitive actions and your general exposure to their webui;
It can presently be used for downloading media (jpg,gif,webm,etc.) from subreddits and users.
It also downloads concurrently, meaning it can aggressively utilize your bandwidth. There is a built in archiver as well, to reduce repeated downloading. 

The config should be initialized upon installation to your default config folder. Usually .config/reclut/config

So far I've only tested it on linux, and I fully expect it not to work on other platforms until I get to fixing that.

reclut depends heavily on PRAW, so for configuration have a look at https://praw.readthedocs.io/en/latest/getting_started/authentication.html

I plan on decouppling it from PRAW down the road.


I develop this sporadically; and for my own purposes, meaning that breakage and interface changes are expected.
