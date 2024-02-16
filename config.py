import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
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
