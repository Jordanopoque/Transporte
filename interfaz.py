import requests
import tkinter as tk
from tkinter import ttk, messagebox
import folium
import webbrowser

# ===============================
# FUNCION PARA GENERAR MAPA
# ===============================
def generar_mapa(codigo):
    try:
        url = f"https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={codigo}"
        data = requests.get(url).json()

        if isinstance(data, list):
            data = data[0]

        ida = data.get("ida", {})
        paraderos = ida.get("paraderos", [])
        path = ida.get("path", [])

        # Crear mapa centrado
        mapa = folium.Map(location=[-33.45, -70.65], zoom_start=12)

        # Dibujar ruta
        if path:
            folium.PolyLine(path, color="red", weight=3).add_to(mapa)

        # Agregar paraderos
        for p in paraderos:
            lat, lon = p.get("pos", [None, None])
            nombre = p.get("name", "Paradero")

            if lat and lon:
                folium.Marker(
                    location=[lat, lon],
                    popup=nombre,
                    icon=folium.Icon(color="blue")
                ).add_to(mapa)

        archivo = f"mapa_{codigo}.html"
        mapa.save(archivo)

        webbrowser.open(archivo)

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el mapa: {e}")


# ===============================
# OBTENER SERVICIOS
# ===============================
url_servicios = "https://www.red.cl/restservice_v2/rest/getservicios/all"
response = requests.get(url_servicios)
servicios = response.json()

print("Cantidad de servicios:", len(servicios))

# ===============================
# CREAR INTERFAZ
# ===============================
root = tk.Tk()
root.title("Recorridos RED - Santiago")
root.geometry("1000x600")

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

canvas = tk.Canvas(frame)
scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# ===============================
# PROCESAR RECORRIDOS
# ===============================
contador = 0

for servicio in servicios:

    try:
        # Obtener código
        if isinstance(servicio, str):
            codigo = servicio
        elif isinstance(servicio, dict):
            codigo = servicio.get("cod", "")
        else:
            continue

        if not codigo:
            continue

        url_detalle = f"https://www.red.cl/restservice_v2/rest/conocerecorrido?codsint={codigo}"
        detalle = requests.get(url_detalle).json()

        if isinstance(detalle, list):
            detalle = detalle[0]

        if not detalle or "ida" not in detalle:
            continue

        negocio = detalle.get("negocio", {})
        empresa = negocio.get("nombre", "Sin empresa")
        color = negocio.get("color", "#000000")

        ida = detalle.get("ida", {})
        paraderos = ida.get("paraderos", [])
        horarios = ida.get("horarios", [])

        # ===============================
        # TITULO DEL RECORRIDO
        # ===============================
        label_titulo = tk.Label(
            scrollable_frame,
            text=f"Recorrido {codigo} - {empresa}",
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            anchor="w"
        )
        label_titulo.pack(fill="x", pady=5)

        # ===============================
        # BOTON MAPA (🔥 PRO)
        # ===============================
        btn_mapa = tk.Button(
            scrollable_frame,
            text="Ver mapa",
            command=lambda c=codigo: generar_mapa(c)
        )
        btn_mapa.pack(anchor="w", padx=10)

        # ===============================
        # HORARIOS (CORRECTOS)
        # ===============================
        if horarios:
            for h in horarios:
                tipo = h.get("tipoDia", "Sin info")
                inicio = h.get("inicio", "-")
                fin = h.get("fin", "-")

                texto_horario = f"🕒 {tipo}: {inicio} - {fin}"
                label_h = tk.Label(scrollable_frame, text=texto_horario, fg="blue")
                label_h.pack(fill="x")
        else:
            label_h = tk.Label(scrollable_frame, text="🕒 Sin horarios disponibles", fg="red")
            label_h.pack(fill="x")

        # ===============================
        # PARADEROS
        # ===============================
        for p in paraderos[:10]:  # limitar para rendimiento
            nombre = p.get("name", "")
            comuna = p.get("comuna", "")
            lat, lon = p.get("pos", ["", ""])

            texto = f"📍 {nombre} ({comuna}) [{lat}, {lon}]"
            label = tk.Label(scrollable_frame, text=texto, anchor="w")
            label.pack(fill="x")

            # Servicios en paradero
            servicios_paradero = p.get("servicios", [])

            for s in servicios_paradero:
                cod_serv = s.get("cod", "")
                destino = s.get("destino", "")

                texto_serv = f"   ↳ {cod_serv} → {destino}"
                label_s = tk.Label(scrollable_frame, text=texto_serv, fg="gray")
                label_s.pack(fill="x")

        contador += 1

        if contador >= 10:  # limitar recorridos
            break

    except Exception as e:
        print(f"Error en servicio {servicio}: {e}")

# ===============================
# EJECUTAR APP
# ===============================
root.mainloop()