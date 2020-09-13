from webdriver_manager.firefox import GeckoDriverManager
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep

url = "https://the-internet.herokuapp.com/dropdown"
driver = webdriver.Firefox(
    executable_path=GeckoDriverManager().install()
)
# The sleep function is to get a more stablized result by purposefully wait for 5 seconds.
driver.get(url)
sleep(5)
options = Select(driver.find_element_by_xpath('//*[@id="dropdown"]'))
# Selection option 2 from dropdown box.
options.select_by_value("2")
sleep(5)
options.select_by_value("1")
sleep(5)
driver.close()

