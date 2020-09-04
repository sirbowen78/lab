from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as condition

import os
from time import sleep


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
driver.get('https://the-internet.herokuapp.com/context_menu')
dotted_box = driver.find_element_by_xpath('//*[@id="hot-spot"]')

# Move to the dotted box and do a right click.
ActionChains(driver).move_to_element(dotted_box).context_click().perform()

# This means the driver will wait for a maximum 20 seconds for the alert to appear.
# The wait is over if the alert appears, hence this is not the same as time.sleep(20).
WebDriverWait(driver, 20).until(condition.alert_is_present())

# switch to the JS alert.
alert = driver.switch_to.alert
sleep(10)

# this clicks OK.
alert.accept()
