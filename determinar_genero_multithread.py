import pandas as pd
import request_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed

df = pd.read_csv('out.csv')

def obtener_genero(name):
    respuesta = request_proxy.request_with_proxy('get', f'https://api.genderize.io/?name={name}')
    data = respuesta.json()
    return name, data.get('gender'), data.get('probability')

resultados = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = {executor.submit(obtener_genero, name): name for name in df['Name']}

    for future in as_completed(futures):
        name, genero, probabilidad = future.result()
        df.loc[df["Name"] == name, "Genero"] = genero
        df.loc[df["Name"] == name, "Probabilidad"] = probabilidad

df.to_csv('out_updated.csv', index=False)
