import tkinter as tk
from tkinter import messagebox
import numpy as np
import random

def distancia_euclidiana(punto1, punto2):
    punto1_np = np.array(punto1)
    punto2_np = np.array(punto2)
    distancia = np.linalg.norm(punto2_np - punto1_np)
    return distancia

def encontrar_puntos_mas_cercanos(puntos):
    if len(puntos) < 2:
        return None, None, None, None, None
    distancia_minima = float('inf')
    puntos_cercanos = (None, None)
    indices = (None, None)

    for i in range(len(puntos)):
        for j in range(i + 1, len(puntos)):
            distancia_actual = distancia_euclidiana(puntos[i], puntos[j])
            if distancia_actual < distancia_minima:
                distancia_minima = distancia_actual
                puntos_cercanos = (puntos[i], puntos[j])
                indices = (i, j)
    return puntos_cercanos, distancia_minima, indices

def calcular_distancia_minima():
    puntos = []
    try:
        for i in range(5):
            x = float(entries_x[i].get())
            y = float(entries_y[i].get())
            puntos.append((x, y))
    except ValueError:
        messagebox.showerror("Error de entrada", "Ingresa solo números en las coordenadas.")
        return

    puntos_cercanos, distancia, indices = encontrar_puntos_mas_cercanos(puntos)

    if puntos_cercanos and distancia is not None:
        i, j = indices
        resultado = f"Los puntos más cercanos son P{i + 1} {puntos[i]} y P{j + 1} {puntos[j]}, con una distancia de {distancia:.2f}"
    else:
        resultado = "Se necesitan al menos dos puntos para el cálculo."

    label_resultado.config(text=resultado)

def limpiar_datos():
    for i in range(5):
        entries_x[i].delete(0, tk.END)
        entries_y[i].delete(0, tk.END)
    label_resultado.config(text="Presiona 'Calcular' para ver la distancia más corta.")

def generar_datos_aleatorios():
    limpiar_datos()  # Limpia los campos antes de llenarlos con nuevos datos
    for i in range(5):
        x = random.randint(0, 40)
        y = random.randint(0, 40)
        entries_x[i].insert(0, str(x))
        entries_y[i].insert(0, str(y))

# Crear la ventana principal de la GUI
root = tk.Tk()
root.title("El Par Más Cercano")
root.geometry("650x450")
root.configure(bg="#e8f5e9")

# Marco para los campos de entrada
frame_puntos = tk.Frame(root, bg="#e8f5e9", padx=10, pady=10)
frame_puntos.pack(pady=10)
tk.Label(frame_puntos, text="Ingresa las coordenadas de 5 puntos:", bg="#e8f5e9", font=("Arial", 11, "bold")).grid(
    row=0, columnspan=3, pady=(0, 10))

entries_x = []
entries_y = []

# Crear los campos de entrada para 5 puntos
for i in range(5):
    tk.Label(frame_puntos, text=f"Punto {i + 1}:", bg="#e8f5e9", font=("Arial", 10, "bold")).grid(row=i * 2 + 1,
                                                                                                  column=0, rowspan=2,
                                                                                                  sticky="w", padx=5)
    tk.Label(frame_puntos, text="x", bg="#e8f5e9").grid(row=i * 2 + 1, column=1, padx=5, pady=(5, 0))
    tk.Label(frame_puntos, text="y", bg="#e8f5e9").grid(row=i * 2 + 1, column=2, padx=5, pady=(5, 0))

    entry_x = tk.Entry(frame_puntos, width=10, borderwidth=2, relief="groove")
    entry_x.grid(row=i * 2 + 2, column=1, padx=5, pady=(0, 5))
    entries_x.append(entry_x)
    entry_y = tk.Entry(frame_puntos, width=10, borderwidth=2, relief="groove")
    entry_y.grid(row=i * 2 + 2, column=2, padx=5, pady=(0, 5))
    entries_y.append(entry_y)

# Marco para los botones
frame_botones = tk.Frame(root, bg="#e8f5e9")
frame_botones.pack(pady=10)

btn_generar = tk.Button(frame_botones, text="Generar Aleatorios", command=generar_datos_aleatorios, bg="#2196F3",
                        fg="white", font=("Arial", 10, "bold"), padx=15, pady=5)
btn_generar.pack(side=tk.LEFT, padx=10)

btn_calcular = tk.Button(frame_botones, text="Calcular", command=calcular_distancia_minima, bg="#4CAF50", fg="white",
                         font=("Arial", 10, "bold"), padx=15, pady=5)
btn_calcular.pack(side=tk.LEFT, padx=10)

btn_limpiar = tk.Button(frame_botones, text="Limpiar", command=limpiar_datos, bg="#f44336", fg="white",
                        font=("Arial", 10, "bold"), padx=15, pady=5)
btn_limpiar.pack(side=tk.LEFT, padx=10)

label_resultado = tk.Label(root, text="Presiona 'Calcular' para ver la distancia más corta.", bg="#e8f5e9",
                           font=("Arial", 10, "italic"), justify="center")
label_resultado.pack(pady=10, padx=10)

root.mainloop()