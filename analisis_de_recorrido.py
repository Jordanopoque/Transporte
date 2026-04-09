import requests

# =========================================
# FUNCION: CONTAR ELEMENTOS DEL JSON
# =========================================
def contar_elementos(obj):
    if isinstance(obj, dict):
        return sum(contar_elementos(v) for v in obj.values()) + len(obj)
    elif isinstance(obj, list):
        return sum(contar_elementos(i) for i in obj) + len(obj)
    else:
        return 1


# =========================================
# CONFIGURACION
# =========================================
codigo = "101"  # 🔥 cambia aquí el recorrido que quieras analizar

url = f"https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={codigo}"

print(f"Analizando recorrido {codigo}...\n")

# =========================================
# CONSUMO API
# =========================================
response = requests.get(url)

if response.status_code != 200:
    print("Error al consumir la API")
    exit()

data = response.json()

# =========================================
# VALIDAR DATOS
# =========================================
if not data or "ida" not in data:
    print("No hay datos del recorrido")
    exit()

# =========================================
# EXTRACCION DE DATOS
# =========================================
negocio = data.get("negocio", {})
empresa = negocio.get("nombre", "Sin empresa")
color = negocio.get("color", "Sin color")

ida = data.get("ida", {})
paraderos = ida.get("paraderos", [])
horarios = ida.get("horarios", [])

# =========================================
# CALCULOS
# =========================================
cantidad_paraderos = len(paraderos)
cantidad_horarios = len(horarios)

total_servicios = 0
for p in paraderos:
    total_servicios += len(p.get("servicios", []))

tamaño_bytes = len(response.content)
tamaño_kb = tamaño_bytes / 1024

total_elementos = contar_elementos(data)

# =========================================
# RESULTADOS
# =========================================
print("===== RESULTADOS =====")
print(f"Recorrido: {codigo}")
print(f"Empresa: {empresa}")
print(f"Color: {color}")
print(f"Cantidad de paraderos: {cantidad_paraderos}")
print(f"Cantidad de horarios: {cantidad_horarios}")
print(f"Servicios en paraderos: {total_servicios}")
print(f"Tamaño del JSON: {tamaño_bytes} bytes ({tamaño_kb:.2f} KB)")
print(f"Complejidad (elementos JSON): {total_elementos}")