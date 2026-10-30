from logica.banquero import calcular_necesidad

maximo = [[3, 2, 2], [1, 2, 2], [2, 1, 1]]
asignacion = [[1, 0, 0], [0, 1, 0], [1, 0, 1]]

print(calcular_necesidad(maximo, asignacion))

from logica.banquero import algoritmo_seguridad

disponible = [3, 3, 2]
necesidad = calcular_necesidad(maximo, asignacion)
print(algoritmo_seguridad(disponible, asignacion, necesidad))

print(algoritmo_seguridad([0, 0, 0], [[1, 0, 0]], [[1, 0, 0]]))

from logica.validaciones import validar_datos

print(validar_datos([[2, 0, 0]], [[1, 0, 0]], [3, 3, 2]))
print(validar_datos([[1, 0, 0]], [[3, 2, 2]], [-1, 0, 0]))
print(validar_datos([[1, 0, 0]], [[3, 2, 2]], [3, 3, 2]))