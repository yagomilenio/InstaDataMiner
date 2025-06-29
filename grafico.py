import csv
import networkx as nx
import matplotlib.pyplot as plt

# Crear el grafo vacío
G = nx.Graph()

# Abrir el archivo CSV y leer línea por línea
with open("data.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if len(row) >= 2:  # Asegura que haya al menos origen y destino
            origen = row[0].strip()
            destino = row[1].strip()
            G.add_edge(origen, destino)
            print(origen)

# Crear posiciones para los nodos con mejor distribución
pos = nx.spring_layout(G, k=0.7, iterations=50)

# Configurar tamaño de la figura para que no quede pequeño
plt.figure(figsize=(12, 8))

# Dibujar el grafo con posiciones y etiquetas legibles
nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray',
        node_size=1500, font_size=10)

plt.title("Grafo desde CSV con mejor espaciado")
plt.show()
