class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None

def find_path(root, path, k):
    #Caso base
    if root is None:
        return False
    #Agrega el nodo actual al camino
    path.append(root.key)
    #Si el nodo actual es el buscado
    if root.key == k:
        return True
    # Busca en los subárboles izquierdo y derecho
    if ((root.left and find_path(root.left, path, k)) or
        (root.right and find_path(root.right, path, k))):
        return True
    # Si no se encuentra, retrocede
    path.pop()
    return False

def find_lca(root, n1, n2):
    path1 = []
    path2 = []
    #Si alguno de los nodos no está presente
    if not find_path(root, path1, n1) or not find_path(root, path2, n2):
        return -1
    #Compara las rutas para encontrar el último nodo común
    i = 0
    while i < len(path1) and i < len(path2):
        if path1[i] != path2[i]:
            break
        i += 1
    return path1[i - 1]

#Ejemplo de uso
if __name__ == "__main__":
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    root.right.left = Node(6)
    root.right.right = Node(7)

    lca = find_lca(root, 4, 5)
    if lca != -1:
        print(f"El LCA de 4 y 5 es {lca}")
    else:
        print("Al menos uno de los nodos no está en el árbol.")

    lca = find_lca(root, 4, 6)
    if lca != -1:
        print(f"El LCA de 4 y 6 es {lca}")
    else:
        print("Al menos uno de los nodos no está en el árbol.")
