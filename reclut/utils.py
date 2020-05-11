
def get_extension(url):
    """Does some splitting on url links to get a file extension"""
    return url.rsplit("/")[-1].split(".")[-1].split("?")[0]


def sanitize_title(title):
    """Removes or replaces certain characters, as these won't do in file names"""
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
