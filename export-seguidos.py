#import undetected_chromedriver as uc
import csv
from selenium import webdriver as uc
import subprocess
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pickle
import time
import re
import pyautogui



MAX_DEPTH=2
USER = input("Introduce el nombre de usuario: ")
cookies_file = "cookies_instagram.pkl"


options = uc.ChromeOptions()

driver = uc.Chrome(options=options)
driver.get("https://www.instagram.com/")

# Cargar cookies desde archivo
with open(cookies_file, "rb") as f:
    cookies = pickle.load(f)

for cookie in cookies:
    # Elimina el campo 'sameSite' si está para evitar errores
    cookie.pop('sameSite', None)
    driver.add_cookie(cookie)

driver.refresh()



def obtain_follows(username, seguidores=False):
    driver.get(f"https://www.instagram.com/{username}")

    print("Deberías estar logueado ahora con las cookies cargadas.")


    def haz_click(xpath):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()




    if seguidores:
        haz_click('/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[2]/div/a')
    else:
        haz_click('/html/body/div[1]/div/div/div[2]/div/div/div[1]/div[2]/div/div[1]/section/main/div/header/section[3]/ul/li[3]/div/a')



    time.sleep(1)

    pyautogui.moveTo(620, 710, duration=0.5)

    # Esperar un momento
    time.sleep(1)

    # Hacer scroll hacia arriba (número positivo) o abajo (número negativo)

    count = 0
    cuenta = 0

    while count < 20:
        actual = len(driver.find_elements(By.XPATH, '//a[contains(@href, "/")]'))

        if actual == cuenta:
            count += 1
        else:
            count = 0

        cuenta = actual
        pyautogui.scroll(-500)

    print("yessssss")

    html = driver.page_source
    patron = r'style="display: flex; flex-direction: column; height: 100%; max-width: 100%;".*<div style="display: flex; flex-direction: column; padding-bottom: 0px; padding-top: 0px; position: relative;">(.*)'

    match = re.search(patron, html)
    
    if match:
        users=match.group(1)
        patron2= r'href="/([^/]+)/"'
        match2=re.findall(patron2, users)
        match2 = list(set(match2))

    else:
        print("No encontrado")


    nombres=match2
    print(nombres)
    print(len(nombres))


    with open("data.csv", mode="a", newline="", encoding="utf-8") as archivo_csv:
        escritor = csv.writer(archivo_csv)

        for nombre in nombres:
            if seguidores:
                escritor.writerow([nombre, username])
            else: 
                escritor.writerow([username, nombre])
    return nombres


procesar = set([USER])
depth = 0

while procesar and depth < MAX_DEPTH:
    nivel_actual = procesar.copy()   
    procesar.clear()                

    for user in nivel_actual:
        seguidos = obtain_follows(user)
        seguidores = obtain_follows(user, seguidores=True)

        for seguido in seguidos:
            procesar.add(seguido)
        for seguidor in seguidores:
            procesar.add(seguidor)

    depth += 1





driver.quit()

exit()



 