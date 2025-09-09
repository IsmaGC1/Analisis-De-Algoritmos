import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Algoritmos de ordenamiento

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, [j, j + 1]
    yield arr, []

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr, [j, min_idx]
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr, [i, min_idx]
    yield arr, []

def merge_sort(arr, start=0, end=None):
    if end is None:
        end = len(arr)
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(arr, start, mid)
        yield from merge_sort(arr, mid, end)
        left = arr[start:mid]
        right = arr[mid:end]
        i = j = 0
        for k in range(start, end):
            if i < len(left) and (j >= len(right) or left[i] <= right[j]):
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            yield arr, [k]
    yield arr, []

def quick_sort(arr, low=0, high=None):
    if high is None:
        high = len(arr) - 1
    if low < high:
        # Llamamos a partition como generador y obtenemos el índice del pivote al final
        pivot_gen = partition(arr, low, high)
        pivot_index = None
        for arr_state, highlights, final_pivot in pivot_gen:
            if final_pivot is not None:
                pivot_index = final_pivot
            yield arr_state, highlights
        yield from quick_sort(arr, low, pivot_index - 1)
        yield from quick_sort(arr, pivot_index + 1, high)
    yield arr, []

def partition(arr, low, high):
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
        yield arr, [i, j], None  # None mientras no termina
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    yield arr, [i + 1], i + 1  # Devuelve índice del pivote al final


