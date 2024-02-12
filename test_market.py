import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
from time import sleep
import random, string

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.example.demoapp',
    appActivity='.MarketActivity',
    language='ru',
    locale='RU'
)
android_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = 'http://localhost:4723'


@pytest.fixture()
def driver():
    android_driver = webdriver.Remote(appium_server_url, options=android_options)
    yield android_driver
    if android_driver:
        android_driver.quit()


def test_check_supplies(driver):
    item_more_details_btn = driver.find_element(by=AppiumBy.XPATH, value='item_more_details_btn')
    item_more_details_btn.click()
    assert driver.current_activity == '.ItemActivity', 'Assertion Error'
