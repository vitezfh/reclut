import concurrent.futures
import os
import requests
from reclut.utils import get_extension, sanitize_title
from bs4 import BeautifulSoup


class Downloader(object):
    """Downloads reddit posts, given a reddit_query object"""

    def __init__(self, reddit_query, directory, archive_file=None):
        self.reddit = reddit_query
        self.directory = directory
        self.archive_file = archive_file
        self.archived = []
        self.download_yt = False

    def _download_worker(self, args):  # Gets mapped as a worker by executor (gets squelched)
        post, post_num = args
        self._fetch_mime(post, post_num)

    def download(self, threads):
        if threads == 0 or threads == 1:
            for post, post_num in self.reddit.get_posts():
                self._fetch_mime(post, post_num)
        else:
            # Quick benchmark:
            #   Multi-threaded(6): 18.5s
            #   Single-threaded: 42.5s
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
                executor.map(self._download_worker, self.reddit.get_posts())

    def _fetch_mime(self, post, post_num):
        """Determines a the type of mime in reddit post, and uses appropriate method to fetch"""
        mime_types = {
            "static_image": [".jpg", ".png", ".jpeg", ".PNG", ".JPEG", ".JPG"],
            "animated_image": [".gif"],
            "video": [".webm", ".mp4"],
            "misc": [".gifv", "gallery", "/a/"]
        }
        # Sets e.g. mime_types["video"] to True and the rest to False if applicable
        for key in mime_types:
            mime_types[key] = any(map(lambda x: x in post.url, mime_types[key]))
        # Fetches direct links to media files
        if mime_types["static_image"] or mime_types["animated_image"] or mime_types["video"]:
            self._download(post_num, post.url, post)
        # Fetches imgur jpegs
        elif "imgur" in post.url and not mime_types["misc"]:
            tag = post.url.rsplit("/")[-1]
            self._download(post_num, "https://i.imgur.com/" + tag + ".jpg", post)
        elif "gfycat" in post.url and "gfycat" in post.media["oembed"]["thumbnail_url"]:
            tag = (post.media["oembed"]["thumbnail_url"].rsplit("/")[-1]).rsplit("-")[0]
            url = "https://giant.gfycat.com/" + tag + ".webm"
            self._download(post_num, url, post)
        # Like gfycat but for nfsw webms. Needs testing
        elif "redgifs" in post.url:  # and "redgifs" in post_thumbnail_url
            tag = post.url.rsplit("/")[-1]
            # TODO: Add higher quality parameter flag. Because there's also a #mp4Source
            soup = BeautifulSoup(requests.get("https://www.gifdeliverynetwork.com/" + tag).text, features="html.parser")
            url = soup.select_one('#webmSource')['src']
            self._download(post_num, url, post)
        # Fetches integrated reddit videos using youtube-dl
        elif "v.redd.it" in post.url and post.media["reddit_video"]["dash_url"]:
            self._yt_download(post_num, post.media["reddit_video"]["dash_url"], post)
        elif "v.redd.it" in post.url and post.media["reddit_video"]["dash_url"]:
            self._yt_download(post_num, post.media["reddit_video"]["fallback_url"], post)
        # Fetches actual youtube videos, these are sometimes long and possibly unwanted
        elif ("youtube.com" in post.url or "youtu.be" in post.url) and self.download_yt:
            self._yt_download(post_num, post.url, post)
        else:
            print(f"Skipped #{post_num}: {post.url}")

    def _download(self, count, url, post=None):
        """Fetches any type of file"""
        try:
            file_name = self._get_filename(count, url, post)
        except IOError:
            return
        with open(os.path.join(self.directory, file_name), "wb+") as handle:
            try:
                with requests.get(url, stream=True, timeout=1) as r:
                    r.raise_for_status()
                    for block in r.iter_content(chunk_size=8192):
                        if not block:
                            break
                        handle.write(block)
            except requests.exceptions.HTTPError as errh:
                print("Http Error:", errh)
            except requests.exceptions.ConnectionError as errc:
                print("Error Connecting:", errc)
            except requests.exceptions.Timeout as errt:
                print("Timeout Error:", errt)
            except requests.exceptions.RequestException as err:
                print("Request Error:", err)

    def _yt_download(self, count, url, post=None):
        """Fetches a youtube video, but first imports the library for that"""
        import youtube_dl
        try:
            filename = self._get_filename(count, url, post).strip(".mpd")
        except IOError:
            return
        if self.download_yt:
            ydl_opts = {'outtmpl': f'{filename}',
                        'quiet': True}
        else:
            ydl_opts = {'format': 'dash-VIDEO-1+dash-AUDIO-1', # Might not be working, throws error
                        'outtmpl': f'{filename}',
                        'quiet': True}

        working_directory = os.getcwd()
        os.chdir(self.directory)
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        os.chdir(working_directory)

    def _get_filename(self, count, url, post):
        """
        Returns a string formatted as, for example
        001-subreddit-xxxxxxxxxxxx.jpg
        002-funnygifs-djakj431kjdja.gif
        003-user123-BigAwesomeHorse.webm
        """
        if self.archive_file: self._archive(count, url, self.archive_file)
        named = True
        last_piece = url.rsplit("/")[-1]
        extension = get_extension(url)
        tag = last_piece.rsplit(extension)[0][:-1]
        if "DASH" in tag:
            tag = url.rsplit("/")[-2][:-1]
        extension = extension.split("?")[0]
        name = ""
        if named:
            name = sanitize_title(post.title)

        file_name = f"{int(count):03d}-{name}-{tag}.{extension}"
        return file_name

    def _archive(self, count, url, archive_file):
        """
        Saves tags to file, if not already present there.
        If present, raises IOError to stop them from getting downloaded.
        """
        if count == 0:
            with open(archive_file, "r") as f:
                for line in f:
                    self.archived.append(line.split("\n")[0])
        if "DASH" in url:
            tag = url.rsplit("/")[-2]
        else:
            last_piece = url.split("/")[-1]
            extension = get_extension(url)
            tag = last_piece.rsplit(extension)[0][:-1]
        if tag not in self.archived:
            with open(archive_file, "a") as f:
                f.write(f"{tag}\n")
        else:
            raise IOError('File already downloaded')  # Needs refinement
