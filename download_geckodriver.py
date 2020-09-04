import requests
import sys
import logging
import platform
import os
from zipfile import ZipFile

# Github has a very organized release tagging.
# The structure of the download link is predictable, hence it is easy to make
# custom python script to fetch the latest release.
# This whole script download the latest geckodriver for windows.

# Latest release url.
gecko_url = "https://github.com/mozilla/geckodriver/releases/latest"


def init_log():
    logger = logging.getLogger(__name__)
    log_fmt = logging.Formatter(
        fmt="%(asctime)s %(funcName)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger.propagate = False
    logger.setLevel(logging.INFO)
    if not logger.hasHandlers():
        console = logging.StreamHandler()
        console.setFormatter(log_fmt)
        logger.addHandler(console)
    return logger


logger = init_log()


def os_architecture():
    # platform.machine() on 64-bit system will return AMD64 as string
    # Do not use platform.architecture() as it reports 32-bit despite your system is 64.
    # This is because the python installed is 32-bit.
    if platform.machine().endswith("64"):
        logger.info("System is 64-bit.")
        return "64"
    else:
        logger.info("System is 32-bit.")
        return "32"


def os_type():
    if sys.platform == "linux":
        logger.info("OS is linux.")
        return "linux"
    elif sys.platform == "win32":
        logger.info("OS is windows.")
        return "win"
    elif sys.platform == "darwin":
        logger.info("OS is machintosh.")
        return "mac"


def get_latest_dl_link():
    """
    By requesting latest release url, the current release url will be returned.
    :return: Download link of the latest release.
    """
    r = requests.get(gecko_url)
    logger.info(f"Requested from {gecko_url}.")
    dl_base_url = r.url.replace("tag", "download")
    logger.info(f"Download base url is {dl_base_url}")
    breakdown = r.url.strip("https://").split("/")
    logger.info("Slice and dice the url...")
    filename = f"{breakdown[2]}-{breakdown[-1]}-{os_type()}{os_architecture()}.zip"
    logger.info(f"Returning the download link: {dl_base_url}/{filename}")
    return f"{dl_base_url}/{filename}", filename


def download_gecko_for_win(path=None):
    """
    This is a very basic download function, if the file is as huge as gigabytes,
    consider using chunk size to download chunk by chunk by turning on stream with requests.get().
    :param path: If not stated will download geckodriver to current working directory.
    :return: The string of the geckodriver abs path.
    """
    if path is None:
        logger.info("No path specified use the current working directory.")
        save_path = os.getcwd()
    else:
        save_path = path
    if not os.path.exists(save_path):
        logger.info(f"{save_path} does not exist, create one.")
        os.makedirs(save_path, exist_ok=True)
    dl_file_info = get_latest_dl_link()
    save_to = f"{save_path}\\{dl_file_info[1]}"
    r = requests.get(dl_file_info[0], allow_redirects=True)
    with open(save_to, "wb") as dl:
        logger.info(f"Downloading {dl_file_info[1]}...")
        dl.write(r.content)
    logger.info(f"Please find the file in {save_to}.")
    return save_to


def unpack(extract_from, extract_to):
    """
    Use the build-in zipfile module to unzip files.
    :param extract_from: abs path where the zip is.
    :param extract_to: directory where you want the extracted item to be.
    :return:
    """
    if not os.path.exists(extract_to):
        os.makedirs(extract_to, exist_ok=True)
        logger.info(f"{extract_to} does not exist, created one.")
    with ZipFile(extract_from, "r") as unarchive:
        unarchive.extractall(extract_to)
    logger.info(f"Decompressed {extract_from}, please find extracted item in {extract_to}.")


def gecko_finder(base="C:\\"):
    """
    If at least one geckodriver.exe is found return the abs path.
    :param base: path to search from.
    :return: If found return abs path else None
    """
    for root, dirs, filenames in os.walk(base):
        if "geckodriver.exe" in filenames:
            return os.path.join(root, "geckodriver.exe")
    return


if __name__ == "__main__":
    # This part demonstrates its usefulness.
    found = gecko_finder()
    if not found:
        logger.info("geckodriver.exe not found, download now.")
        save_path = download_gecko_for_win(path="c:\\tmp\\testing")
        unpack(save_path, "c:\\tmp\\webdriver")
        found = gecko_finder()

    from selenium import webdriver
    logger.info(f"Use {found} to test.")
    driver = webdriver.Firefox(executable_path=found)
    driver.get("https://the-internet.herokuapp.com/")
    if not os.path.exists("C:\\tmp"):
        os.makedirs("C:\\tmp", exist_ok=True)
    driver.save_screenshot("C:\\tmp\\success.png")
    logger.info("screenshot saved.")
    driver.close()
