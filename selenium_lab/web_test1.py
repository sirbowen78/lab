from selenium import webdriver
import os
import requests
from pathlib import Path
import shutil
import tarfile

# This is written based on MacOS.
# If geckodriver is not found, download the latest, then untar and ungzip.
# Follow by a test with selenium webdriver, once the website is reached the screenshot is taken.

def get_dl_link():
    url = "https://github.com/mozilla/geckodriver/releases/latest"
    base_url = requests.get(url, allow_redirects=True).url.replace("tag", "download")
    url_slices = base_url.strip("https://").split("/")
    driver_name = f"{url_slices[2]}-{url_slices[-1]}-macos.tar.gz"
    return f"{base_url}/{driver_name}"


def dl_geckdriver(base_path="tmp"):
    dl_link = get_dl_link()
    filename = dl_link.split("/")[-1]
    os.makedirs(os.path.join(Path.home(), base_path), exist_ok=True)
    full_path = os.path.join(Path.home(), base_path, filename)
    with requests.get(dl_link, stream=True) as r:
        with open(full_path, "wb") as f:
            shutil.copyfileobj(r.raw, f)
    return full_path


def unpack(extract_from, extract_to):
    os.makedirs(extract_to, exist_ok=True)
    with tarfile.open(extract_from) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, extract_to)


def get_geckodriver_path(base=Path.home()):
    for root, dirs, filenames in os.walk(base):
        if "geckodriver" in filenames:
            return os.path.join(root, "geckodriver")
    return


if __name__ == "__main__":
    found = get_geckodriver_path()
    if not found:
        driver_pkg = dl_geckdriver(base_path="webdriver")
        unpack(driver_pkg, os.path.join(Path.home(), "firefox"))
        found = get_geckodriver_path()
    driver = webdriver.Firefox(executable_path=found)
    driver.get("https://github.com/mozilla/geckodriver/releases/latest")
    driver.save_screenshot("success.png")
    driver.close()
