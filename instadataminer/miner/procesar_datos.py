import pandas as pd
import math
from proxy import request_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import cv2
import numpy as np
from deepface import DeepFace
import face_recognition
import os

class miner:
    def __init__(input_file="db.csv"):
        self.input_file=input_file
        self.df=pd.read_csv(input_file)

    def calcular_genero(name):
        respuesta = request_proxy.request_with_proxy('get', f'https://api.genderize.io/?name={name}', 'gender')
        data = respuesta.json()
        return name, data.get('gender'), data.get('probability')



    def calcular_genero_from_file(output_file):
        if output_file is None:
            output_file = f"{self.input_file}_gen"
        resultados = []

        with ThreadPoolExecutor(max_workers=70) as executor:
            futures = {executor.submit(obtener_genero, name): name for name in self.df['Name']}

        for future in as_completed(futures):
            name, genero, probabilidad = future.result()
            self.df.loc[df["name"] == name, "genero"] = genero
            self.df.loc[df["name"] == name, "probabilidad"] = probabilidad

        self.df.to_csv(output_file, index=False)

    def calcular_popularidad():
        self.df['popularidad']=self.df['seguidores']/(self.df['seguidos']+1) + math.log(self.df['publicaciones']+1)


    def calcular_influencia():
        self.df['influencia']=self.df['seguidores']/(self.df['seguidos']+1)


    def belleza_relativa(image_path):
        # Cargar imagen
        image = face_recognition.load_image_file(image_path)
        
        # Detectar rostros
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            # No hay rostro
            return None
        
        # Tomamos el primer rostro detectado
        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        
        # Convertir a BGR para OpenCV / DeepFace
        face_image_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
        
        # Obtener embedding facial con DeepFace
        embedding = DeepFace.represent(face_image_bgr, model_name='Facenet', enforce_detection=False)[0]["embedding"]
        
        score = np.linalg.norm(embedding)
        
        return score

    def calcular_belleza(input_folder="img"):
        
        for user in self.df['user']:
            path = f"./{input_folder}/{user}.jpg"
            if not os.path.exists(path):
                df.loc[df['user'] == user, 'belleza'] = np.nan
            else:
                score = belleza_relativa()
                df.loc[df['user'] == user, 'belleza'] = score


