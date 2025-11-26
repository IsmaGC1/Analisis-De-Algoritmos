# Visualizador de Algoritmos LCA (Lowest Common Ancestor)

Este proyecto es una aplicación con GUI desarrollada en **Python** que permite visualizar, simular y analizar el rendimiento de diferentes algoritmos para encontrar el **Ancestro Común Más Bajo (LCA)** en una estructura de datos de árbol.

La herramienta incluye animaciones paso a paso, gráficos de complejidad temporal/espacial y una utilidad extra de compresión de datos utilizando codificación Huffman.

## Características Principales

* **Visualización de Árboles:** Representación gráfica de nodos y aristas con coordenadas predefinidas.
* **Algoritmos Implementados:**
    1.  **Fuerza Bruta:** Búsqueda ingenua ascendiendo por los padres hasta encontrar la intersección.
    2.  **Binary Lifting (Divide y Vencerás):** Preprocesamiento con tabla de saltos (Sparse Table) para consultas en tiempo logarítmico O(log N).
    3.  **Algoritmo de Tarjan (Offline):** Uso de estructuras de conjuntos disjuntos (DSU - Union Find) para procesar consultas.
* **Análisis de Rendimiento:** Medición en tiempo real del tiempo de ejecución y uso de memoria (usando `tracemalloc`), con generación de gráficos comparativos mediante `matplotlib`.
* **Simulación Paso a Paso:** Animaciones visuales del funcionamiento interno de los algoritmos (DFS, construcción de tablas, recorrido de búsqueda).
* **Persistencia Comprimida:** Capacidad de guardar y cargar la estructura del árbol en un formato binario propio (`.huff`) comprimido mediante el algoritmo de **Huffman**.

## Requisitos y Dependencias

Para ejecutar este proyecto necesitas tener instalado **Python 3.x**.

El código utiliza las siguientes librerías estándar de Python (no requieren instalación adicional):
* `tkinter` (Interfaz Gráfica)
* `math`, `time`, `tracemalloc`, `heapq`, `json`, `collections`, `os`

### Librerías de Terceros
El proyecto requiere **Matplotlib** para la generación de gráficos de complejidad. Debes instalarlo ejecutando el siguiente comando en tu terminal:

```bash
pip install matplotlib
```

## Instrucciones de Ejecución

1.  Clona este repositorio o descarga el archivo del código fuente (`Proyecto Final.py`).
2.  Abre una terminal o línea de comandos en la carpeta del proyecto.
3.  Ejecuta el script principal:

```bash
python "Proyecto Final.py"
```

4.  Se abrirá la ventana **"Visualizador de LCA - Completo"**.

## Guía de Uso

La interfaz está dividida en 4 secciones funcionales:

### 1. Simular Preprocesamiento
Antes de realizar búsquedas optimizadas, puedes ver cómo se prepara el árbol:
* **Simular DFS:** Muestra cómo el algoritmo recorre el árbol para asignar niveles y padres directos.
* **Simular Tabla de Saltos:** Visualiza cómo se llena la tabla de potencias de 2 para el algoritmo de *Binary Lifting*.

### 2. Medir y Simular Búsqueda
Aquí realizas las consultas de LCA entre dos nodos:
* Ingresa los IDs de los nodos en las casillas **N1** y **N2** (Rango 1-12).
* Selecciona el algoritmo deseado: *Divide y Vencerás*, *Fuerza Bruta* o *Tarjan*.
* Haz clic en **"Calcular, Medir y Simular"**.
* Observarás la animación en el árbol y el resultado (tiempo y memoria) en la etiqueta inferior.

### 3. Análisis de Complejidad
Después de ejecutar varias búsquedas con diferentes algoritmos:
* Haz clic en **"Ver Gráficos de Complejidad"**.
* Se abrirá una ventana con gráficas comparativas de **Tiempo vs Búsquedas** y **Memoria vs Búsquedas**.

### 4. Guardar/Cargar Estructura
* **Guardar:** Exporta la estructura actual del árbol a un archivo `.huff` comprimido.
* **Cargar:** Lee un archivo `.huff` previamente guardado y reconstruye el árbol en la interfaz.

---
**Proyecto De Ismael Gándara Cornejo y Ángel Miguel Villalvazo Vázquez - Análisis de Algoritmos**
