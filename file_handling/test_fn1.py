import os
import sys
import requests
from pathlib import Path
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import shutil

# Download file with tqdm for progress bar and shutil.copyfileobj for copying the requests stream.

def get_filename(url):
    filename = os.path.basename(url)
    fname, extension = os.path.splitext(filename)
    if extension:
        return filename
    header = requests.head(url).headers
    if "Location" in header:
        return os.path.basename(header["Location"])
    return fname


def get_file_size(url):
    header = requests.head(url).headers
    if "Content-Length" in header and header["Content-Length"] != 0:
        return int(header["Content-Length"])
    elif "Location" in header and "status" not in header:
        redirect_link = header["Location"]
        r = requests.head(redirect_link).headers
        return int(r["Content-Length"])


def download_file(url, filename=None):
    # Download to the Downloads folder in user's home folder.
    download_dir = os.path.join(Path.home(), "Downloads")
    if not os.path.exists(download_dir):
        os.makedirs(download_dir, exist_ok=True)
    if not filename:
        filename = get_filename(url)
    file_size = get_file_size(url)
    abs_path = os.path.join(download_dir, filename)
    chunk_size = 1024
    with open(abs_path, "wb") as f, requests.get(url, stream=True) as r, tqdm.wrapattr(
            r.raw,
            "read",
            unit="B",
            unit_scale=True,
            unit_divisor=chunk_size,
            desc=filename,
            total=file_size,
            file=sys.stdout
    ) as raw:
        shutil.copyfileobj(raw, f)


if __name__ == "__main__":
    urls = ["http://mirrors.evowise.com/linuxmint/stable/20/linuxmint-20-xfce-64bit.iso",
            "https://www.vmware.com/go/getworkstation-win",
            "https://download.geany.org/geany-1.36_setup.exe"]
    with ProcessPoolExecutor() as e:
        e.map(download_file, urls, timeout=60)
