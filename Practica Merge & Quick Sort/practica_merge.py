def merge(izquierda, derecha):
    resultado = []
    i, j = 0, 0

    while i < len(izquierda) and j < len(derecha):
        if izquierda[i] < derecha[j]:
            resultado.append(izquierda[i])
            i += 1
        else:
            resultado.append(derecha[j])
            j += 1

    resultado.extend(izquierda[i:])
    resultado.extend(derecha[j:])

    return resultado


def merge_sort(lista):
    if len(lista) <= 1:
        return lista

    medio = len(lista) // 2

    izquierda = merge_sort(lista[:medio])
    derecha = merge_sort(lista[medio:])

    return merge(izquierda, derecha)


array_merge = [7, 38, 27, 43, 3, 9, 82, 10]
sorted_arr_merge = merge_sort(array_merge)
print("Arreglo ordenado con Merge Sort:", sorted_arr_merge)