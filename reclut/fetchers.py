import requests
import youtube_dl
import glob, os, sys
from multiprocessing.pool import ThreadPool
import concurrent.futures
import time
class Downloader(object):
    def __init__(self, Query, directory, archive_file=None):
        self.reddit = Query
        self.directory = directory
        self.archive_file = archive_file
        self.archived = []


    def download_worker(self, args): # Gets mapped as a worker by executor (gets squelched) 
        post, post_num = args
        self.fetch_mimes(post, post_num)


    def download(self, threads):
        if threads == 0 or threads == 1:
            for post, post_num in self.reddit.get_posts():
                self.fetch_mimes(post, post_num)
        else:
            # Quick benchmark:
            #   Multi-threaded(6): 18.5s
            #   Single-threaded: 42.5s
            #with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
            #    executor.map(download_worker, self.reddit.get_posts())
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(self.download_worker, self.reddit.get_posts())


    def fetch_mimes(self, post, post_num):
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
            self.fetch_file(post_num, post.url, post)
        elif "imgur" in post.url and not mime_types["misc"]:
            # TODO: These fail silently (because url-s would 403, etc). It does need a more precise except...
            # This is good at the time of writing; as it passes on missing, deleted, etc. files.
            try:
                tag = post.url.rsplit("/")[-1]
                self.fetch_file(post_num, "https://i.imgur.com/" + tag + ".jpg", post)
            except:
                pass
        elif "gfycat" in post.url and "gfycat" in post_thumbnail_url:
            # TODO: These fail silently (because url-s would 403, etc). 
            # This is good at the time of writing; as it passes on missing, deleted, etc. files.
            try:
                tag = (post_thumbnail_url.rsplit("/")[-1]).rsplit("-")[0]
                url = "https://giant.gfycat.com/" + tag + ".webm"
                self.fetch_file(post_num, url, post)
            except:
                pass
        elif "v.redd.it" in post.url and post_media_dash_url:
            self.fetch_yt_video(post_num, post_media_dash_url, post)
        elif "v.redd.it" in post.url and post_media_fallback_url:
            self.fetch_yt_video(post_num, post_media_fallback_url, post)
        else:
            print(f"#######\nSkipping: {post.url} \n#######\n")


    def fetch_file(self, count, url, post=None):
        try:
            file_name = self.get_filename(count, url, post)
        except IOError:
            return
        with open(os.path.join(self.directory, file_name), "wb+") as handle:
            with requests.get(url, stream=True, timeout=1) as r:
                r.raise_for_status()
                for block in r.iter_content(chunk_size=8192):
                    if not block:
                        break
                    handle.write(block)
                r.close


    def fetch_yt_video(self, count, url, post=None):
        try:
            filename = self.get_filename(count, url, post).strip(".mpd")
        except IOError:
            return
        ydl_opts = {'format':   'dash-VIDEO-1+dash-AUDIO-1',
                    'outtmpl':  f'{filename}',
                    'quiet':    True}
        working_directory = os.getcwd()
        os.chdir(self.directory)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        os.chdir(working_directory)


    def get_filename(self, count, url, post):
        """
        Returns a string formatted as, for example
        001-subreddit-xxxxxxxxxxxx.jpg
        002-funnygifs-djakj431kjdja.gif
        003-user123-BigAwesomeHorse.webm
        """
        if self.archive_file: self.archive(count, url, self.archive_file)

        named = True
        last_piece = url.rsplit("/")[-1]
        extension = self.get_extension(url)
        tag = last_piece.rsplit(extension)[0][:-1]
        if "DASH" in tag:
            tag = url.rsplit("/")[-2][:-1]
        extension = extension.split("?")[0]

        name = ""
        if named:
            name = self.clean_title(post.title)

        file_name = f"{int(count):03d}-{name}-{tag}.{extension}"
        return file_name


    def archive(self, count, url, archive_file):
        if count == 0:
            with open(archive_file, "r") as f:
                for line in f:
                    self.archived.append(line.split("\n")[0])
        if "DASH" in url:
            tag = url.rsplit("/")[-2]
        else:
            last_piece = url.split("/")[-1]
            extension = self.get_extension(url)
            tag = last_piece.rsplit(extension)[0][:-1]
        if tag not in self.archived:
            with open(archive_file, "a") as f:
                f.write(f"{tag}\n")
        else:
            raise IOError('File already downloaded') # Needs refinement


    @staticmethod
    def get_extension(url):
        return url.rsplit("/")[-1].split(".")[-1].split("?")[0]


    @staticmethod
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

