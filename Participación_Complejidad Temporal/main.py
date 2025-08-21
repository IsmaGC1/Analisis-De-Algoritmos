import random
import time
import matplotlib.pyplot as plt
import pandas as pd

def generar_lista(N, minimo=1, maximo=10000):
    return [random.randint(minimo, maximo) for _ in range(N)]

def bubble_sort(arr):
    a = arr.copy()
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return merge(left, right)

def merge(left, right):
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

# Diccionario de algoritmos para simplificar
ALGORITMOS = {
    "Bubble Sort": bubble_sort,
    "Merge Sort": merge_sort,
    "Quick Sort": quick_sort
}

def medir_tiempos():
    tamanos = list(range(50, 1050, 50))
    resultados = {"Tamaño": tamanos}

    for nombre, funcion in ALGORITMOS.items():
        tiempos = []
        for n in tamanos:
            lista = generar_lista(n)
            inicio = time.perf_counter()
            funcion(lista)
            fin = time.perf_counter()
            tiempos.append((fin - inicio) * 1000)  # Tiempo en ms
        resultados[nombre] = tiempos

    return resultados

def graficar_resultados(resultados):
    tamanos = resultados["Tamaño"]

    plt.figure(figsize=(10, 6))
    for nombre in ALGORITMOS.keys():
        plt.plot(tamanos, resultados[nombre], marker="o", label=nombre)

    plt.xlabel("Tamaño de la lista")
    plt.ylabel("Tiempo de ejecución (ms)")
    plt.title("Comparación de Algoritmos de Ordenamiento")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.show()

def mostrar_tabla(resultados):
    df = pd.DataFrame(resultados)
    print("\n===== TABLA DE TIEMPOS (ms) =====")
    print(df)
    return df

if __name__ == "__main__":
    resultados = medir_tiempos()
    tabla = mostrar_tabla(resultados)
    graficar_resultados(resultados)
