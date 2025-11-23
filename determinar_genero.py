import pandas as pd 
import request_proxy

df = pd.read_csv('out.csv')

for name in df['Name']:

    respuesta = request_proxy.request_with_proxy('get', f'https://api.genderize.io/?name={name}')
    data = respuesta.json()
    print(respuesta)
    print(data)

    genero = data.get('gender')
    probabilidad = data.get('probability')

    print(genero)
    print(probabilidad)


    df.loc[df["Name"] == name, "Genero"] = genero 
    df.loc[df["Name"] == name, "Probabilidad"] = probabilidad 



df.to_csv('out_updated.csv', index=False)
