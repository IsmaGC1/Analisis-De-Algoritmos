import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math
import time
import tracemalloc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import heapq
import json
from collections import Counter
import os


class VisualizadorLCA:
    def __init__(self, ventana_principal):
        # Constructor de la clase que inicializa el árbol y la GUI.
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Visualizador de LCA - Completo")
        self.ventana_principal.geometry("1100x650")  # Aumenté un poco la altura

        # Definición del Árbol
        self.num_nodos = 12
        self.aristas = [(1, 2), (1, 3), (2, 4), (2, 5), (3, 6), (5, 7), (5, 8),
                        (8, 9), (8, 10), (10, 11)]
        self.coordenadas = {
            1: (450, 50), 2: (300, 120), 3: (600, 120), 4: (225, 190),
            5: (375, 190), 6: (600, 190), 7: (325, 260), 8: (425, 260),
            9: (475, 330), 10: (375, 330), 11: (375, 400)
        }

        self.radio_nodo = 20
        self.tabla_labels = {}
        self.simulacion_activa = False

        # ESTRUCTURAS PARA MEDICIÓN DE RENDIMIENTO
        self.datos_rendimiento = []  # Lista para almacenar los resultados de cada ejecución
        self.num_busquedas = 0  # Contador para el eje X de los gráficos

        self.crear_componentes()
        self.reiniciar_estado()
        self.preprocesar_algoritmos()
        self.dibujar_arbol()

    class _NodoH:
        def __init__(self, caracter, frecuencia):
            self.caracter = caracter
            self.frecuencia = frecuencia
            self.izq = None
            self.der = None

        def __lt__(self, other):
            return self.frecuencia < other.frecuencia

    def _calcular_frecuencias(self, texto):
        return Counter(texto)

    def _construir_arbol_huffman(self, frecuencias):
        heap = [self._NodoH(caracter, frecuencia) for caracter, frecuencia in frecuencias.items()]
        heapq.heapify(heap)
        if len(heap) == 1:
            nodo = heapq.heappop(heap)
            raiz = self._NodoH(None, nodo.frecuencia)
            raiz.izq = nodo
            return raiz
        while len(heap) > 1:
            nodo1 = heapq.heappop(heap)
            nodo2 = heapq.heappop(heap)
            nuevo = self._NodoH(None, nodo1.frecuencia + nodo2.frecuencia)
            nuevo.izq, nuevo.der = nodo1, nodo2
            heapq.heappush(heap, nuevo)
        return heap[0] if heap else None

    def generar_codigos(self, raiz):
        codigos = {}

        def recorrer(nodo, codigo_actual):
            if nodo is None:
                return
            if nodo.caracter is not None:
                codigos[nodo.caracter] = codigo_actual if codigo_actual else "0"
                return
            recorrer(nodo.izq, codigo_actual + "0")
            recorrer(nodo.der, codigo_actual + "1")

        recorrer(raiz, "")
        return codigos

    def codificar_texto(self, texto, codigos):
        return "".join(codigos[caracter] for caracter in texto)

    def decodificar_texto(self, texto_codificado, raiz):
        if raiz is None:
            return ""
        resultado = []
        nodo_actual = raiz
        # caso hoja única
        if raiz.izq and not raiz.der and raiz.izq.caracter:
            return raiz.izq.caracter * len(texto_codificado)
        for bit in texto_codificado:
            if bit == '0':
                nodo_actual = nodo_actual.izq
            else:
                nodo_actual = nodo_actual.der
            if nodo_actual is None:
                continue
            if nodo_actual.caracter is not None:
                resultado.append(nodo_actual.caracter)
                nodo_actual = raiz
        return "".join(resultado)

    def huffman_encode_bytes(self, s: str):
        # s es la string pa
        frecuencias = self._calcular_frecuencias(s)
        raiz = self._construir_arbol_huffman(frecuencias)
        codigos = self.generar_codigos(raiz)
        bits = self.codificar_texto(s, codigos)
        padding = (8 - len(bits) % 8) % 8
        bits_padded = bits + "0" * padding

        b_array = bytearray()
        for i in range(0, len(bits_padded), 8):
            byte_str = bits_padded[i:i + 8]
            b_array.append(int(byte_str, 2))

        cabecera = {
            'frecuencias': dict(frecuencias),
            'padding': padding
        }
        cabecera_json = json.dumps(cabecera)
        return cabecera_json.encode('utf-8'), bytes(b_array)

    def huffman_decode_bytes(self, cabecera_bytes: bytes, datos_bytes: bytes):
        cabecera_json_str = cabecera_bytes.decode('utf-8')
        cabecera = json.loads(cabecera_json_str)
        frecuencias = Counter(cabecera['frecuencias'])
        padding = cabecera['padding']
        raiz = self._construir_arbol_huffman(frecuencias)

        bits_string = "".join(f'{byte:08b}' for byte in datos_bytes)
        if padding > 0:
            bits_string = bits_string[:-padding]
        texto_decodificado = self.decodificar_texto(bits_string, raiz)
        return texto_decodificado

    def dsu_set(self, u):
        self.dsu_padre[u] = u
        self.dsu_ancestro[u] = u
        self.dsu_rango[u] = 0

    def dsu_encontrar(self, u):
        if self.dsu_padre[u] != u:
            self.dsu_padre[u] = self.dsu_encontrar(self.dsu_padre[u])
        return self.dsu_padre[u]

    def dsu_union(self, u, v):
        root_u = self.dsu_encontrar(u)
        root_v = self.dsu_encontrar(v)
        if root_u != root_v:
            if self.dsu_rango[root_u] < self.dsu_rango[root_v]:
                root_u, root_v = root_v, root_u
            self.dsu_padre[root_v] = root_u
            if self.dsu_rango[root_u] == self.dsu_rango[root_v]:
                self.dsu_rango[root_u] += 1

    def obtener_lca_tarjan(self, u_obj, v_obj):
        # Inicialización de estructuras DSU y auxiliares
        self.dsu_padre = list(range(self.n_maximo))
        self.dsu_ancestro = list(range(self.n_maximo))
        self.dsu_rango = [0] * self.n_maximo
        self.color = ["WHITE"] * self.n_maximo

        # Consultas
        self.queries = {i: [] for i in range(self.n_maximo)}
        self.queries[u_obj].append(v_obj)
        self.queries[v_obj].append(u_obj)

        self.resultado_tarjan = None

        # Ejecutar DFS de la raiz
        self.tarjan_dfs(1)
        return self.resultado_tarjan

    def tarjan_dfs(self, u):
        self.dsu_set(u)
        self.dsu_ancestro[u] = u

        for v in self.lista_adyacencia[u]:
            if self.color[v] == "WHITE":  # Si es hijo y no ha sido visitado
                if self.padre[v][0] == u:
                    self.tarjan_dfs(v)
                    self.dsu_union(u, v)
                    self.dsu_ancestro[self.dsu_encontrar(u)] = u

        self.color[u] = "BLACK"

        # Verificar consultas relacionadas con u
        for v in self.queries[u]:
            if self.color[v] == "BLACK":
                # El LCA es el ancestro del conjunto donde está v
                self.resultado_tarjan = self.dsu_ancestro[self.dsu_encontrar(v)]

    def obtener_lca_tarjan_generador(self, u_obj, v_obj):
        # Reiniciar estructuras
        self.dsu_padre = list(range(self.n_maximo))
        self.dsu_ancestro = list(range(self.n_maximo))
        self.dsu_rango = [0] * self.n_maximo
        self.color = ["WHITE"] * self.n_maximo

        self.queries = {i: [] for i in range(self.n_maximo)}
        self.queries[u_obj].append(v_obj)
        self.queries[v_obj].append(u_obj)

        # [nodo, indice_hijo, padre_directo]
        stack = [[1, 0, 0]]
        self.dsu_set(1)
        self.dsu_ancestro[1] = 1

        lca_encontrado = None

        while stack:
            u, idx, p = stack[-1]

            if idx == 0:
                yield u, None, "DFS Ingresando"

            # Procesar hijos
            hijos = [v for v in self.lista_adyacencia[u] if v != p]

            if idx < len(hijos):
                v = hijos[idx]
                stack[-1][1] += 1  # Avanzar indice para la próxima vuelta

                # Simular llamada recursiva
                self.dsu_set(v)
                self.dsu_ancestro[v] = v
                stack.append([v, 0, u])
                continue
            else:
                # Todos los hijos procesados (Post-order)
                stack.pop()
                self.color[u] = "BLACK"

                chequeando_con = None
                for q_node in self.queries[u]:
                    if self.color[q_node] == "BLACK":
                        lca = self.dsu_ancestro[self.dsu_encontrar(q_node)]
                        lca_encontrado = lca
                        chequeando_con = q_node
                        yield u, chequeando_con, f"Query ({u}, {q_node}) -> LCA: {lca}"
                        # En Tarjan real continuaríamos, pero aquí ya tenemos el resultado
                        return lca

                if not lca_encontrado:
                    yield u, None, "DFS Regresando (Post-order)"

                # Unión con el padre al regresar de la recursión
                if p != 0:
                    self.dsu_union(p, u)
                    self.dsu_ancestro[self.dsu_encontrar(p)] = p

        return lca_encontrado

    def reiniciar_estado(self):
        self.n_maximo = self.num_nodos + 1
        self.log_max = math.ceil(math.log2(self.n_maximo))
        self.lista_adyacencia = [[] for _ in range(self.n_maximo)]
        self.nivel = [0] * self.n_maximo
        self.padre = [[0] * (self.log_max + 1) for _ in range(self.n_maximo)]
        self.construir_lista_adyacencia()

    def preprocesar_algoritmos(self):
        # DFS de binary lifting
        stack = [(1, 0, 1)]
        visitados = {1}
        while stack:
            u, p, l = stack.pop()
            self.nivel[u] = l
            self.padre[u][0] = p
            for v in self.lista_adyacencia[u]:
                if v != p and v not in visitados:
                    visitados.add(v)
                    stack.append((v, u, l + 1))
        # Tabla de saltos
        for i in range(1, self.log_max + 1):
            for u in range(1, self.num_nodos + 1):
                ancestro_intermedio = self.padre[u][i - 1]
                if ancestro_intermedio != 0:
                    self.padre[u][i] = self.padre[ancestro_intermedio][i - 1]

    def construir_lista_adyacencia(self):
        # reconstruye lista en base a self.aristas y self.n_maximo
        self.lista_adyacencia = [[] for _ in range(self.n_maximo)]
        for u, v in self.aristas:
            if u < self.n_maximo and v < self.n_maximo:
                self.lista_adyacencia[u].append(v)
                self.lista_adyacencia[v].append(u)

    # Generadores para Simulación de Preprocesamiento
    def dfs_generador(self, u, p, l, visitados):
        visitados.add(u)
        self.nivel[u] = l
        self.padre[u][0] = p
        yield u, p, set(visitados)
        for v in self.lista_adyacencia[u]:
            if v != p:
                yield from self.dfs_generador(v, u, l + 1, visitados)

    def construir_tabla_dispersa_generador(self):
        for i in range(1, self.log_max + 1):
            for u in range(1, self.num_nodos + 1):
                ancestro_intermedio = self.padre[u][i - 1]
                if ancestro_intermedio != 0:
                    ancestro_final = self.padre[ancestro_intermedio][i - 1]
                    self.padre[u][i] = ancestro_final
                    yield u, i, ancestro_intermedio, ancestro_final
                else:
                    yield u, i, 0, 0

    def obtener_lca(self, u, v):
        if self.nivel[u] > self.nivel[v]:
            u, v = v, u
        for i in range(self.log_max, -1, -1):
            if self.nivel[v] - (1 << i) >= self.nivel[u]:
                v = self.padre[v][i]
        if u == v:
            return u
        for i in range(self.log_max, -1, -1):
            if self.padre[u][i] != 0 and self.padre[u][i] != self.padre[v][i]:
                u = self.padre[u][i]
                v = self.padre[v][i]
        return self.padre[u][0]

    def obtener_lca_fuerza_bruta(self, u, v):
        while self.nivel[u] > self.nivel[v]:
            u = self.padre[u][0]
        while self.nivel[v] > self.nivel[u]:
            v = self.padre[v][0]
        while u != v:
            u = self.padre[u][0]
            v = self.padre[v][0]
        return u

    # eneradores para Simulación Visual de Consulta
    def obtener_lca_generador(self, u, v):
        if self.nivel[u] > self.nivel[v]:
            u, v = v, u
        for i in range(self.log_max, -1, -1):
            if self.nivel[v] - (1 << i) >= self.nivel[u]:
                v = self.padre[v][i]
                yield u, v
        if u == v:
            yield u, v
            return u
        for i in range(self.log_max, -1, -1):
            if self.padre[u][i] != 0 and self.padre[u][i] != self.padre[v][i]:
                u = self.padre[u][i]
                v = self.padre[v][i]
                yield u, v
        yield u, v
        return self.padre[u][0]

    def obtener_lca_fuerza_bruta_generador(self, u, v):
        while self.nivel[u] > self.nivel[v]:
            u = self.padre[u][0]
            yield u, v
        while self.nivel[v] > self.nivel[u]:
            v = self.padre[v][0]
            yield u, v
        while u != v:
            u = self.padre[u][0]
            v = self.padre[v][0]
            yield u, v
        yield u, v
        return u

    # Creación de la GUI
    def crear_componentes(self):
        main_frame = tk.Frame(self.ventana_principal)
        main_frame.pack(fill=tk.BOTH, expand=True)

        controles_frame = tk.Frame(main_frame, width=320, padx=10, pady=10)
        controles_frame.pack(side=tk.LEFT, fill=tk.Y)
        controles_frame.pack_propagate(False)

        # Sección de Preprocesamiento
        prep_frame = ttk.LabelFrame(controles_frame, text="1. Simular Preprocesamiento")
        prep_frame.pack(fill=tk.X, pady=10)
        self.btn_sim_dfs = tk.Button(prep_frame, text="Simular DFS (Niveles y Padres)",
                                     command=self.iniciar_simulacion_dfs)
        self.btn_sim_dfs.pack(fill=tk.X, padx=5, pady=5)
        self.btn_sim_tabla = tk.Button(prep_frame, text="Simular Tabla de Saltos",
                                       command=self.iniciar_simulacion_tabla_dispersa)
        self.btn_sim_tabla.pack(fill=tk.X, padx=5, pady=5)

        # Sección de Consulta y Medición
        query_frame = ttk.LabelFrame(controles_frame, text="2. Medir y Simular Búsqueda")
        query_frame.pack(fill=tk.X, pady=10)

        nodos_frame = tk.Frame(query_frame)
        nodos_frame.pack(pady=5)
        tk.Label(nodos_frame, text="N1:").pack(side=tk.LEFT)
        self.entrada_nodo1 = tk.Entry(nodos_frame, width=4)
        self.entrada_nodo1.pack(side=tk.LEFT)
        self.entrada_nodo1.insert(0, "7")
        tk.Label(nodos_frame, text="N2:").pack(side=tk.LEFT, padx=(10, 0))
        self.entrada_nodo2 = tk.Entry(nodos_frame, width=4)
        self.entrada_nodo2.pack(side=tk.LEFT)
        self.entrada_nodo2.insert(0, "4")
        self.algoritmo_seleccionado = tk.StringVar(value="divide_y_venceras")

        self.rb_bl = tk.Radiobutton(query_frame, text="Divide y Vencerás", variable=self.algoritmo_seleccionado,
                                    value="divide_y_venceras")
        self.rb_bl.pack(anchor='w', padx=5)

        self.rb_fb = tk.Radiobutton(query_frame, text="Fuerza Bruta", variable=self.algoritmo_seleccionado,
                                    value="fuerza_bruta")
        self.rb_fb.pack(anchor='w', padx=5)

        self.rb_tj = tk.Radiobutton(query_frame, text="Tarjan Offline (DSU)", variable=self.algoritmo_seleccionado,
                                    value="tarjan")
        self.rb_tj.pack(anchor='w', padx=5)

        self.btn_ejecutar = tk.Button(query_frame, text="Calcular, Medir y Simular",
                                      command=self.ejecutar_medicion_y_simulacion)
        self.btn_ejecutar.pack(fill=tk.X, padx=5, pady=5)
        self.etiqueta_resultado = tk.Label(query_frame, text="Resultado: ...", justify=tk.LEFT,
                                           font=("Arial", 10, "bold"))
        self.etiqueta_resultado.pack(pady=5, anchor='w')

        # Sección de Gráficos de Complejidad
        analysis_frame = ttk.LabelFrame(controles_frame, text="3. Análisis de Complejidad")
        analysis_frame.pack(fill=tk.X, pady=10)
        btn_graficar = tk.Button(analysis_frame, text="Ver Gráficos de Complejidad",
                                 command=self.graficar_complejidad_medida)
        btn_graficar.pack(fill=tk.X, padx=5, pady=5)
        btn_limpiar = tk.Button(analysis_frame, text="Limpiar Datos", command=self.limpiar_datos)
        btn_limpiar.pack(fill=tk.X, padx=5, pady=(0, 5))

        # Sección de Compresión
        comp_frame = ttk.LabelFrame(controles_frame, text="4. Guardar/Cargar Estructura (Comprimida)")
        comp_frame.pack(fill=tk.X, pady=10)
        btn_guardar = tk.Button(comp_frame, text="Guardar Estructura Comprimida (.huff)",
                                command=self.guardar_estructura_comprimida)
        btn_guardar.pack(fill=tk.X, padx=5, pady=5)
        btn_cargar = tk.Button(comp_frame, text="Cargar Estructura Comprimida (.huff)",
                               command=self.cargar_estructura_comprimida)
        btn_cargar.pack(fill=tk.X, padx=5, pady=5)

        self.lienzo = tk.Canvas(main_frame, bg="white")
        self.lienzo.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def controlar_widgets(self, estado):
        state = tk.NORMAL if estado else tk.DISABLED
        self.btn_sim_dfs.config(state=state)
        self.btn_sim_tabla.config(state=state)
        self.btn_ejecutar.config(state=state)
        self.rb_bl.config(state=state)
        self.rb_fb.config(state=state)
        self.rb_tj.config(state=state)
        self.simulacion_activa = not estado

    # Lógica de Medición y Simulación
    def ejecutar_medicion_y_simulacion(self):
        if self.simulacion_activa: return
        try:
            u, v = int(self.entrada_nodo1.get()), int(self.entrada_nodo2.get())

            # Comprueba contra el diccionario de coordenadas
            if u not in self.coordenadas or v not in self.coordenadas:
                messagebox.showerror("Error", f"Nodos inválidos. Por favor ingrese números entre 1 y {self.num_nodos}.")
                return

            algo_seleccionado = self.algoritmo_seleccionado.get()
            tracemalloc.start()

            if algo_seleccionado == "divide_y_venceras":
                start_time = time.perf_counter()
                lca = self.obtener_lca(u, v)
                end_time = time.perf_counter()
            elif algo_seleccionado == "tarjan":  # <-- BLOQUE AGREGADO
                start_time = time.perf_counter()
                lca = self.obtener_lca_tarjan(u, v)
                end_time = time.perf_counter()
            else:
                start_time = time.perf_counter()
                lca = self.obtener_lca_fuerza_bruta(u, v)
                end_time = time.perf_counter()

            memoria_actual, memoria_pico = tracemalloc.get_traced_memory()
            tracemalloc.stop()

            tiempo_ejecucion = end_time - start_time
            self.num_busquedas += 1

            self.datos_rendimiento.append({
                'id': self.num_busquedas,
                'algoritmo': algo_seleccionado,
                'tiempo': tiempo_ejecucion,
                'memoria': memoria_pico
            })

            resultado_texto = (f"Resultado: LCA({u},{v}) = {lca}\n"
                               f"Tiempo: {tiempo_ejecucion:.6f} s\n"
                               f"Espacio: {memoria_pico} bytes")
            self.etiqueta_resultado.config(text=resultado_texto)
            self.iniciar_simulacion_lca_visual(u, v)
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese números válidos en las entradas de nodos.")

    # Lógica de Simulaciones Visuales
    def iniciar_simulacion_dfs(self):
        if self.simulacion_activa: return
        self.controlar_widgets(False)
        self.reiniciar_estado()
        self.etiqueta_resultado.config(text="Simulando DFS...")
        generador = self.dfs_generador(1, 0, 1, set())
        self.paso_simulacion_dfs(generador)

    def paso_simulacion_dfs(self, generador):
        try:
            u, p, visitados = next(generador)
            info = f"Visitando nodo: {u}\nPadre: {p}\nNivel: {self.nivel[u]}"
            self.dibujar_arbol(nodos_visitados=visitados, nodo_actual_dfs=u, info_texto=info)
            self.ventana_principal.after(400, lambda: self.paso_simulacion_dfs(generador))
        except StopIteration:
            self.dibujar_arbol(nodos_visitados=set(range(1, self.num_nodos + 1)))
            self.etiqueta_resultado.config(text="DFS completado.")
            self.controlar_widgets(True)

    def iniciar_simulacion_tabla_dispersa(self):
        if self.simulacion_activa: return
        self.controlar_widgets(False)
        self.reiniciar_estado()
        # Se necesita ejecutar el DFS primero para tener los padres directos
        for _ in self.dfs_generador(1, 0, 1, set()):
            pass
        self.etiqueta_resultado.config(text="Simulando Tabla...")
        self.crear_ventana_tabla()
        generador = self.construir_tabla_dispersa_generador()
        self.paso_simulacion_tabla(generador)

    def paso_simulacion_tabla(self, generador):
        try:
            u, i, p_intermedio, p_final = next(generador)
            for label in self.tabla_labels.values():
                label.config(bg='white')
            if (u, i) in self.tabla_labels:
                self.tabla_labels[(u, i)].config(bg='yellow')

            if p_final != 0:
                self.tabla_labels[(u, i)].config(text=str(p_final))
                camino = self.obtener_camino_hacia_ancestro(u, p_final)
                info = f"Calculando padre[u={u}][2^{i}={1 << i}]\n" \
                       f"Salto: {u} -> {p_intermedio} -> {p_final}"
            else:
                camino, info = [], f"Calculando padre[u={u}][2^{i}={1 << i}]\nNo hay ancestro."
            self.dibujar_arbol(camino_tabla=camino, info_texto=info)
            self.ventana_principal.after(300, lambda: self.paso_simulacion_tabla(generador))
        except StopIteration:
            self.dibujar_arbol()
            self.etiqueta_resultado.config(text="Tabla de saltos completada.")
            self.controlar_widgets(True)

    def iniciar_simulacion_lca_visual(self, u, v):
        self.controlar_widgets(False)
        self.dibujar_arbol(resaltar_iniciales=(u, v))

        sel = self.algoritmo_seleccionado.get()

        if sel == "divide_y_venceras":
            generador = self.obtener_lca_generador(u, v)
            self.paso_simulacion_lca_visual(u, v, generador)
        elif sel == "fuerza_bruta":
            generador = self.obtener_lca_fuerza_bruta_generador(u, v)
            self.paso_simulacion_lca_visual(u, v, generador)
        elif sel == "tarjan":
            generador = self.obtener_lca_tarjan_generador(u, v)
            self.paso_simulacion_tarjan_visual(u, v, generador)

    def paso_simulacion_lca_visual(self, u_inicial, v_inicial, generador):
        try:
            u_actual, v_actual = next(generador)
            camino_u = self.obtener_camino_hacia_ancestro(u_inicial, u_actual)
            camino_v = self.obtener_camino_hacia_ancestro(v_inicial, v_actual)
            self.dibujar_arbol(resaltar_iniciales=(u_inicial, v_inicial), resaltar_actuales=(u_actual, v_actual),
                               camino_u=camino_u, camino_v=camino_v)
            self.ventana_principal.after(500, lambda: self.paso_simulacion_lca_visual(u_inicial, v_inicial, generador))
        except StopIteration as e:
            lca = e.value
            camino_u = self.obtener_camino_hacia_ancestro(u_inicial, lca)
            camino_v = self.obtener_camino_hacia_ancestro(v_inicial, lca)
            self.dibujar_arbol(resaltar_iniciales=(u_inicial, v_inicial), resaltar_lca=lca, camino_u=camino_u,
                               camino_v=camino_v)
            self.controlar_widgets(True)

    def paso_simulacion_tarjan_visual(self, u_inicial, v_inicial, generador):
        try:
            res = next(generador)

            # Si el generador retorna el resultado final directamente
            if not isinstance(res, tuple):
                lca = res
                raise StopIteration(lca)

            u_actual, nodo_check, msg = res

            visitados_set = {n for n in range(1, self.num_nodos + 1) if self.color[n] == "BLACK"}

            self.dibujar_arbol(
                resaltar_iniciales=(u_inicial, v_inicial),
                nodo_actual_dfs=u_actual,
                nodos_visitados=visitados_set,
                info_texto=f"Tarjan DFS: {msg}"
            )

            # Si estamos chequeando query, resaltar el nodo contraparte
            if nodo_check:
                x1, y1 = self.coordenadas[u_actual]
                x2, y2 = self.coordenadas[nodo_check]
                self.lienzo.create_line(x1, y1, x2, y2, fill="green", dash=(4, 2), width=2)

            self.ventana_principal.after(500,
                                         lambda: self.paso_simulacion_tarjan_visual(u_inicial, v_inicial, generador))

        except StopIteration as e:
            lca = e.value
            if lca is None: lca = self.resultado_tarjan

            camino_u = self.obtener_camino_hacia_ancestro(u_inicial, lca)
            camino_v = self.obtener_camino_hacia_ancestro(v_inicial, lca)

            self.dibujar_arbol(
                resaltar_iniciales=(u_inicial, v_inicial),
                resaltar_lca=lca,
                camino_u=camino_u,
                camino_v=camino_v,
                info_texto=f"Tarjan completado. LCA: {lca}"
            )
            self.controlar_widgets(True)

    def limpiar_datos(self):
        if messagebox.askyesno("Confirmar",
                               "¿Está seguro de que desea borrar todos los datos de complejidad recolectados?"):
            self.datos_rendimiento = []
            self.num_busquedas = 0
            messagebox.showinfo("Éxito", "Los datos de complejidad han sido borrados.")

    def guardar_estructura_comprimida(self):
        # Serializa la estructura que queremos guardar
        estructura = {
            'num_nodos': self.num_nodos,
            'aristas': self.aristas,
            'coordenadas': self.coordenadas
        }
        json_str = json.dumps(estructura, ensure_ascii=False)
        # Codificar con Huffman (cabecera + bytes)
        cabecera_b, datos_b = self.huffman_encode_bytes(json_str)

        ruta_salida = filedialog.asksaveasfilename(
            title="Guardar estructura comprimida",
            defaultextension=".huff",
            filetypes=[("Archivos Huffman", "*.huff")]
        )
        if not ruta_salida:
            return
        try:
            with open(ruta_salida, "wb") as f:
                f.write(cabecera_b + b'\n')
                f.write(datos_b)
            tam_orig = len(json_str.encode('utf-8'))
            tam_comp = os.path.getsize(ruta_salida)
            tasa = (1 - tam_comp / tam_orig) * 100 if tam_orig > 0 else 0
            messagebox.showinfo("Éxito",
                                f"Estructura comprimida guardada:\n{ruta_salida}\n\nTamaño JSON: {tam_orig} bytes\nTamaño .huff: {tam_comp} bytes\nTasa de compresión: {tasa:.2f}%")
        except Exception as e:
            messagebox.showerror("Error al guardar", f"No se pudo escribir el archivo comprimido.\n{e}")

    def cargar_estructura_comprimida(self):
        ruta_entrada = filedialog.askopenfilename(
            title="Seleccionar archivo .huff para cargar",
            filetypes=[("Archivos Huffman", "*.huff")]
        )
        if not ruta_entrada:
            return
        try:
            with open(ruta_entrada, "rb") as f:
                cabecera_line = f.readline()
                cabecera_bytes = cabecera_line.rstrip(b'\n')
                datos_bytes = f.read()

            json_str = self.huffman_decode_bytes(cabecera_bytes, datos_bytes)
            estructura = json.loads(json_str)

            # Validaciones básicas
            if 'num_nodos' not in estructura or 'aristas' not in estructura or 'coordenadas' not in estructura:
                messagebox.showerror("Error", "El archivo .huff no contiene la estructura esperada.")
                return

            self.num_nodos = int(estructura['num_nodos'])
            # Forzamos conversiones
            self.aristas = [tuple(map(int, a)) for a in estructura['aristas']]
            coords = {}
            for k, v in estructura['coordenadas'].items():
                try:
                    key = int(k)
                except:
                    key = int(str(k))
                coords[key] = tuple(v)
            self.coordenadas = coords

            self.reiniciar_estado()
            # Ejecutar DFS para niveles/padres y reconstruir tabla
            self.preprocesar_algoritmos()
            self.dibujar_arbol()
            messagebox.showinfo("Éxito", f"Estructura cargada desde:\n{ruta_entrada}")
        except Exception as e:
            messagebox.showerror("Error al cargar", f"No se pudo cargar el archivo comprimido.\n{e}")

    # Gráficos y Lógica Auxiliar
    def dibujar_arbol(self, **kwargs):
        self.lienzo.delete("all")
        nodos_visitados = kwargs.get('nodos_visitados', set())
        nodo_actual_dfs = kwargs.get('nodo_actual_dfs')
        camino_tabla = kwargs.get('camino_tabla', [])
        resaltar_iniciales = kwargs.get('resaltar_iniciales')
        resaltar_actuales = kwargs.get('resaltar_actuales')
        resaltar_lca = kwargs.get('resaltar_lca')
        camino_u = kwargs.get('camino_u')
        camino_v = kwargs.get('camino_v')
        self.lienzo.create_text(10, 10, anchor='nw', text=kwargs.get('info_texto', ''))
        for u, v in self.aristas:
            # si alguna arista refiere nodos que no existan en coordenadas, saltar
            if u not in self.coordenadas or v not in self.coordenadas:
                continue
            self.lienzo.create_line(self.coordenadas[u], self.coordenadas[v], fill="lightgray", width=2)
        for camino in [camino_u, camino_v, camino_tabla]:
            if camino and len(camino) > 1:
                for i in range(len(camino) - 1):
                    if camino[i] in self.coordenadas and camino[i + 1] in self.coordenadas:
                        self.lienzo.create_line(self.coordenadas[camino[i]], self.coordenadas[camino[i + 1]],
                                                fill="red",
                                                width=3)
        for nodo, (x, y) in self.coordenadas.items():
            color_relleno = "lightblue"
            if nodo in nodos_visitados:
                color_relleno = "lightgray"
            if resaltar_iniciales and nodo in resaltar_iniciales:
                color_relleno = "deepskyblue"
            if resaltar_actuales and nodo in resaltar_actuales:
                color_relleno = "orange"
            if nodo == nodo_actual_dfs:
                color_relleno = "violet"
            if nodo == resaltar_lca:
                color_relleno = "lightgreen"
            self.lienzo.create_oval(x - self.radio_nodo, y - self.radio_nodo, x + self.radio_nodo, y + self.radio_nodo,
                                    fill=color_relleno, outline="black", width=2)
            self.lienzo.create_text(x, y, text=str(nodo), font=("Arial", 12, "bold"))

    def crear_ventana_tabla(self):
        win = tk.Toplevel(self.ventana_principal)
        win.title("Tabla de Ancestros (padre[u][i])")
        tk.Label(win, text="u \\ i", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5, pady=2)
        for i in range(self.log_max + 1):
            tk.Label(win, text=f"{i}", font=("Arial", 10, "bold")).grid(row=0, column=i + 1, padx=5, pady=2)
            tk.Label(win, text=f"(2^{i})", font=("Arial", 8)).grid(row=1, column=i + 1)
        for u in range(1, self.num_nodos + 1):
            tk.Label(win, text=f"{u}", font=("Arial", 10, "bold")).grid(row=u + 1, column=0, padx=5, pady=2)
            for i in range(self.log_max + 1):
                val = self.padre[u][i] if i == 0 else "?"
                label = tk.Label(win, text=str(val), width=4, relief="ridge")
                label.grid(row=u + 1, column=i + 1)
                self.tabla_labels[(u, i)] = label

    def obtener_camino_hacia_ancestro(self, u_start, u_end):
        if u_start == 0 or u_end == 0:
            return []
        camino = [u_start]
        curr = u_start
        for _ in range(self.num_nodos + 1):
            if curr == u_end:
                break
            curr = self.padre[curr][0]
            if curr == 0:
                return []
            camino.append(curr)
        return camino

    def graficar_complejidad_medida(self):
        if not self.datos_rendimiento:
            messagebox.showinfo("Sin Datos",
                                "No hay datos de complejidad para graficar. Realice algunas búsquedas primero.")
            return
        datos_bl = [d for d in self.datos_rendimiento if d['algoritmo'] == 'divide_y_venceras']
        datos_fb = [d for d in self.datos_rendimiento if d['algoritmo'] == 'fuerza_bruta']
        datos_tj = [d for d in self.datos_rendimiento if d['algoritmo'] == 'tarjan']

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5.5))
        fig.suptitle('Complejidad de Búsquedas LCA', fontsize=16)

        # Gráfico de Complejidad Temporal
        if datos_bl:
            ax1.plot([d['id'] for d in datos_bl], [d['tiempo'] for d in datos_bl], label='Divide y Vencerás (O(log N))',
                     marker='o', linestyle='-')
        if datos_fb:
            ax1.plot([d['id'] for d in datos_fb], [d['tiempo'] for d in datos_fb], label='Fuerza Bruta (O(N))',
                     marker='x', linestyle='-')
        if datos_tj:
            ax1.plot([d['id'] for d in datos_tj], [d['tiempo'] for d in datos_tj], label='Tarjan (O(N+Q))',
                     marker='s', linestyle='-')

        ax1.set_title('Complejidad Temporal')
        ax1.set_xlabel('Número de Búsqueda')
        ax1.set_ylabel('Tiempo')
        ax1.legend()
        ax1.grid(True)
        ax1.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))

        # Gráfico de Complejidad Espacial
        if datos_bl:
            ax2.plot([d['id'] for d in datos_bl], [d['memoria'] for d in datos_bl],
                     label='Divide y Vencerás (O(N log N))', marker='o', linestyle='-')
        if datos_fb:
            ax2.plot([d['id'] for d in datos_fb], [d['memoria'] for d in datos_fb], label='Fuerza Bruta (O(N))',
                     marker='x', linestyle='-')
        if datos_tj:
            ax2.plot([d['id'] for d in datos_tj], [d['memoria'] for d in datos_tj], label='Tarjan (DSU)',
                     marker='s', linestyle='-')

        ax2.set_title('Complejidad Espacial')
        ax2.set_xlabel('Número de Búsqueda')
        ax2.set_ylabel('Memoria (bytes)')
        ax2.legend()
        ax2.grid(True)

        fig.tight_layout(rect=[0, 0.03, 1, 0.95])
        win = tk.Toplevel(self.ventana_principal)
        win.title("Gráficos de Complejidad")
        win.geometry("1100x600")
        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    raiz = tk.Tk()
    aplicacion = VisualizadorLCA(raiz)
    raiz.mainloop()