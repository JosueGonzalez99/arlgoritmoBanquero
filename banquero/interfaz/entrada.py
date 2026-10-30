import pandas as pd
import streamlit as st


def _nombres_procesos(n):
    return [f"P{i}" for i in range(n)]


def _nombres_recursos(m):
    return [chr(ord("A") + j) for j in range(m)]


def _convertir(valor):
    if pd.isna(valor):
        return None
    if isinstance(valor, float) and valor.is_integer():
        return int(valor)
    return valor


def _tabla(titulo, clave, filas, columnas, n, m, datos_iniciales=0):
    st.subheader(titulo)
    base = pd.DataFrame(datos_iniciales, index=filas, columns=columnas)
    configuracion = {
        columna: st.column_config.NumberColumn(columna, step=1, format="%d")
        for columna in columnas
    }
    editada = st.data_editor(
        base,
        key=f"{clave}_{n}_{m}",
        column_config=configuracion,
        use_container_width=True,
    )
    return [[_convertir(valor) for valor in fila] for fila in editada.values.tolist()]


def pedir_datos():
    col_chk1, col_chk2 = st.columns(2)
    with col_chk1:
        usar_ejemplo = st.checkbox("Cargar datos de prueba (5 procesos, 3 recursos)")
    with col_chk2:
        activar_solicitud = st.checkbox("Simular solicitud adicional de recursos (Request)")

    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input(
            "Número de procesos (N)",
            min_value=1,
            max_value=20,
            value=5 if usar_ejemplo else 3,
            step=1,
            disabled=usar_ejemplo,
        )
    with col2:
        m = st.number_input(
            "Número de tipos de recursos (M)",
            min_value=1,
            max_value=26,
            value=3,
            step=1,
            disabled=usar_ejemplo,
        )

    n = int(n)
    m = int(m)
    procesos = _nombres_procesos(n)
    recursos = _nombres_recursos(m)

    if usar_ejemplo:
        init_alloc = [[0, 1, 0], [2, 0, 0], [3, 0, 2], [2, 1, 1], [0, 0, 2]]
        init_max = [[7, 5, 3], [3, 2, 2], [9, 0, 2], [2, 2, 2], [4, 3, 3]]
        init_avail = [[3, 3, 2]]
        init_req = [[1, 0, 2]]
        sufijo = "ejemplo"
    else:
        init_alloc = 0
        init_max = 0
        init_avail = 0
        init_req = 0
        sufijo = "manual"

    col_a, col_b = st.columns(2)
    with col_a:
        asignacion = _tabla(
            "Allocation (recursos asignados)",
            f"asignacion_{sufijo}",
            procesos,
            recursos,
            n,
            m,
            init_alloc,
        )
    with col_b:
        maximo = _tabla(
            "Max (demanda máxima)",
            f"maximo_{sufijo}",
            procesos,
            recursos,
            n,
            m,
            init_max,
        )

    disponible = _tabla(
        "Available (recursos disponibles)",
        f"disponible_{sufijo}",
        ["Available"],
        recursos,
        n,
        m,
        init_avail,
    )[0]

    proceso_solicitud = None
    solicitud = None

    if activar_solicitud:
        st.divider()
        indice_defecto = 1 if (usar_ejemplo and n > 1) else 0
        proceso_seleccionado = st.selectbox(
            "Proceso que realiza la solicitud",
            options=procesos,
            index=indice_defecto,
        )
        proceso_solicitud = procesos.index(proceso_seleccionado)
        solicitud = _tabla(
            f"Request (solicitud de {proceso_seleccionado})",
            f"request_{sufijo}_{proceso_solicitud}",
            [proceso_seleccionado],
            recursos,
            n,
            m,
            init_req,
        )[0]

    return {
        "procesos": procesos,
        "recursos": recursos,
        "asignacion": asignacion,
        "maximo": maximo,
        "disponible": disponible,
        "activar_solicitud": activar_solicitud,
        "proceso_solicitud": proceso_solicitud,
        "solicitud": solicitud,
    }