import os
from elasticsearch import Elasticsearch
import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns

# Configuración de la conexión desde variables de entorno
es_endpoint = os.getenv("ES_ENDPOINT", "https://my-elasticsearch-project-c267e7.es.us-east-1.aws.elastic.cloud:443")  # Valor por defecto
es_api_key = os.getenv("ES_API_KEY", "d1NaWHNwWUJIbEJDY3RlR0htS2M6ZDFYX0R3VFFsNVoxc1JnM0lMTXBLQQ==")  # Valor por defecto

# Validar que las variables no sean None
if not es_endpoint or not es_api_key:
    print("Error: Las variables de entorno ES_ENDPOINT y ES_API_KEY deben estar definidas")
    exit()

client = Elasticsearch(
    es_endpoint,
    api_key=es_api_key
)

# Verificar la conexión
if client.ping():
    print("Conexión exitosa a Elasticsearch")
else:
    print("Error: No se pudo conectar a Elasticsearch")
    exit()

# Nombre del índice
index_name = "iris_dataset"

# Crear el índice si no existe
if not client.indices.exists(index=index_name):
    mappings = {
        "properties": {
            "sepal length (cm)": {"type": "float"},
            "sepal width (cm)": {"type": "float"},
            "petal length (cm)": {"type": "float"},
            "petal width (cm)": {"type": "float"},
            "target": {"type": "integer"},
            "target_names": {"type": "keyword"}
        }
    }
    client.indices.create(index=index_name, body={"mappings": mappings})
    print(f"Índice {index_name} creado con mapeo")
else:
    print(f"Índice {index_name} ya existe")

# Cargar el dataset Iris
iris = load_iris()
iris_df = pd.DataFrame(data=iris.data, columns=iris.feature_names)
iris_df['target'] = iris.target
iris_df['target_names'] = iris_df['target'].apply(lambda x: iris.target_names[x])

# Indexar los datos
for i, row in iris_df.iterrows():
    doc = row.to_dict()
    client.index(index=index_name, id=i, body=doc)

print(f"Datos indexados en Elasticsearch en el índice {index_name}")

# Crear gráficos
os.makedirs("docs", exist_ok=True)  # Carpeta para GitHub Pages

# Gráfico 1: Scatter plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=iris_df, x="sepal length (cm)", y="sepal width (cm)", hue="target_names")
plt.title("Sepal Length vs Sepal Width")
plt.savefig("docs/sepal_plot.png")
plt.close()

# Gráfico 2: Pairplot
sns.pairplot(iris_df, hue="target_names", vars=iris.feature_names)
plt.savefig("docs/pairplot.png")
plt.close()

print("Gráficos generados en la carpeta 'docs'")