from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
import time
import csv
import os
import base64
import traceback

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from threading import Lock, Thread

processed_lock = Lock()
processed_usernames = set()




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





class UserProfile():
    def __init__(self, username, nombre, descripcion, publicaciones, seguidores, seguidos, business):
        self.username=username
        self.nombre=nombre
        self.descripcion=descripcion
        self.publicaciones=publicaciones
        self.seguidores=seguidores
        self.seguidos=seguidos
        self.business=business
    def __str__(self):
        return (
            f"UserProfile(\n"
            f"  username='{self.username}',\n"
            f"  nombre='{self.nombre}',\n"
            f"  descripcion='{self.descripcion}',\n"
            f"  publicaciones={self.publicaciones},\n"
            f"  seguidores={self.seguidores},\n"
            f"  seguidos={self.seguidos},\n"
            f"  business={self.business}\n"
            f")"
        )

def connect(device, system_port):

    options = AppiumOptions()
    options.load_capabilities({
        "appium:platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:deviceName": device,
        "appium:appPackage": "com.instagram.android",
        "appium:appActivity": ".MainActivity",
        "appium:noReset": True,
        "appium:uiautomator2ServerInstallTimeout": 90000,
        "appium:newCommandTimeout": 4000,
        "appium:connectHardwareKeyboard": True,
        "appium:systemPort": system_port
    })
    return webdriver.Remote("http://127.0.0.1:4723", options=options)


def save_to_csv(userProfile, output_file):
    file_exists = os.path.exists(output_file)
    write_header = not file_exists or os.path.getsize(output_file) == 0

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)  
            if write_header:
                writer.writerow(["user", "name", "descripcion", "publicaciones", "seguidores", "seguidos", "business"])
            writer.writerow([userProfile.username, userProfile.nombre, userProfile.descripcion, userProfile.publicaciones, userProfile.seguidores, userProfile.seguidos, userProfile.business])

def process_user(driver, username, output_folder):

        wait = WebDriverWait(driver, 2)

        try:
            search = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/search_tab")   
            search.click()
        except Exception:
            borrar_busqueda=driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Borrar texto")')
            if borrar_busqueda:
                borrar_busqueda[0].click()
            driver.press_keycode(4)


        search_bar = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/action_bar_search_edit_text")
        search_bar.click()

        search_bar_input = driver.find_element(by=AppiumBy.ID, value="com.instagram.android:id/action_bar_search_edit_text")
        search_bar_input.send_keys(username)

        profile = wait.until(EC.element_to_be_clickable((AppiumBy.ID, "com.instagram.android:id/row_search_user_container")))
        profile.click()


        print("[DEBUG] - Obteniendo foto de perfil")

        try:
            foto_perfil = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.instagram.android:id/row_profile_header_imageview")))
        except:
            foto_perfil = None

        if foto_perfil is None:
            try:
                foto_perfil = wait.until(EC.visibility_of_element_located((AppiumBy.ID, "com.instagram.android:id/profilePic")))
            except:
                foto_perfil = None
            
        if foto_perfil is not None:
            image_base64 = foto_perfil.screenshot_as_base64

        os.makedirs(output_folder, exist_ok=True)
        with open(f"./{output_folder}/{username}.png", "wb") as f:
            f.write(base64.b64decode(image_base64))

        print("[DEBUG] - Obteniendo nombre")


        
        nombre = driver.find_elements(by=AppiumBy.ID, value="com.instagram.android:id/profile_header_full_name")
        if nombre:
            nombre_txt=nombre[0].text
        else:
            nombre_txt="Null"
            


        print(f"\t- {nombre_txt}")

        print("[DEBUG] - Obteniendo business")
        try:
            business_list = WebDriverWait(driver, 1).until(
                EC.presence_of_all_elements_located(
                    (AppiumBy.ID, "com.instagram.android:id/profile_header_business_category")
                )
            )
        except:
            business_list = []
        
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

def get_user_info(device, user, output_folder="img"):

    driver=connect(device, 8200)
    userProfile = process_user(driver, user, output_folder)
    driver.quit()
    return userProfile


def get_users_info(device, system_port, input_file="usuarios.txt", output_file="procesed_users.csv", last_output_file="procesed_users.csv", output_folder="img"):
    if not os.path.exists(input_file):
        raise FileNotFoundError(f"El fichero de entrada {input_file} no existe")

    driver = connect(device, system_port)

    global processed_usernames 


    if os.path.exists(last_output_file):

        with open(last_output_file, "r", encoding="utf-8") as f:
            for linea in f:
                partes = linea.strip().split(",") 
                if partes:                         
                    procesed_usernames.add(partes[0])




    with open(input_file, "r", encoding="utf-8") as users:

        for user in users:

            username = user.strip()

            with processed_lock:
                if username in processed_usernames: #si ya fue procesado pasa al siguiente
                    continue 
                
                processed_usernames.add(username) #sino marca este como procesado

                try:

                    user_profile = process_user(driver, username, output_folder)
                    save_to_csv(user_profile, output_file)
                except Exception as e:
                    print(f"[ERROR] - Ocurrió un error con {username}: {e}")
                    traceback.print_exc()
                    driver.quit()
                    processed.remove(username)
                    driver = connect(device, system_port)

                    continue


def get_users_info_multi_device(devices, input_file="usuarios.txt", output_file="procesed_users.csv", last_output_file="procesed_users.csv", output_folder="img"):
    threads = []
    default_system_port = 8200
    for device in devices:
        t = Thread(target=get_users_info, args=(device, default_system_port, input_file, output_file, last_output_file, output_folder))
        t.start()
        threads.append(t)
        default_system_port+=1

    for t in threads:
        t.join()



