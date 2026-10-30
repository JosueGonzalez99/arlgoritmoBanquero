def _es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def _nombre_recurso(j):
    return chr(ord("A") + j)


def _validar_matriz(nombre, matriz, errores):
    for i in range(len(matriz)):
        for j in range(len(matriz[i])):
            valor = matriz[i][j]
            recurso = _nombre_recurso(j)
            if not _es_entero(valor):
                errores.append(f"{nombre}: P{i}, recurso {recurso} debe ser un número entero.")
            elif valor < 0:
                errores.append(f"{nombre}: P{i}, recurso {recurso} no puede ser negativo.")


def validar_datos(asignacion, maximo, disponible, solicitud=None):
    errores = []

    for j in range(len(disponible)):
        valor = disponible[j]
        recurso = _nombre_recurso(j)
        if not _es_entero(valor):
            errores.append(f"Available: el recurso {recurso} debe ser un número entero.")
        elif valor < 0:
            errores.append(f"Available: el recurso {recurso} no puede ser negativo.")

    _validar_matriz("Allocation", asignacion, errores)
    _validar_matriz("Max", maximo, errores)

    if solicitud is not None:
        for j in range(len(solicitud)):
            valor = solicitud[j]
            recurso = _nombre_recurso(j)
            if not _es_entero(valor):
                errores.append(f"Request: el recurso {recurso} debe ser un número entero.")
            elif valor < 0:
                errores.append(f"Request: el recurso {recurso} no puede ser negativo.")

    if errores:
        return errores

    for i in range(len(asignacion)):
        for j in range(len(asignacion[i])):
            if asignacion[i][j] > maximo[i][j]:
                errores.append(
                    f"Allocation supera a Max en P{i}, recurso {_nombre_recurso(j)} "
                    f"({asignacion[i][j]} > {maximo[i][j]})."
                )

    return errores