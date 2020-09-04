from selenium import webdriver
import os
from time import sleep
from random import uniform


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


driver = webdriver.Firefox(executable_path=find_file(name="geckodriver.exe"))
driver.get("https://the-internet.herokuapp.com/dropdown")

# Select option1.
driver.find_element_by_xpath('/html/body/div[2]/div/div/select/option[2]').click()

# use sleep to temporarily pause before next click.
sleep(uniform(5, 10))

# select option2.
driver.find_element_by_xpath('/html/body/div[2]/div/div/select/option[3]').click()
