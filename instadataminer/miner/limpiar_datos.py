import pandas as pd 

def clean(input_file):

    df = pd.read_csv(input_file)

    df['name_c'] = df['name'].astype(str).apply(lambda x: re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]', '', x)) #limpiado de columna nombre quitando emojis etc
    df['descripcion_c'] = df['descripcion'].astype(str).apply(lambda x: re.sub(r'[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]', '', x))