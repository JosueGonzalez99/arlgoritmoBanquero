import streamlit as st

from logica.banquero import calcular_necesidad, algoritmo_seguridad, evaluar_solicitud
from logica.validaciones import validar_datos
from interfaz.entrada import pedir_datos
from interfaz.resultados import (
    mostrar_necesidad,
    mostrar_resultado,
    mostrar_pasos,
    mostrar_evaluacion_solicitud,
)

st.set_page_config(page_title="Algoritmo del Banquero", layout="wide")

st.title("Simulador del Algoritmo del Banquero")
st.caption("Sistemas Operativos - Universidad Mariano Gálvez")

datos = pedir_datos()

if st.button("Ejecutar algoritmo", type="primary"):
    errores = validar_datos(
        datos["asignacion"],
        datos["maximo"],
        datos["disponible"],
        datos["solicitud"] if datos["activar_solicitud"] else None,
    )

    if errores:
        for error in errores:
            st.error(error)
    else:
        necesidad = calcular_necesidad(datos["maximo"], datos["asignacion"])
        mostrar_necesidad(necesidad, datos["procesos"], datos["recursos"])

        es_seguro, secuencia, pasos = algoritmo_seguridad(
            datos["disponible"], datos["asignacion"], necesidad
        )

        mostrar_resultado(es_seguro, secuencia, datos["procesos"])
        mostrar_pasos(pasos, datos["procesos"], datos["recursos"])

        if datos["activar_solicitud"]:
            resultado_req = evaluar_solicitud(
                datos["disponible"],
                datos["asignacion"],
                necesidad,
                datos["proceso_solicitud"],
                datos["solicitud"],
            )
            mostrar_evaluacion_solicitud(
                resultado_req,
                datos["proceso_solicitud"],
                datos["solicitud"],
                datos["procesos"],
                datos["recursos"],
            )