# Clase principal del visualizador

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Visualizador de Métodos de Ordenamiento")

        # Algoritmos disponibles
        self.algorithms = {
            "Bubble Sort": bubble_sort,
            "Selection Sort": selection_sort,
            "Merge Sort": merge_sort,
            "Quick Sort": quick_sort
        }

        self.colors = {
            "Bubble Sort": "#4f81bd",
            "Selection Sort": "#f39c12",
            "Merge Sort": "#2ecc71",
            "Quick Sort": "#9b59b6"
        }

        # Variables principales
        self.array = []
        self.speed = tk.IntVar(value=50)
        self.size = tk.IntVar(value=30)
        self.current_algorithm = tk.StringVar(value="Bubble Sort")
        self.sorted_indices = []
        self.pause = False
        self.generator = None
        self.sorting = False
        self.times = {alg: [] for alg in self.algorithms}


        control_frame = ttk.Frame(root, padding=10)
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Algoritmo:").grid(row=0, column=0, padx=4)
        self.algorithm_menu = ttk.Combobox(control_frame, textvariable=self.current_algorithm, values=list(self.algorithms.keys()), state="readonly")
        self.algorithm_menu.grid(row=0, column=1, padx=4)

        ttk.Label(control_frame, text="N:").grid(row=0, column=2, padx=4)
        self.size_entry = ttk.Entry(control_frame, textvariable=self.size, width=5)
        self.size_entry.grid(row=0, column=3, padx=4)

        self.btnGenerar = ttk.Button(control_frame, text="Generar", command=self.generate)
        self.btnGenerar.grid(row=0, column=4, padx=4)

        self.btnOrdenar = ttk.Button(control_frame, text="Ordenar", command=self.start_sort)
        self.btnOrdenar.grid(row=0, column=5, padx=4)

        self.btnPausar = ttk.Button(control_frame, text="Pausar/Despausar", command=self.alternar_pausa)
        self.btnPausar.grid(row=0, column=6, padx=4)

        self.btnMezclar = ttk.Button(control_frame, text="Mezclar", command=self.shuffle)
        self.btnMezclar.grid(row=0, column=7, padx=4)

        self.btnLimpiar = ttk.Button(control_frame, text="Limpiar", command=self.clear_highlights)
        self.btnLimpiar.grid(row=0, column=8, padx=4)

        self.btnVerGrafica = ttk.Button(control_frame, text="Ver gráfica de tiempos", command=self.show_graph)
        self.btnVerGrafica.grid(row=0, column=9, padx=4)

        ttk.Label(control_frame, text="Velocidad (ms):").grid(row=1, column=0, sticky=tk.W, padx=4)
        self.speed_scale = ttk.Scale(control_frame, from_=0, to=200, orient=tk.HORIZONTAL, variable=self.speed)
        self.speed_scale.grid(row=1, column=1, columnspan=3, sticky=tk.EW, padx=4)

        self.speed_label = ttk.Label(control_frame, text=f"{self.speed.get()} ms")
        self.speed_label.grid(row=1, column=4, padx=4)
        self.speed_scale.bind("<Motion>", lambda e: self.speed_label.config(text=f"{self.speed.get()} ms"))

        self.canvas = tk.Canvas(root, width=900, height=450, bg="white")
        self.canvas.pack(pady=10)

    def generate(self):
        n = self.size.get()
        self.array = random.sample(range(1, n + 1), n)
        self.sorted_indices.clear()
        self.draw_bars(self.array, [], [])

    def shuffle(self):
        random.shuffle(self.array)
        self.sorted_indices.clear()
        self.draw_bars(self.array, [], [])

    def clear_highlights(self):
        self.draw_bars(self.array, [], [])

    def start_sort(self):
        if self.sorting:
            return
        self.sorting = True
        self.pause = False

        self.btnGenerar["state"] = "disabled"
        self.btnOrdenar["state"] = "disabled"
        self.btnLimpiar["state"] = "disabled"
        self.btnVerGrafica["state"] = "disabled"
        self.btnMezclar["state"] = "disabled"

        algorithm = self.algorithms[self.current_algorithm.get()]
        self.generator = algorithm(self.array)
        start_time = time.time()
        self.animate(start_time)

    def alternar_pausa(self):
        if self.sorting:
            self.pause = not self.pause

    def animate(self, start_time):
        if self.pause:
            self.root.after(self.speed.get(), lambda: self.animate(start_time))
            return
        try:
            arr, highlights = next(self.generator)
            self.draw_bars(arr, highlights, self.sorted_indices)
            self.root.after(self.speed.get(), lambda: self.animate(start_time))
        except StopIteration:
            end_time = time.time()
            elapsed = end_time - start_time
            n = len(self.array)
            self.times[self.current_algorithm.get()].append((n, elapsed))
            self.sorted_indices = list(range(len(self.array)))
            self.draw_bars(self.array, [], self.sorted_indices)
            self.btnOrdenar["state"] = "enabled"
            self.btnGenerar["state"] = "enabled"
            self.btnLimpiar["state"] = "enabled"
            self.btnVerGrafica["state"] = "enabled"
            self.btnMezclar["state"] = "enabled"
            self.sorting = False

    def draw_bars(self, arr, highlights, sorted_indices):
        self.canvas.delete("all")
        c_w = int(self.canvas.winfo_width() or 900)
        c_h = int(self.canvas.winfo_height() or 450)
        n = len(arr)
        if n == 0:
            return
        bar_width = max(c_w // n, 1)
        max_val = max(arr)
        color = self.colors[self.current_algorithm.get()]
        for i, val in enumerate(arr):
            x0 = i * bar_width
            x1 = x0 + bar_width - 1
            height = int((val / max_val) * (c_h - 40)) if max_val else 0
            y0 = c_h - height
            y1 = c_h
            fill_color = color
            if i in highlights:
                fill_color = "#e26a6a"
            elif i in sorted_indices:
                fill_color = "#6aa84f"
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=fill_color, outline="")
            if bar_width >= 15:
                self.canvas.create_text(
                    x0 + bar_width // 2,
                    y0 - 10,
                    text=str(val),
                    fill="black",
                    font=("Arial", 8)
                )
        self.root.update_idletasks()

    def show_graph(self):
        # Verificamos que haya al menos un dato
        if not any(self.times.values()):
            messagebox.showinfo("Información", "Primero debes ordenar al menos una vez.")
            return

        graph_window = tk.Toplevel(self.root)
        graph_window.title("Tiempos de ejecución")
        graph_window.geometry("600x400")

        fig, ax = plt.subplots(figsize=(6, 4))

        # Dibujar cada algoritmo como una línea distinta
        for alg, time_list in self.times.items():
            if time_list:
                ejeX = [elemento[0] for elemento in time_list]
                ejey = [elemento[1] for elemento in time_list]
                ax.plot(ejeX, ejey, marker="o", linestyle="-", label=alg)

        ax.set_xlabel("Ejecución")
        ax.set_ylabel("Tiempo (s)")
        ax.set_title("Comparativa de tiempos por algoritmo")
        ax.legend()

        canvas = FigureCanvasTkAgg(fig, master=graph_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# Ejecutar la app

if __name__ == "__main__":
    root = tk.Tk()
    app = SortingVisualizer(root)
    root.mainloop()
