import requests
from pathlib import Path
import os


url = "https://www.python.org/ftp/python/3.7.9/python-3.7.9-macosx10.9.pkg"
filename = os.path.basename(url)
dl_path = os.path.join(Path.home(), "tmp")
os.makedirs(dl_path, exist_ok=True)
abs_path = os.path.join(dl_path, filename)
with requests.get(url, stream=True) as r, open(abs_path, "wb") as f:
    for chunk in r.iter_content(chunk_size=1024):
        f.write(chunk)
