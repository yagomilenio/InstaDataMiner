import pandas as pd
import math
from proxy import request_proxy
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np
import os
import cv2
from deepface import DeepFace
import face_recognition
from tensorflow.keras.models import load_model
from .beautyPredict.beauty_predict import beauty_predict

class miner:
    def __init__(self, input_file="db.csv", output_file="db_out.csv"):
        self.input_file=input_file
        self.output_file=output_file
        self.df=pd.read_csv(input_file)

    def calcular_genero(self, name):
        respuesta = request_proxy.request_with_proxy('get', f'https://api.genderize.io/?name={name}', 'gender')
        data = respuesta.json()
        return name, data.get('gender'), data.get('probability')



    def calcular_genero_from_file(self):
        
        resultados = []

        with ThreadPoolExecutor(max_workers=70) as executor:
            futures = {executor.submit(self.calcular_genero, name): name for name in self.df['name_c']}

        for future in as_completed(futures):
            name, genero, probabilidad = future.result()
            self.df.loc[self.df["name_c"] == name, "genero"] = genero
            self.df.loc[self.df["name_c"] == name, "probabilidad"] = probabilidad

        

    def calcular_popularidad(self):
        self.df['seguidores'] = pd.to_numeric(self.df['seguidores'], errors='coerce').fillna(0).astype(int)
        self.df['seguidos'] = pd.to_numeric(self.df['seguidos'], errors='coerce').fillna(0).astype(int)
        self.df['publicaciones'] = pd.to_numeric(self.df['publicaciones'], errors='coerce').fillna(0).astype(int)

        self.df['popularidad'] = self.df['seguidores'] / (self.df['seguidos'] + 1) + np.log(self.df['publicaciones'] + 1)


    def calcular_influencia(self):
        self.df['seguidores'] = pd.to_numeric(self.df['seguidores'], errors='coerce').fillna(0).astype(int)
        self.df['seguidos'] = pd.to_numeric(self.df['seguidos'], errors='coerce').fillna(0).astype(int)

        self.df['influencia'] = self.df['seguidores'] / (self.df['seguidos'] + 1)


    def belleza_relativa(self, path, image_name):
        """ # Cargar imagen
        image = face_recognition.load_image_file(image_path)
        
        # Detectar rostros
        face_locations = face_recognition.face_locations(image)
        
        if len(face_locations) == 0:
            # No hay rostro
            return np.nan
        
        # Tomamos el primer rostro detectado
        top, right, bottom, left = face_locations[0]
        face_image = image[top:bottom, left:right]
        
        # Convertir a BGR para OpenCV / DeepFace
        face_image_bgr = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
        
        # Obtener embedding facial con DeepFace
        embedding = DeepFace.represent(face_image_bgr, model_name='Facenet', enforce_detection=False)[0]["embedding"]
        
        score = np.linalg.norm(embedding)"""

        return beauty_predict(image_path, image_name)
        
        #return score

    def calcular_belleza(self, input_img_folder="img"):
        from deepface import DeepFace
        import face_recognition
        import cv2
        
        for user in self.df['user']:
            path = f"./{input_img_folder}"
            image_name=f"{user}.png"
            if not os.path.exists(path):
                print(f"[DEBUG] - No hay imagen de perfil de {user}")
                self.df.loc[self.df['user'] == user, 'belleza'] = np.nan
            else:
                print(f"[DEBUG] - Calculando belleza de {user}")
                score = self.belleza_relativa(path, image_name)
                print(f" - score : {score}")
                self.df.loc[self.df['user'] == user, 'belleza'] = score

    def save_to_csv(self):
        self.df.to_csv(self.output_file, index=False)


