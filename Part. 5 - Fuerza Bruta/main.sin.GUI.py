import numpy as np

def distancia_euclidiana(x1, y1, x2, y2):
   punto1 = np.array([x1, y1])
   punto2 = np.array([x2, y2])
   distancia = np.linalg.norm(punto2 - punto1)
   return distancia

def obtener_puntos():
   puntos = []
   for i in range(5):
       x = float(input(f"Coordenada x del punto {i + 1}: "))
       y = float(input(f"Coordenada y del punto {i + 1}: "))
       puntos.append((x, y))
   return puntos

def puntos_mas_cercanos(puntos):
   distancias = []
   for i in range(len(puntos)):
       for j in range(i + 1, len(puntos)):
           x1, y1 = puntos[i]
           x2, y2 = puntos[j]
           distancia = distancia_euclidiana(x1, y1, x2, y2)
           distancias.append(((i, j), distancia))
   distancias.sort(key=lambda x: x[1])
   (i, j), distancia = distancias[0]
   print(f"Los puntos más cercanos son P{i + 1} {puntos[i]} y P{j + 1} {puntos[j]}, con una distancia de {distancia:.2f}")

puntos = obtener_puntos()
puntos_mas_cercanos(puntos)
