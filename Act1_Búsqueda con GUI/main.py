import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
from statistics import mean
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class BusquedaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Practica GUI")
        self.geometry("850x600")

        self.data = {}
        self.avg_times = {"lineal": {}, "binaria": {}}

        self._build_ui()
        self._init_plot()

    def _build_ui(self):
        # Generar datos
        frame_gen = ttk.LabelFrame(self, text="Lista de Datos")
        frame_gen.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_gen, text="Tamaño de lista:").grid(row=0, column=0, padx=5, pady=5)
        self.size_var = tk.StringVar(value="100")
        ttk.Combobox(
            frame_gen,
            textvariable=self.size_var,
            state="readonly",
            values=["100", "1000", "10000", "100000"]
        ).grid(row=0, column=1, padx=5)

        ttk.Button(frame_gen, text="Generar datos", command=self.generate_data)\
           .grid(row=0, column=2, padx=10)

        # Búsqueda
        frame_search = ttk.LabelFrame(self, text="Realizar Búsqueda")
        frame_search.pack(fill="x", padx=10, pady=5)

        ttk.Label(frame_search, text="Valor a buscar:").grid(row=0, column=0, padx=5)
        self.target_var = tk.StringVar()
        ttk.Entry(frame_search, textvariable=self.target_var, width=15).grid(row=0, column=1, padx=5)

        ttk.Button(frame_search, text="Búsqueda lineal",
                   command=lambda: self.search("lineal"))\
           .grid(row=0, column=2, padx=5)
        ttk.Button(frame_search, text="Búsqueda binaria",
                   command=lambda: self.search("binaria"))\
           .grid(row=0, column=3, padx=5)

        # Resultados
        frame_res = ttk.LabelFrame(self, text="Resultados")
        frame_res.pack(fill="x", padx=10, pady=5)

        self.result_var = tk.StringVar(value="Aquí aparecerán los resultados.")
        ttk.Label(frame_res, textvariable=self.result_var)\
           .pack(anchor="w", padx=5, pady=5)

    def _init_plot(self):
        # Configuración gráfica
        self.fig, self.ax = plt.subplots(figsize=(6, 3))
        self.ax.set_title("Tiempo promedio de búsqueda")
        self.ax.set_xlabel("Tamaño de lista")
        self.ax.set_ylabel("Tiempo (ms)")

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=5)

    def generate_data(self):
        try:
            n = int(self.size_var.get())
        except ValueError:
            messagebox.showerror("Error", "Tamaño inválido.")
            return

        self.data[n] = sorted(random.sample(range(n * 10), n))
        self.result_var.set(f"Datos generados para tamaño {n}.")
        self._update_plot()

    def search(self, algo: str):
        if not self.data:
            messagebox.showwarning("Atención", "Primero genera los datos.")
            return

        try:
            n = int(self.size_var.get())
            x = int(self.target_var.get())
            lst = self.data[n]
        except (ValueError, KeyError):
            messagebox.showerror("Error", "Entrada no válida.")
            return

        func = self.busqueda_lineal if algo == "lineal" else self.busqueda_binaria
        tiempos = []
        idx = -1

        for _ in range(5):
            t0 = time.perf_counter()
            idx = func(lst, x)
            t1 = time.perf_counter()
            tiempos.append((t1 - t0) * 1000)

        t_avg = mean(tiempos)
        self.avg_times[algo][n] = t_avg

        estado = f"Encontrado en índice {idx}" if idx != -1 else "No encontrado"
        self.result_var.set(
            f"Tamaño={n} | {algo.title()} | {estado} | Tiempo promedio={t_avg:.3f} ms"
        )
        self._update_plot()

    @staticmethod
    def busqueda_lineal(lst, x):
        for i, v in enumerate(lst):
            if v == x:
                return i
        return -1

    @staticmethod
    def busqueda_binaria(lst, x):
        lo, hi = 0, len(lst) - 1
        while lo <= hi:
            mid = (lo + hi) // 2
            if lst[mid] == x:
                return mid
            if lst[mid] < x:
                lo = mid + 1
            else:
                hi = mid - 1
        return -1

    def _update_plot(self):
        self.ax.clear()
        self.ax.set_title("Tiempo promedio de búsqueda")
        self.ax.set_xlabel("Tamaño de lista")
        self.ax.set_ylabel("Tiempo (ms)")

        tamaños = sorted(self.data.keys())

        for algo, color in [("lineal", "blue"), ("binaria", "red")]:
            xs_data = [n for n in tamaños if n in self.avg_times[algo]]
            ys_data = [self.avg_times[algo][n] for n in xs_data]

            if xs_data:
                xs_poly = [0] + xs_data
                ys_poly = [0] + ys_data
                self.ax.plot(
                    xs_poly, ys_poly,
                    linestyle='-', marker='o',
                    color=color, label=algo.title()
                )

        # Solo llamar a legend si hay etiquetas
        handles, labels = self.ax.get_legend_handles_labels()
        if labels:
            self.ax.legend()

        self.canvas.draw()

if __name__ == "__main__":
    app = BusquedaApp()
    app.mainloop()
