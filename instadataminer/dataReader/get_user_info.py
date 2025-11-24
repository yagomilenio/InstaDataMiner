from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
import time
import csv
import os
import traceback

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = AppiumOptions()
options.load_capabilities({
	"appium:platformName": "Android",
	"appium:automationName": "UiAutomator2",
	"appium:deviceName": "R58N7077SJD",
	"appium:appPackage": "com.instagram.android",
	"appium:appActivity": ".MainActivity",
	"appium:noReset": True,
	"appium:uiautomator2ServerInstallTimeout": 90000,
	"appium:newCommandTimeout": 4000,
	"appium:connectHardwareKeyboard": True
})

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



driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

class UserProfile():
    def __init__(self, username, nombre, descripcion, publicaciones, seguidores, seguidos, business):
        self.username=username
        self.nombre=nombre
        self.descripcion=descripcion
        self.publicaciones=publicaciones
        self.seguidores=seguidores
        self.seguidos=seguidos
        self.business=business

def save_to_csv(userProfile):
    file_exists = os.path.exists("procesed_users.csv")
    write_header = not file_exists or os.path.getsize("procesed_users.csv") == 0

    with open("procesed_users.csv", mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)  
            if write_header:
                writer.writerow(["user", "name", "descripcion", "publicaciones", "seguidores", "seguidos", "business"])
            writer.writerow([userProfile.username, userProfile.nombre, userProfile.descripcion, userProfile.publicaciones, userProfile.seguidores, userProfile.seguidos, userProfile.business])

def process_user(driver, username):

        wait = WebDriverWait(driver, 15)

        try:
            search = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/search_tab")   
            search.click()
        except Exception:
            driver.press_keycode(4)


        search_bar = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/action_bar_search_edit_text")
        search_bar.click()

        search_bar_input = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/action_bar_search_edit_text")
        search_bar_input.send_keys(username)

        profile = wait.until(EC.presence_of_all_elements_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.instagram.android:id/row_search_user_container").instance(0)')))
        if profile:
            profile[0].click()
        else:
            profile = wait.until(EC.presence_of_element_located((AppiumBy.ID, 'com.instagram.android:id/row_search_user_container')))
            profile.click()

        print("[DEBUG] - Obteniendo nombre")


        
        nombre = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/profile_header_full_name")
        if nombre:
            nombre_txt=nombre[0].text
        else:
            nombre_txt="Null"
            


        print(f"\t- {nombre_txt}")

        print("[DEBUG] - Obteniendo business")
        business_list = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/profile_header_business_category")
        business_txt = business_list[0].text if business_list else "Null"

        print(f"\t- {business_txt}")

        print("[DEBUG] - Obteniendo descripcion")
        descripcion = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/profile_header_bio_text")
        if descripcion:
            descripcion_txt = descripcion[0].text
        else:
            descripcion_txt="Null"

        print(f"\t- {descripcion_txt}")

        print("[DEBUG] - Obteniendo publicaciones")
        publicaciones = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.instagram.android:id/row_profile_header_textview_post_count")))
        publicaciones_txt = publicaciones.text

        print(f"\t- {publicaciones_txt}")

        print("[DEBUG] - Obteniendo seguidores")
        seguidores = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.instagram.android:id/row_profile_header_textview_followers_count")))
        seguidores_txt = seguidores.text

        print(f"\t- {seguidores_txt}")

        print("[DEBUG] - Obteniendo seguidos")
        seguidos = wait.until(EC.presence_of_element_located((AppiumBy.ID, "com.instagram.android:id/row_profile_header_textview_following_count")))
        seguidos_txt = seguidos.text

        print(f"\t- {seguidos_txt}")

        return UserProfile(username, nombre_txt, descripcion_txt, publicaciones_txt, seguidores_txt, seguidos_txt, business_txt)


procesed_usernames = []

with open("procesed_users.csv", "r", encoding="utf-8") as f:
    for linea in f:
        partes = linea.strip().split(",") 
        if partes:                         
            procesed_usernames.append(partes[0])




with open("usuarios.txt", "r", encoding="utf-8") as users:

    for user in users:

        username = user.strip()
        if username not in procesed_usernames:

            try:

                user_profile = process_user(driver, username)
                save_to_csv(user_profile)
            except Exception as e:
                print(f"[ERROR] - Ocurrió un error con {username}: {e}")
                traceback.print_exc()
                driver.quit()
                driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

                continue



