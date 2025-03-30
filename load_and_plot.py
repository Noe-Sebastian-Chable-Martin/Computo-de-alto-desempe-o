from elasticsearch import Elasticsearch
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris

# Conectar a Elasticsearch con autenticación
es = Elasticsearch(
    "http://localhost:9200",
    basic_auth=("elastic", "1234")  # Ajusta según el usuario que creaste (puede ser "elastic" y "1234")
)

# Verificar conexión
if es.ping():
    print("Conexión a Elasticsearch exitosa")
else:
    print("No se pudo conectar a Elasticsearch")
    exit()

# Cargar el dataset Iris
iris = load_iris()
df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
df['target'] = iris.target
df['species'] = df['target'].map({0: 'setosa', 1: 'versicolor', 2: 'virginica'})

# Reemplazar NaN con None (por si acaso)
df = df.where(pd.notna(df), None)

# Indexar datos en Elasticsearch
for index, row in df.iterrows():
    es.index(index="iris_data", id=index, body=row.to_dict())

print("Dataset Iris cargado en Elasticsearch.")

# Generar gráfica
plt.figure(figsize=(10, 6))
for species in df['species'].unique():
    species_df = df[df['species'] == species]
    plt.scatter(species_df['sepal length (cm)'], species_df['sepal width (cm)'], label=species)

plt.title("Longitud vs Ancho de Sépalos por Especie de Iris")
plt.xlabel("Longitud de Sépalo (cm)")
plt.ylabel("Ancho de Sépalo (cm)")
plt.legend()
plt.grid(True)

# Guardar la gráfica como HTML interactivo usando plotly para GitHub Pages
import plotly.express as px
fig = px.scatter(df, x="sepal length (cm)", y="sepal width (cm)", color="species",
                 title="Longitud vs Ancho de Sépalos por Especie de Iris",
                 labels={"sepal length (cm)": "Longitud de Sépalo (cm)", "sepal width (cm)": "Ancho de Sépalo (cm)"})
fig.write_html("index.html")

print("Gráfica guardada como 'index.html' para GitHub Pages.")