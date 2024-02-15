import pytest
from time import sleep

from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy

from additional_tools import AdditionalTools as Tools

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

rand_username = Tools.generate_random_string(length=8)
rand_email = Tools.generate_random_string(length=5) + '@test.com'
rand_password = Tools.generate_random_string(length=8)

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
    driver.implicitly_wait(3)

    username_input = driver.find_element(by=AppiumBy.ID, value='username_input')
    username_input.send_keys(rand_username)

    email_input = driver.find_element(by=AppiumBy.ID, value='email_input')
    email_input.send_keys(rand_email)

    password_input = driver.find_element(by=AppiumBy.ID, value='password_input')
    password_input.send_keys(rand_password)

    signup_btn = driver.find_element(by=AppiumBy.ID, value='btn_signup')
    signup_btn.click()

    toast_text = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Toast").text
    assert toast_text == 'User ' + rand_username + ' created', (f"Toast.\n"
                                                                f"Expected: User {rand_username} created',\n"
                                                                f"Received: '{toast_text}'")


def test_login(driver):
    goto_login_btn = driver.find_element(by=AppiumBy.ID, value='btn_goto_signin')
    goto_login_btn.click()
    driver.implicitly_wait(3)

    username_input = driver.find_element(by=AppiumBy.ID, value='username_input')
    username_input.send_keys(test_username)

    password_input = driver.find_element(by=AppiumBy.ID, value='password_input')
    password_input.send_keys(test_password)

    signin_btn = driver.find_element(by=AppiumBy.ID, value='btn_signin')
    signin_btn.click()

    toast_text = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Toast").text
    assert toast_text == 'Auth success', (f"Toast.\n"
                                          f"Expected: Auth success',\n"
                                          f"Received: '{toast_text}'")


def test_buy_item(driver):
    test_login(driver)
    item_more_details_btn = driver.find_element(by=AppiumBy.ID, value='item_more_details_btn')
    item_more_details_btn.click()

    assert driver.current_activity == '.ItemActivity', (f'Activity check failed,\n'
                                                        f'expected .ItemActivity,\n'
                                                        f'got: {driver.current_activity}')
    assert driver.find_element(by=AppiumBy.ID, value='item_detail_text')

    buy_btn = driver.find_element(by=AppiumBy.ID, value='item_detail_buy_btn')
    buy_btn.click()

    assert driver.current_activity == '.BillingActivity', (f'Activity check failed,\n'
                                                           f'expected .BillingActivity,\n'
                                                           f'got: {driver.current_activity}')

    card_number = driver.find_element(by=AppiumBy.ID, value='order_card_number_input')
    card_number.send_keys('1111 2222 3333 4444')

    # Attempt to continue by not entering all values. Expecting: Toast
    submit_btn = driver.find_element(by=AppiumBy.ID, value='order_submit_btn')
    submit_btn.click()
    toast_text = driver.find_element(by=AppiumBy.XPATH, value="//android.widget.Toast").text
    assert toast_text == 'Not all fields are filled in', (f"Toast.\n"
                                                          f"Expected: Not all fields are filled in',\n"
                                                          f"Received: '{toast_text}'")

    card_exp = driver.find_element(by=AppiumBy.ID, value='order_card_exp_input')
    card_exp.send_keys('04/44')

    card_cvv = driver.find_element(by=AppiumBy.ID, value='order_card_cvv_input')
    card_cvv.send_keys('333')

    submit_btn.click()

    # Checking the existence of a purchase notification
    driver.open_notifications()
    sleep(1)
    assert driver.find_element(by=AppiumBy.XPATH,
                               value='//android.widget.TextView[@resource-id="android:id/title" '
                                     'and @text="DEMO APP"]'), \
        ('Notification.\n'
         'notification is not found')
    driver.back()
