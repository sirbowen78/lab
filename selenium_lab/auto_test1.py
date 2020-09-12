# Selenium practice website: http://automationpractice.com/index.php
# Using webdriver manager module makes driver installation or update is easy, thanks to SergeyPirogov.
# Selenium is about element interaction without human intervention, a few things learned from this exercise:
# 1. Learn how to select value/text from dropdox box.
# 2. Learn how to do radio button selection, if xpath does not work try css_selector, if element not found,
# use time.sleep(2) to pause for 2 seconds before clicking on radio button.
# 3. Anything that is expected to be visible and clickable if failed to "clicked" by selenium always try to
# use time.sleep to pause for a short time before proceed to click.
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as condition
from time import sleep
import calendar


class WebAppTester:
    def __init__(self, url="http://automationpractice.com/index.php",
                 driver_type="gecko"):
        self.url = url
        self.driver_type = driver_type

    def init_driver(self):
        if self.driver_type.lower() == "gecko" or self.driver_type.lower() == "firefox":
            return webdriver.Firefox(executable_path=GeckoDriverManager().install())
        elif self.driver_type.lower() == "chrome":
            return webdriver.Chrome(executable_path=ChromeDriverManager().install())
        elif self.driver_type.lower() == "msedge" or self.driver_type.lower() == "edge":
            return webdriver.Edge(executable_path=EdgeChromiumDriverManager().install())

    def register(self, email="test@example.com", **personal_details):
        """
        Method to test registeration with input data.
        :param email: email to register
        :param personal_details: personal details in dictionary
        :return:
        """
        driver = self.init_driver()
        driver.get(self.url)
        driver.find_element_by_xpath("/html/body/div/div[1]/header/div[2]/div/div/nav/div[1]/a").click()
        email_box = WebDriverWait(driver, 10).until(
            condition.presence_of_element_located((By.XPATH, '//*[@id="email_create"]')))
        email_box.send_keys(email)
        driver.find_element_by_xpath(
            '/html/body/div/div[2]/div/div[3]/div/div/div[1]/form/div/div[3]/button/span').click()

        # Reference radio button https://stackoverflow.com/questions/21322116/using-selenium-in-python-to-click-select-a-radio-button
        sleep(2)
        if personal_details["gender"].lower() == "mr":
            driver.find_element_by_css_selector('#id_gender1').click()
        elif personal_details["gender"].lower() == "mrs":
            driver.find_element_by_css_selector('#id_gender2').click()
        driver.find_element_by_xpath('//*[@id="customer_firstname"]').send_keys(personal_details["firstname"])
        driver.find_element_by_xpath('//*[@id="customer_lastname"]').send_keys(personal_details["lastname"])
        driver.find_element_by_xpath('//*[@id="passwd"]').send_keys(personal_details["password"])
        driver.find_element_by_css_selector(f'#days > option:nth-child({int(personal_details["day"]) + 1})').click()

        # Reference for calendar conversion from month name to number. https://stackoverflow.com/questions/3418050/month-name-to-month-number-and-vice-versa-in-python
        driver.find_element_by_css_selector(
            f'#months > option:nth-child({list(calendar.month_name).index(personal_details["month"].capitalize()) + 1})').click()

        # Reference for dropdox selection: https://intellipaat.com/community/4266/how-to-select-a-drop-down-menu-option-value-with-selenium-python
        year_dropdown = Select(driver.find_element_by_xpath('//*[@id="years"]'))
        year_dropdown.select_by_value(personal_details["year"])

        sleep(2)
        if personal_details["newsletter"]:
            driver.find_element_by_xpath('//*[@id="newsletter"]').click()
        if personal_details["optin"]:
            driver.find_element_by_xpath('//*[@id="optin"]').click()
        if "company" in personal_details.keys():
            driver.find_element_by_xpath('//*[@id="company"]').send_keys(personal_details["company"])
        driver.find_element_by_xpath('//*[@id="address1"]').send_keys(personal_details["address1"])
        if "address2" in personal_details.keys():
            driver.find_element_by_xpath('//*[@id="address2"]').send_keys(personal_details["address2"])
        driver.find_element_by_xpath('//*[@id="city"]').send_keys(personal_details['city'])
        state = Select(driver.find_element_by_xpath('//*[@id="id_state"]'))
        sleep(2)
        state.select_by_visible_text(personal_details["state"].capitalize())
        driver.find_element_by_xpath('//*[@id="postcode"]').send_keys(personal_details["postcode"])
        if "phone" in personal_details.keys():
            driver.find_element_by_xpath('//*[@id="phone"]').send_keys(personal_details["phone"])
        driver.find_element_by_xpath('//*[@id="phone_mobile"]').send_keys(personal_details["phone_mobile"])
        driver.find_element_by_xpath('//*[@id="alias"]').send_keys(personal_details["address_ref"].capitalize())
        sleep(2)
        driver.find_element_by_xpath('/html/body/div/div[2]/div/div[3]/div/div/form/div[4]/button/span').click()


if __name__ == "__main__":
    test1 = WebAppTester()
    personal_details = {
        "gender": "mr",
        "firstname": "testfirst",
        "lastname": "testsecond",
        "password": "12345",
        "day": "10",
        "month": "december",
        "year": "1965",
        "newsletter": True,
        "optin": True,
        "company": "test company",
        "address1": "false address",
        "city": "AZ",
        "state": "arizona",
        "postcode": "12345",
        "phone_mobile": "123456787",
        "address_ref": "singapore"
    }
    test1.register(email="cyruslab1@local.com", **personal_details)
