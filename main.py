"""import requests
import pandas as pd
import time

url = "https://www.red.cl/restservice_v2/rest/getservicios/all"
data = requests.get(url).json()

df_api = pd.DataFrame(data)

print("Cantidad de servicios:", len(df_api))

print("\nCOLUMNAS:")
print(df_api.columns)

detalles = []

for i, row in df_api.iterrows():
    # Forma segura
    codigo = row.iloc[0]
    
    url_detalle = f"https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={codigo}"
    
    print(f"Procesando {codigo}...")
    
    try:
        detalle = requests.get(url_detalle).json()
        
        detalles.append({
            "codigo": codigo,
            "data": detalle
        })
        
        time.sleep(0.2)  # evitar sobrecargar API
        
    except Exception as e:
        print(f"Error en {codigo}: {e}")

df_detalles = pd.DataFrame(detalles)

df_detalles.to_json("detalle_recorridos.json", orient="records")

print("\nProceso terminado 🚀")"""

import pandas as pd

url = "https://storage.googleapis.com/proyecto-duoc-datasets-transports-stgo/dataset-transport-stgo.tsv"

# Leer dataset
df = pd.read_csv(url, sep="\t")

# Total de registros (filas)
total_filas = df.shape[0]

# Total de columnas
total_columnas = df.shape[1]

print("Total de registros:", total_filas)
print("Total de columnas:", total_columnas)