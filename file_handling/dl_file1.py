from tqdm import tqdm
import os
import sys
from pathlib import Path
import requests

home_path = Path.home()
sub_path = "tmp"
url = "https://www.python.org/ftp/python/3.8.5/python-3.8.5-macosx10.9.pkg"
filesize = int(requests.head(url).headers["Content-Length"])
filename = os.path.basename(url)
os.makedirs(os.path.join(home_path, sub_path), exist_ok=True)
dl_path = os.path.join(home_path, sub_path, filename)
chunk_size = 1024
with requests.get(url, stream=True) as r:
    with open(dl_path, "wb") as f, tqdm(
        unit="B",
        unit_scale=True,
        unit_divisor=1024,
        total=filesize,
        file=sys.stdout
    ) as progress:
        for chunk in r.iter_content(chunk_size=chunk_size):
            datasize = f.write(chunk)
            progress.update(datasize)