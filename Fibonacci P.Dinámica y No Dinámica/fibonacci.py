import tkinter as tk
from tkinter import ttk, messagebox
import time

#Intenta importar matplotlib, si no está, informa al usuario.
try:
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


#Definiciones de las funciones de Fibonacci

def fibonacci_sin_pd(n):
    #Calcula Fibonacci con recursión simple (exponencial).
    if n <= 1:
        return n
    else:
        return fibonacci_sin_pd(n - 1) + fibonacci_sin_pd(n - 2)


def fibonacci_con_pd(n, memo={}):
    #Calcula Fibonacci con Programación Dinámica (memoización).
    if n in memo:
        return memo[n]
    if n <= 1:
        return n

    resultado = fibonacci_con_pd(n - 1, memo) + fibonacci_con_pd(n - 2, memo)
    memo[n] = resultado
    return resultado


#Clase principal de la Aplicación GUI

class FibonacciApp:
    def __init__(self, root):
        self.root = root
        root.title("Calculadora de Fibonacci")
        root.geometry("450x350")  #Tamaño de la ventana ajustado

        #Frame principal
        mainframe = ttk.Frame(root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        #Widgets de entrada y cálculo
        ttk.Label(mainframe, text="Introduce el término n:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.n_entry = ttk.Entry(mainframe, width=10)
        self.n_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(mainframe, text="Elige el método:").grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=5)
        self.metodo_var = tk.StringVar(value="con_pd")
        ttk.Radiobutton(mainframe, text="Con Programación Dinámica (Rápido)", variable=self.metodo_var,
                        value="con_pd").grid(row=2, column=0, columnspan=2, sticky=tk.W)
        ttk.Radiobutton(mainframe, text="Sin Programación Dinámica (Lento)", variable=self.metodo_var,
                        value="sin_pd").grid(row=3, column=0, columnspan=2, sticky=tk.W)

        self.calc_button = ttk.Button(mainframe, text="Calcular", command=self.calcular_fibonacci)
        self.calc_button.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        #Widgets de resultado
        self.status_label = ttk.Label(mainframe, text="Presiona 'Calcular' para empezar.")
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=tk.W)
        self.resultado_label = ttk.Label(mainframe, text="Resultado: ", font=("Arial", 12, "bold"))
        self.resultado_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=10)

        #Separador y botones de gráficas
        ttk.Separator(mainframe, orient='horizontal').grid(row=7, column=0, columnspan=2, sticky='ew', pady=10)

        ttk.Label(mainframe, text="Análisis de Complejidad:", font=("Arial", 10, "bold")).grid(row=8, column=0,
                                                                                               columnspan=2,
                                                                                               sticky=tk.W)

        self.time_graph_button = ttk.Button(mainframe, text="Gráfica de Tiempo", command=self.plot_time_comparison)
        self.time_graph_button.grid(row=9, column=0, sticky=(tk.W, tk.E), pady=5, padx=2)

        self.space_graph_button = ttk.Button(mainframe, text="Gráfica de Espacio", command=self.plot_space_comparison)
        self.space_graph_button.grid(row=9, column=1, sticky=(tk.W, tk.E), pady=5, padx=2)

        if not MATPLOTLIB_AVAILABLE:
            self.time_graph_button.config(state="disabled")
            self.space_graph_button.config(state="disabled")
            ttk.Label(mainframe, text="Instala 'matplotlib' para ver las gráficas.", foreground="red").grid(row=10,
                                                                                                            column=0,
                                                                                                            columnspan=2)

    def calcular_fibonacci(self):
        # ... (código sin cambios)
        try:
            n = int(self.n_entry.get())
            if n < 0:
                messagebox.showerror("Error", "Por favor, introduce un número no negativo.")
                return
        except ValueError:
            messagebox.showerror("Error", "Entrada no válida. Introduce un número entero.")
            return

        metodo = self.metodo_var.get()
        resultado = 0

        self.resultado_label.config(text="Resultado: ")
        self.status_label.config(text="Calculando...")
        self.root.update_idletasks()

        if metodo == "sin_pd" and n > 35:
            messagebox.showwarning("Advertencia",
                                   f"Calcular el término {n} sin P. Dinámica tomará mucho tiempo. Límite fijado en n=35 para este método.")
            self.status_label.config(text="Cálculo 'Sin PD' abortado (n > 35).")
            return

        start_time = time.perf_counter()
        if metodo == "con_pd":
            resultado = fibonacci_con_pd(n, {})
        else:
            resultado = fibonacci_sin_pd(n)
        end_time = time.perf_counter()
        tiempo_total = end_time - start_time

        self.resultado_label.config(text=f"Resultado: {resultado}")
        self.status_label.config(text=f"Cálculo completado en {tiempo_total:.8f} segundos.")

    def plot_time_comparison(self):
        #Genera y muestra una gráfica de la complejidad temporal.
        max_n = 38  # Límite para que el método lento no tarde demasiado
        n_values = range(1, max_n + 1)
        times_sin_pd = []
        times_con_pd = []

        self.status_label.config(text=f"Generando datos para la gráfica de tiempo (hasta n={max_n})...")
        self.root.update_idletasks()

        for i in n_values:
            #Medir tiempo para metodo sin PD
            start = time.perf_counter()
            fibonacci_sin_pd(i)
            times_sin_pd.append(time.perf_counter() - start)

            # Medir tiempo para metodo CON PD
            start = time.perf_counter()
            fibonacci_con_pd(i, {})
            times_con_pd.append(time.perf_counter() - start)

        self.status_label.config(text="Gráfica de tiempo generada.")
        self.create_plot_window(
            n_values,
            [times_sin_pd, times_con_pd],
            labels=['Sin PD (Exponencial)', 'Con PD (Lineal)'],
            title='Comparación de Tiempo de Ejecución (Complejidad Temporal)',
            ylabel='Tiempo (segundos) - Escala Logarítmica',
            use_log_scale=True
        )

    def plot_space_comparison(self):
        #Genera y muestra una gráfica de la complejidad espacial.
        max_n = 50
        n_values = range(1, max_n + 1)

        #Sin PD el espacio es la profundidad de la recursión, que es n.
        space_sin_pd = [n for n in n_values]

        #Con PD el espacio es el tamaño del diccionario 'memoización', que es n.
        space_con_pd = [n for n in n_values]

        self.status_label.config(text="Gráfica de espacio generada.")
        self.create_plot_window(
            n_values,
            [space_sin_pd, space_con_pd],
            labels=['Sin PD (O(n))', 'Con PD (O(n))'],
            title='Comparación de Uso de Memoria (Complejidad Espacial)',
            ylabel='Unidades de Espacio (profundidad de recursión)',
        )

    def create_plot_window(self, x_data, y_data_list, labels, title, ylabel, use_log_scale=False):
        #Función auxiliar para crear la ventana de la gráfica.
        plot_window = tk.Toplevel(self.root)
        plot_window.title(title)
        plot_window.geometry("800x600")

        fig, ax = plt.subplots(figsize=(7, 5))
        for y_data, label in zip(y_data_list, labels):
            ax.plot(x_data, y_data, label=label, marker='o', markersize=3)

        ax.set_xlabel("Término de Fibonacci (n)")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.legend()
        ax.grid(True, which="both", ls="--")

        if use_log_scale:
            ax.set_yscale('log')  #Escala logarítmica para ver la diferencia

        canvas = FigureCanvasTkAgg(fig, master=plot_window)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


#Bloque principal para ejecutar la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = FibonacciApp(root)
    root.mainloop()