import requests
import youtube_dl
import glob, os, sys


global archived, archive_file

archived = []

def download(args): # Gets mapped as a worker by executor (gets squelched)
    post, post_num, directory, reddit_type = args
    fetch_mimes(post, post_num, directory, reddit_type=reddit_type)


def fetch_mimes(post, post_num, directory, reddit_type=None):
    #print(post.__dict__)
    mime_types = {
        "static_image":     [".jpg", ".png", ".jpeg", ".PNG", ".JPEG", ".JPG"],
        "animated_image":   [".gif"],
        "video":            [".webm"],
        "misc":             [".gifv", "gallery", "/a/"]
    }
    for key in mime_types:
        mime_types[key] = any(map(lambda x: x in post.url, mime_types[key]))
    try:
        post_thumbnail_url = post.media["oembed"]["thumbnail_url"]
    except:
        post_thumbnail_url = None
    try:
        post_media_fallback_url = post.media["reddit_video"]["fallback_url"]
    except:
        post_media_fallback_url = None
    try:
        post_media_dash_url = post.media["reddit_video"]["dash_url"]
    except:
        post_media_dash_url = None
    if mime_types["static_image"] or mime_types["animated_image"]:
        fetch_file(post_num, post.url, directory, post=post, reddit_type=reddit_type)
    elif "imgur" in post.url and not mime_types["misc"]:
        # TODO: These fail silently (because url-s would 403, etc). It does need a more precise except...
        # This is good at the time of writing; as it passes on missing, deleted, etc. files.
        try:
            tag = post.url.rsplit("/")[-1]
            fetch_file(post_num, "https://i.imgur.com/" + tag + ".jpg", directory, post=post, reddit_type=reddit_type)
        except:
            pass
    elif "gfycat" in post.url and "gfycat" in post_thumbnail_url:
        # TODO: These fail silently (because url-s would 403, etc). 
        # This is good at the time of writing; as it passes on missing, deleted, etc. files.
        try:
            tag = (post_thumbnail_url.rsplit("/")[-1]).rsplit("-")[0]
            url = "https://giant.gfycat.com/" + tag + ".webm"
            fetch_file(post_num, url, directory, post=post, reddit_type=reddit_type)
        except:
            pass
    elif "v.redd.it" in post.url and post_media_dash_url:
        fetch_yt_video(post_num, post_media_dash_url, directory, post=post, reddit_type=reddit_type)
    elif "v.redd.it" in post.url and post_media_fallback_url:
        fetch_yt_video(post_num, post_media_fallback_url, directory, post=post, reddit_type=reddit_type)
    else:
        print(f"#######\nSkipping: {post.url} \n#######\n")


def fetch_file(count, url, directory, post=None, reddit_type=""):
    file_name = get_filename(count=count, url=url, post=post, reddit_type=reddit_type)

    with open(os.path.join(directory, file_name), "wb+") as handle:
        with requests.get(url, stream=True, timeout=1) as r:
            r.raise_for_status()
            for block in r.iter_content(chunk_size=8192):
                if not block:
                    break
                handle.write(block)
            r.close


def fetch_yt_video(count, url, directory, post=None, reddit_type=""):
    try:
        filename = (get_filename(count, url, post=post, reddit_type=reddit_type)).strip(".mpd")
    except IOError:
        return
    ydl_opts = {'format':   'dash-VIDEO-1+dash-AUDIO-1',
                'outtmpl':  f'{filename}',
                'quiet':    True}
    working_directory = os.getcwd()
    os.chdir(directory)
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    os.chdir(working_directory)


def archive(func):
    def inner(*args, **kwargs):
        if archive_file == None:
            exit()
        if kwargs["count"] == "0":
            with open(archive_file, "r") as f:
                for line in f:
                    archived.append(line.split("\n")[0])
        last_piece = kwargs["url"].split("/")[-1]
        extension = get_extension(kwargs["url"])
        tag = last_piece.rsplit(extension)[0][:-1]
        if "DASH" in tag:
            tag = kwargs["url"].rsplit("/")[-2]
        if tag not in archived:
            with open(file, "a") as f:
                f.write(f"{tag}\n")
            return func(*args, **kwargs)
        else:
            raise IOError('File already downloaded') # Requires refinement
    return inner


def get_filename(count=0, url="", post=None, reddit_type=""):
    """
    Returns a string formatted as, for example
    001-subreddit-xxxxxxxxxxxx.jpg
    024-funnygifs-djakj431kjdja.gif
    000-user123-BigAwesomeHorse.webm
    """
    named = True
    last_piece = url.rsplit("/")[-1]
    extension = get_extension(url)
    tag = last_piece.rsplit(extension)[0][:-1]
    if "DASH" in tag:
        tag = url.rsplit("/")[-2][:-1]
    extension = extension.split("?")[0]

    name = ""
    if named:
        name = "-" + clean_title(post.title)

    file_name = f"{int(count):03d}-{reddit_type}{name}-{tag}.{extension}"

    return file_name


def get_extension(url):
    return url.rsplit("/")[-1].split(".")[-1].split("?")[0]


def clean_title(title):
    replacement_list = [
        (" - ", "_"),
        ("-", "_"),
        (".", ""),
        (",", ""),
        ("/", ""),
        ("!", ""),
        ("?", ""),
        ("(", ""),
        (")", ""),
        ("[", ""),
        ("]", ""),
        (" ", "_")
    ]
    for to_replace, replacement in replacement_list:
        title = title.replace(to_replace, replacement)
    return title

