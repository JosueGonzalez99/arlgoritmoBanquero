def calcular_necesidad(maximo, asignacion):
    necesidad = []
    for i in range(len(maximo)):
        fila = []
        for j in range(len(maximo[i])):
            fila.append(maximo[i][j] - asignacion[i][j])
        necesidad.append(fila)
    return necesidad


def algoritmo_seguridad(disponible, asignacion, necesidad):
    n = len(asignacion)
    m = len(disponible)

    work = disponible[:]
    finish = [False] * n
    secuencia = []
    pasos = []

    encontrado = True
    while encontrado:
        encontrado = False
        for i in range(n):
            if finish[i]:
                continue

            puede_terminar = True
            for j in range(m):
                if necesidad[i][j] > work[j]:
                    puede_terminar = False
                    break

            if puede_terminar:
                work_antes = work[:]
                for j in range(m):
                    work[j] += asignacion[i][j]

                finish[i] = True
                secuencia.append(i)
                pasos.append({
                    "proceso": i,
                    "necesidad": necesidad[i][:],
                    "work_antes": work_antes,
                    "work_despues": work[:],
                })
                encontrado = True

    es_seguro = all(finish)
    return es_seguro, secuencia, pasos


def evaluar_solicitud(disponible, asignacion, necesidad, proceso_idx, solicitud):
    m = len(disponible)

    for j in range(m):
        if solicitud[j] > necesidad[proceso_idx][j]:
            return {
                "otorgado": False,
                "motivo": "supera_necesidad",
                "recurso": j,
                "valor_solicitado": solicitud[j],
                "valor_limite": necesidad[proceso_idx][j],
            }

    for j in range(m):
        if solicitud[j] > disponible[j]:
            return {
                "otorgado": False,
                "motivo": "supera_disponible",
                "recurso": j,
                "valor_solicitado": solicitud[j],
                "valor_limite": disponible[j],
            }

    nuevo_disponible = [disponible[j] - solicitud[j] for j in range(m)]
    nueva_asignacion = [fila[:] for fila in asignacion]
    nueva_necesidad = [fila[:] for fila in necesidad]

    for j in range(m):
        nueva_asignacion[proceso_idx][j] += solicitud[j]
        nueva_necesidad[proceso_idx][j] -= solicitud[j]

    es_seguro, secuencia, pasos = algoritmo_seguridad(
        nuevo_disponible, nueva_asignacion, nueva_necesidad
    )

    return {
        "otorgado": es_seguro,
        "motivo": "seguro" if es_seguro else "inseguro",
        "disponible": nuevo_disponible,
        "asignacion": nueva_asignacion,
        "necesidad": nueva_necesidad,
        "es_seguro": es_seguro,
        "secuencia": secuencia,
        "pasos": pasos,
    }