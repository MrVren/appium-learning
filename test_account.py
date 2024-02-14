from time import sleep
from additional_tools import AdditionalTools as tools

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='Android',
    appPackage='com.example.demoapp',
    appActivity='.WelcomeActivity',
    forceAppLaunch=True,
    fullReset=False,
    noReset=True,
    autoGrantPermissions=True,
    language='en',
    locale='US'
)
android_options = UiAutomator2Options().load_capabilities(capabilities)
appium_server_url = 'http://localhost:4723'


rand_username = tools.generate_random_string(length=8)
rand_email = tools.generate_random_string(length=5) + '@test.com'
rand_password = tools.generate_random_string(length=8)

test_username = 'tester'
test_password = '123'


@pytest.fixture()
def driver():
    android_driver = webdriver.Remote(appium_server_url, options=android_options)
    yield android_driver
    if android_driver:
        android_driver.quit()


def test_create_account(driver):
    goto_signup_btn = driver.find_element(by=AppiumBy.ID, value='btn_goto_signup')
    goto_signup_btn.click()
    sleep(1)

    username_input = driver.find_element(by=AppiumBy.ID, value='username_input')
    username_input.send_keys(rand_username)

    email_input = driver.find_element(by=AppiumBy.ID, value='email_input')
    email_input.send_keys(rand_email)

    password_input = driver.find_element(by=AppiumBy.ID, value='password_input')
    password_input.send_keys(rand_password)

    signup_btn = driver.find_element(by=AppiumBy.ID, value='btn_signup')
    signup_btn.click()

    toast_text = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Toast").text
    assert toast_text == 'User ' + rand_username + ' created', (f"Toast. Expected: User {rand_username} created',\n"
                                                                f"Received: '{toast_text}'")


def test_login(driver):
    goto_login_btn = driver.find_element(by=AppiumBy.ID, value='btn_goto_signin')
    goto_login_btn.click()
    sleep(1)

    username_input = driver.find_element(by=AppiumBy.ID, value='username_input')
    username_input.send_keys(test_username)

    password_input = driver.find_element(by=AppiumBy.ID, value='password_input')
    password_input.send_keys(test_password)

    signin_btn = driver.find_element(by=AppiumBy.ID, value='btn_signin')
    signin_btn.click()

    toast_text = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Toast").text
    assert toast_text == 'Auth success', (f"Toast. Expected: Auth success',\n"
                                          f"Received: '{toast_text}'")


def test_check_supplies(driver):
    test_login(driver)
    item_more_details_btn = driver.find_element(by=AppiumBy.ID, value='item_more_details_btn')
    item_more_details_btn.click()
    assert driver.current_activity == '.ItemActivity', 'Assertion Error'