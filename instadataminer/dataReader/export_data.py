from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
import time

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput






"""
"platformName": "Android",
"appium:automationName": "UiAutomator2",
"appium:deviceName": "R58N7077SJD",
"appium:appPackage": "com.instagram.android",
"appium:appActivity": ".MainActivity",
"appium:noReset": true,
"appium:uiautomator2ServerInstallTimeout": 90000,
"appium:newCommandTimeout": 3600,
"appium:connectHardwareKeyboard": true
"""

def connect():
    options = AppiumOptions()
    options.load_capabilities({
        "appium:platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": "R58N7077SJD",
        "appium:appPackage": "com.instagram.android",
        "appium:appActivity": ".MainActivity",
        "appium:noReset": True,
        "appium:uiautomator2ServerInstallTimeout": 90000,
        "appium:newCommandTimeout": 3200,
        "appium:connectHardwareKeyboard": True
    })
    return webdriver.Remote("http://127.0.0.1:4723", options=options)

def split_action(driver, user_list, output_file, followers, following):
    if following: 
        process_list(driver, user_list, output_file, "com.instagram.android:id/row_profile_header_textview_following_count")
    if followers:
        process_list(driver, user_list, output_file, "com.instagram.android:id/row_profile_header_textview_followers_count")

def process_list(driver, user_list, output_file, id):
    while True:

        users = driver.find_elements(AppiumBy.ID, id)
        
        usernames = [u.get_attribute("text") for u in users]

        with open(output_file, "a", encoding="utf-8") as f:
            for username in usernames:
                if username not in user_list:
                    user_list.append(username)
                    f.write(username + "\n")
                    print(f"ADDED - {username}")


        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(470, 1800)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(470, 1100)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        #era bien meter aqui que si hay hide button que eliminase todos antes de seguir despues de un rato no se iban a volver a generar (mejor aun darle a mas sugerencias y quitar todos antes)



        ver_mas = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/see_more_button")
        if ver_mas:
            try:
                ver_mas[0].click()
            except Exception:
                continue


def main(output_file="usuarios.txt", followers=False, following=False):

    user_list = []

    while True:

        try:

            driver = connect()

            split_action(driver, user_list, output_file, followers, following)
        except Exception:
            continue



