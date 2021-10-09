import hashlib


def hash_url(url: str):
    return hashlib.md5(url.encode()).hexdigest()


def remove_url_trailing_slash(url: str):
    return url.rstrip('/')