# This script contains functions for downloading files from websites
# The functions work for most file servers in the public, but there is a challenge
# in determining the content length of the files from github.
# The scripts that are written use type hinting to assist in using the functions
import os
import sys
import requests
from pathlib import Path
import shutil
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor


def get_file_name(url: str):
    """
    This function gets the file name from the download link. Works for most websites.
    Do not work on files hosted in content delivery website, as retrieval of file from CDN
    uses unique session keys which are hard to determine.
    :param url: the download link
    :return: filename in string.
    """
    filename = os.path.basename(url)
    fname, extension = os.path.splitext(filename)
    if extension:
        if "=" in filename:
            return filename.split("=")[-1]
        return filename
    header = requests.head(url).headers
    if "Location" in header:
        return os.path.basename(header["Location"])
    return filename


def get_file_size(url: str):
    """
    This function only works if Content-Length is in the header,
    files hosted in CDN will not work as there is no content-length or
    content-length is not accurate.
    Knowing the file size is useful for implementing progress bar.
    :param url:
    :return:
    """
    header = requests.head(url).headers
    if "Content-Length" in header and header["Content-Length"] != 0:
        return int(header["Content-Length"])
    elif "Location" in header:
        h = requests.head(header["Location"]).headers
        return int(h.get("Content-Length", 0))
    else:
        return 0


def set_save_to(filename, subdir="Downloads"):
    """
    This function is used to set the target directory where
    the download will be saved to.
    :param filename: the filename of the downloading file.
    :param subdir: the subdirectory under the home directory.
    :return: absolute path.
    """
    path = os.path.join(Path.home(), subdir)
    if not os.path.exists(path):
        os.makedirs(path)
    return os.path.join(path, filename)


def file_dl(url: str, fdst: str = "Temps"):
    """
    This function download the files from the download link.
    TQDM is used to keep track on the download progress,
    This examples show how to use tqdm with shutil.copyfileobj.
    Searching from the internet it is more common to find
    for chunk in chunk_size:
        f.write(chunk)
        pbar.update(len(chunk))
    :param url: download link
    :param fdst: dst path
    :return: shutil returns none, if you need data written use f.write().
    """
    filename = get_file_name(url)
    size = get_file_size(url)
    save_to = set_save_to(filename, subdir=fdst)
    with requests.get(url, stream=True) as r, open(save_to, "wb") as f, tqdm.wrapattr(
            r.raw,
            "read",
            total=size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
            desc=filename,
            file=sys.stdout
    ) as raw:
        shutil.copyfileobj(raw, f)


if __name__ == "__main__":
    urls = ["https://www.vmware.com/go/getworkstation-win",
            "https://download.geany.org/geany-1.36_osx-2.dmg",
            "http://download.betanews.com/download/1099412658-1/iview454_plugins_x64_setup.exe",
            "https://get.videolan.org/vlc/3.0.11.1/macosx/vlc-3.0.11.1.dmg",
            "https://www.python.org/ftp/python/3.8.5/python-3.8.5-macosx10.9.pkg"]

    with ProcessPoolExecutor() as e:
        e.map(file_dl, urls)
