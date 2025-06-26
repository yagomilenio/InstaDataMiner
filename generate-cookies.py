import undetected_chromedriver as uc
import pickle
import time

# Ruta donde guardarás las cookies
cookies_file = "cookies_instagram.pkl"

options = uc.ChromeOptions()

driver = uc.Chrome(options=options)

driver.get("https://www.instagram.com/accounts/login/")

print("Por favor, haz login manualmente en el navegador que se abrió.")
print("Cuando termines y estés dentro, vuelve aquí y presiona Enter.")

input("Presiona Enter para guardar las cookies...")

# Esperamos un poco para asegurarnos que todo cargó bien
time.sleep(5)

# Guardar cookies en archivo
cookies = driver.get_cookies()
with open(cookies_file, "wb") as f:
    pickle.dump(cookies, f)

print(f"Cookies guardadas en {cookies_file}")

driver.quit()
