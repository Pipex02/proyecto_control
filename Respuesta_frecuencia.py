import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from define_frecuencia import Respuesta_frecuencia_abierto  # Asegúrate de tener la función root_locus definida en el archivo 'Root_base.py'
from non_define_frecuencia import Respuesta_non_frecuencia_abierto  # Asegúrate de tener la función root_locus definida en el archivo 'Root_base.py'
from Root_base_nondefine import non_root_locus  # Asegúrate de tener la función root_locus definida en el archivo 'Root_base.py'
from define_planta import define_parameters

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    /* Establecer el ancho máximo de la página al 72% del ancho total */
    .block-container {
        max-width: 72%;
        margin: auto;
        overflow: auto;  /* Permite desplazamiento vertical si el contenido excede el área */
        /* Reducir el margen superior para que haya menos espacio encima de la página */
    
    </style>
    """, unsafe_allow_html=True)

st.header("Respuestas en frecuencia del Sistema")
planta_seleccionada = st.selectbox("Selecciona el tipo de planta", ["Planta real", "Planta variable"])

def main():
        
    # Parámetros para la Planta real
    if planta_seleccionada == "Planta real":
        m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
        Respuesta_frecuencia_abierto()
        
    mostrar_parametros = st.checkbox("Mostrar parámetros")
    
    # Parámetros para la Planta variable
    if planta_seleccionada == "Planta variable":
        # Llamar a la función de modificación de parámetros
        with st.expander("Modificar parámetros del sistema", expanded=False):  # expanded=False para que esté cerrado
            # Subdividir los parámetros en 3 columnas
            col1, col2, col3 = st.columns(3)

            with col1:
                m = st.number_input("Masa de la bola (Kg)", value=0.0464)
                r = st.number_input("Radio de la bola (m)", value=0.02)
                d = st.number_input("Desplazamiento del brazo (m)", value=0.04)

            with col2:
                g = st.number_input("Gravedad (m/s^2)", value=9.8)
                l = st.number_input("Longitud de la viga (m)", value=0.37)

            with col3:
                Kp = st.number_input("Ganancia proporcional (Kp)", value=26)
                Ki = st.number_input("Ganancia integral (Ki)", value=13)
                Kd = st.number_input("Ganancia derivativa (Kd)", value=30)

        Respuesta_non_frecuencia_abierto(m, r, d, g, l, Kp, Ki, Kd)
    # Opción para mostrar u ocultar los parámetros
    

    # Si el checkbox está marcado, mostramos los parámetros en 3 columnas
    if mostrar_parametros:
        st.subheader("Parámetros ingresados:")
        
        # Crear tres columnas para los parámetros
        col1, col2, col3 = st.columns(3)

        with col1:
            st.write(f"Masa de la bola: {m} Kg")
            st.write(f"Radio de la bola: {r} m")
            st.write(f"Desplazamiento del brazo: {d} m")
        
        with col2:
            st.write(f"Gravedad: {g} m/s²")
            st.write(f"Longitud de la viga: {l} m")
            st.write(f"Ganancia proporcional (Kp): {Kp}")

        with col3:
            st.write(f"Ganancia integral (Ki): {Ki}")
            st.write(f"Ganancia derivativa (Kd): {Kd}") 
  
main()