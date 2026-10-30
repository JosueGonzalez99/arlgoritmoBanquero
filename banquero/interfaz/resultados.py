import pandas as pd
import streamlit as st


def _formato_vector(vector, recursos):
    return ", ".join(f"{recursos[j]}={vector[j]}" for j in range(len(vector)))


def mostrar_necesidad(necesidad, procesos, recursos, titulo="Matriz Need (Max - Allocation)"):
    st.subheader(titulo)
    tabla = pd.DataFrame(necesidad, index=procesos, columns=recursos)
    st.dataframe(tabla, use_container_width=True)


def mostrar_resultado(es_seguro, secuencia, procesos):
    st.subheader("Resultado de Seguridad")

    if es_seguro:
        nombres = [procesos[i] for i in secuencia]
        st.success("El sistema se encuentra en estado SEGURO.")
        st.markdown("**Secuencia segura:** " + " → ".join(nombres))
    else:
        st.error("El sistema se encuentra en estado INSEGURO (posible interbloqueo).")
        pendientes = [procesos[i] for i in range(len(procesos)) if i not in secuencia]
        st.markdown("**Procesos que no pudieron terminar:** " + ", ".join(pendientes))
        if secuencia:
            nombres = [procesos[i] for i in secuencia]
            st.markdown("**Procesos que sí terminaron:** " + " → ".join(nombres))


def mostrar_pasos(pasos, procesos, recursos):
    st.subheader("Detalle paso a paso")

    if not pasos:
        st.info("Ningún proceso pudo terminar con los recursos disponibles.")
        return

    filas = []
    for numero, paso in enumerate(pasos, start=1):
        filas.append({
            "Paso": numero,
            "Proceso": procesos[paso["proceso"]],
            "Need": _formato_vector(paso["necesidad"], recursos),
            "Work antes": _formato_vector(paso["work_antes"], recursos),
            "Work después": _formato_vector(paso["work_despues"], recursos),
        })
    st.dataframe(pd.DataFrame(filas), hide_index=True, use_container_width=True)

    for numero, paso in enumerate(pasos, start=1):
        nombre = procesos[paso["proceso"]]
        st.write(
            f"Paso {numero}: {nombre} puede terminar porque su Need "
            f"({_formato_vector(paso['necesidad'], recursos)}) es menor o igual a Work "
            f"({_formato_vector(paso['work_antes'], recursos)}). Al terminar devuelve sus "
            f"recursos y Work queda en ({_formato_vector(paso['work_despues'], recursos)})."
        )


def mostrar_evaluacion_solicitud(resultado_req, proceso_idx, solicitud, procesos, recursos):
    st.divider()
    nombre_proc = procesos[proceso_idx]
    st.subheader(f"Evaluación de Solicitud para {nombre_proc}: ({_formato_vector(solicitud, recursos)})")

    motivo = resultado_req["motivo"]

    if motivo == "supera_necesidad":
        recurso = recursos[resultado_req["recurso"]]
        st.error(
            f"Solicitud RECHAZADA: {nombre_proc} solicitó {resultado_req['valor_solicitado']} "
            f"del recurso {recurso}, pero su Need máxima declarada es {resultado_req['valor_limite']}."
        )
        return

    if motivo == "supera_disponible":
        recurso = recursos[resultado_req["recurso"]]
        st.warning(
            f"Solicitud EN ESPERA: {nombre_proc} solicitó {resultado_req['valor_solicitado']} "
            f"del recurso {recurso}, pero actualmente solo hay {resultado_req['valor_limite']} disponible(s)."
        )
        return

    if resultado_req["otorgado"]:
        st.success(f"Solicitud APROBADA: Se pueden entregar los recursos a {nombre_proc} de forma segura.")
    else:
        st.error(
            f"Solicitud DENEGADA: Aunque hay recursos disponibles, entregárselos a {nombre_proc} "
            f"dejaría al sistema en un estado INSEGURO."
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Nuevo Allocation simulado**")
        st.dataframe(
            pd.DataFrame(resultado_req["asignacion"], index=procesos, columns=recursos),
            use_container_width=True,
        )
    with col2:
        st.markdown("**Nuevo Need simulado**")
        st.dataframe(
            pd.DataFrame(resultado_req["necesidad"], index=procesos, columns=recursos),
            use_container_width=True,
        )
    with col3:
        st.markdown("**Nuevo Available simulado**")
        st.dataframe(
            pd.DataFrame([resultado_req["disponible"]], index=["Available"], columns=recursos),
            use_container_width=True,
        )

    mostrar_resultado(resultado_req["es_seguro"], resultado_req["secuencia"], procesos)
    mostrar_pasos(resultado_req["pasos"], procesos, recursos)