from appium.webdriver.common.appiumby import AppiumBy
from config import *


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
