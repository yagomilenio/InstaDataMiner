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
        "appium:newCommandTimeout": 0,
        "appium:connectHardwareKeyboard": True
    })
    return webdriver.Remote("http://127.0.0.1:4723", options=options)

def split_action(driver, user_list, output_file, followers, following):
    if following: 
        process_list(driver, user_list, output_file, "com.instagram.android:id/row_profile_header_textview_following_count")
    if followers:
        process_list(driver, user_list, output_file, "com.instagram.android:id/row_profile_header_textview_followers_count")

def process_list(driver, user_list, output_file, id):
    mode = driver.find_elements(AppiumBy.ID, id)
    if mode:
        mode[0].click()
    else:
        print("[ALERT] - No se encuentra modo de operación")
        return

    exit_counter=0

    while True:

        users = driver.find_elements(AppiumBy.ID, 'com.instagram.android:id/follow_list_username')

        while len(users) < 9:   #a  veces tarda en cargar hasta que cargue todo no avanza
            users = driver.find_elements(AppiumBy.ID, 'com.instagram.android:id/follow_list_username')
        
        usernames = [u.get_attribute("text") for u in users]

        with open(output_file, "a", encoding="utf-8") as f:
            continuar=False
            for username in usernames:
                if username not in user_list:
                    user_list.append(username)
                    f.write(username + "\n")
                    continuar=True
                    exit_counter=0
                    print(f"ADDED - {username}")

        if not continuar:
            exit_counter+=1

        if exit_counter >= 1000:
            driver.quit()
            exit()

        actions = ActionChains(driver)
        actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
        actions.w3c_actions.pointer_action.move_to_location(470, 1800)
        actions.w3c_actions.pointer_action.pointer_down()
        actions.w3c_actions.pointer_action.move_to_location(470, 1100)
        actions.w3c_actions.pointer_action.release()
        actions.perform()

        hide_buttons=driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.instagram.android:id/row_recommended_hide_icon_button")')
        num_hide_buttons=len(hide_buttons)

        for i in reversed(range(num_hide_buttons)):
            try:
                hide_button = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().resourceId("com.instagram.android:id/row_recommended_hide_icon_button").instance({i})')
                hide_button.click()
            except Exception as e:
                print(f"Instance {i} ya no existe: {e}")
                continue
        
        



        ver_mas = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/see_more_button")
        if ver_mas:
            try:
                ver_mas[0].click()
            except Exception:
                continue


    back=driver.find_element(AppiumBy.ID, 'com.instagram.android:id/action_bar_button_back')
    back.click()


def main(output_file="usuarios.txt", followers=False, following=False):

    user_list = []

    while True:

        try:

            driver = connect()

            split_action(driver, user_list, output_file, followers, following)
        except Exception:
            driver.quit()
            continue



