import os
from elasticsearch import Elasticsearch
import pandas as pd
import json

# Configuración de la conexión desde variables de entorno
es_endpoint = os.getenv("ES_ENDPOINT", "https://my-elasticsearch-project-c267e7.es.us-east-1.aws.elastic.cloud:443")
es_api_key = os.getenv("ES_API_KEY", "d3liZnNwWUJIbEJDY3RlR3ZtS0I6WGJsLThBQ1JDTmFPcHpVc3pOOHl2UQ==")

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

# Obtener datos de Elasticsearch
response = client.search(index=index_name, body={"query": {"match_all": {}}}, size=1000)
hits = response['hits']['hits']

# Convertir datos a un formato para gráficos
data = []
for hit in hits:
    source = hit['_source']
    data.append({
        "sepal_length": source.get("sepal length (cm)"),
        "sepal_width": source.get("sepal width (cm)"),
        "target_names": source.get("target_names")
    })

# Guardar datos en un archivo JSON
os.makedirs("docs", exist_ok=True)
with open("docs/data.json", "w") as f:
    json.dump(data, f)

print("Datos guardados en docs/data.json")