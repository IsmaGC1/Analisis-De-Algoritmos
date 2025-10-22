# Visualizador y Comparador de Algoritmos LCA

Este es un **programa** de escritorio desarrollado en Python con Tkinter que permite visualizar, simular y comparar el rendimiento de dos algoritmos para encontrar el **Ancestro Común más Bajo** (LCA, por sus siglas en inglés: *Lowest Common Ancestor*) en un árbol.

El programa utiliza `Matplotlib` para graficar la complejidad temporal y espacial de las búsquedas y `tracemalloc` para medir el uso de memoria.

---

## Características Principales

* **Visualización Interactiva:** Dibuja un árbol estático predefinido y resalta los nodos y caminos durante las simulaciones.
* **Simulación de Preprocesamiento:**
    * Muestra paso a paso la ejecución de **DFS** (Búsqueda en Profundidad) para calcular los niveles y padres directos de cada nodo.
    * Muestra la construcción de la **Tabla de Saltos** utilizada por el algoritmo Binary Lifting, en una ventana emergente.
* **Simulación de Búsqueda:** Anima el proceso de búsqueda del LCA para ambos algoritmos, mostrando cómo los nodos "escalan" por el árbol hasta encontrarse.
* **Medición de Rendimiento:** Utiliza `time.perf_counter` y `tracemalloc` para capturar el tiempo de ejecución exacto y el uso de memoria pico de cada consulta.
* **Análisis de Complejidad:** Genera gráficos de dispersión en tiempo real que comparan el rendimiento (tiempo y espacio) de los algoritmos a medida que el usuario realiza más búsquedas.

---

## Algoritmos Comparados

La herramienta implementa y compara dos métodos distintos para encontrar el LCA:

1.  **Fuerza Bruta**
    * **Búsqueda:** $O(N)$
    * Este método primero iguala el nivel de ambos nodos (subiendo al ancestro del nodo más profundo).
    * Luego, hace que ambos nodos suban un padre a la vez hasta que coinciden en el mismo nodo.
    * **Preprocesamiento:** $O(N)$ (solo necesita el DFS inicial).
    * **Espacio:** $O(N)$.

2.  **Binary Lifting (Divide y Vencerás)**
    * *(Etiquetado como "Divide y Vencerás" en la GUI)*.
    * **Búsqueda:** $O(\log N)$
    * Este método utiliza una tabla de preprocesamiento que permite a los nodos "saltar" $2^i$ ancestros de una sola vez.
    * Iguala los niveles usando saltos binarios y luego encuentra el LCA usando una técnica similar.
    * **Preprocesamiento:** $O(N \log N)$ (para construir la tabla de saltos).
    * **Espacio:** $O(N \log N)$.

---

## Instalación y Ejecución

Para ejecutar este programa, necesitas Python 3 o superior y la biblioteca `matplotlib`.

1.  Clona o descarga este repositorio.

2.  Instala las dependencias necesarias:
    ```bash
    pip install matplotlib
    ```

3.  Ejecuta el script principal (asegúrate de que el nombre coincida con tu archivo, por ejemplo `main.py` o `visualizador.py`):
    ```bash
    python tu_script.py
    ```

---

## Modo de Uso

La interfaz se divide en tres secciones principales:

### 1. Simular Preprocesamiento
* Usa los botones **"Simular DFS"** y **"Simular Tabla de Saltos"** para entender visualmente cómo se preparan las estructuras de datos antes de cualquier consulta.

### 2. Medir y Simular Búsqueda
1.  Introduce los dos nodos (N1 y N2) que deseas consultar.
2.  Selecciona el algoritmo a utilizar: "Divide y Vencerás" (Binary Lifting) o "Fuerza Bruta".
3.  Haz clic en **"Calcular, Medir y Simular"**.
4.  Observa el resultado (LCA, tiempo y memoria) en la parte izquierda.
5.  Observa la simulación visual de la búsqueda en el lienzo de la derecha.

### 3. Análisis de Complejidad
* Después de realizar varias búsquedas con ambos algoritmos, haz clic en **"Ver Gráficos de Complejidad"**.
* Esto abrirá una nueva ventana con dos gráficos que comparan el **Tiempo (segundos)** y la **Memoria (bytes)** de todas las búsquedas realizadas.
* Usa el botón **"Limpiar Datos"** para reiniciar las métricas.

---

## dependencies
* Python 3
* Tkinter
* Matplotlib
