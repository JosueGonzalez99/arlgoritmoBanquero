import streamlit as st
from interfaz.entrada import pedir_datos

datos = pedir_datos()
st.write(datos)