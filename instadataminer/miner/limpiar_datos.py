import pandas as pd 
import re

def clean(input_file, output_file):
    if output_file is None:
        output_file=f"{input_file.split('.')[0]}_out.csv"

    df = pd.read_csv(input_file)

    df['name_c'] = df['name'].astype(str).apply(lambda x: re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]', '', x)) #limpiado de columna nombre quitando emojis etc
    df['descripcion_c'] = df['descripcion'].astype(str).apply(lambda x: re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]', '', x))

    df.to_csv(output_file, index=False, encoding="utf-8")