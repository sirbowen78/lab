from selenium import webdriver
from selenium.common.exceptions import UnexpectedAlertPresentException, WebDriverException

import os


def find_file(base="C:\\", name=None):
    """
    Find file and return the first match found.
    :param base: Base path to search
    :param name: filename to search
    :return: absolute path of the file.
    """
    for root, dirs, filename in os.walk(base):
        if name in filename:
            return os.path.join(root, name)


try:
    has_driver = find_file(name="geckodriver.exe")
    if has_driver:
        # if driver is found.
        driver = webdriver.Firefox(executable_path=has_driver)
    else:
        # Thank you Sergey Pirogov for creating webdriver manager module.
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    try:
        # No exception is good news.
        # if auth has failed UnexpectedAlertPresentException will appear.
        driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")
        if "Congratulations! You must have the proper credentials." in driver.page_source:
            print("Authentication successful!")
    except UnexpectedAlertPresentException as e:
        # Only use stderr if exception is caught.
        from sys import stderr
        stderr.write(str(e))
    finally:
        # close the driver regardless of whatever.
        driver.close()
except WebDriverException as e:
    from sys import stderr
    stderr.write(str(e))
