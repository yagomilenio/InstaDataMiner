import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
import html
import time
import pandas as pd
import requests
import os

def haz_click(xpath):
        wait = WebDriverWait(driver, 10)
        element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element.click()



df = pd.read_csv('data.csv')

col1=list(set(df.iloc[:,0]))

col2=list(set(df.iloc[:,1]))

col1.extend(col2)

usuarios=list(set(col1))


options = uc.ChromeOptions()

driver = uc.Chrome(options=options)
first = True
for usuario in usuarios:

    if not os.path.exists(f'images/{usuario}'):

        driver.get(f"https://www.instagram.com/{usuario}/")

        if first:
            first=False
            haz_click('/html/body/div[4]/div[1]/div/div[2]/div/div/div/div/div[2]/div/button[1]')

        dom = driver.page_source

        time.sleep(2)
        match = re.search(r'<img[^>]*alt="Foto del perfil[^"]*"[^>]*src="([^">]+)"' , dom)
        print(match)
        if match:
            src = match.group(1)
            src = html.unescape(src)
            response=requests.get(src)
            if response.status_code == 200:
                with open(f'images/{usuario}.jpg', 'wb') as f:
                    f.write(response.content)
            else:
                print("Error al descargar:", response.status_code)
        else:
            print("Imagen no encontrada.")


driver.quit()
