from time import sleep
from appium.webdriver.common.appiumby import AppiumBy
from config import *
from test_login import test_login


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
