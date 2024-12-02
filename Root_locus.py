import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from Root_base import root_locus  # Asegúrate de tener la función root_locus definida en el archivo 'Root_base.py'

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    /* Ajuste del ancho máximo de la página */
    .block-container {
        max-width: 72%;  /* Ajuste el ancho máximo del contenedor al 100% para mayor espacio */
        margin: auto;
        padding-top: none;
        margin-top: 0px !important;
    }

    /* Estilo del título de la página */
    h1 {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    body {
        font-family: 'Arial', sans-serif;
        font-size: 16px;
        margin: 0;
        padding: 0;
    }

    /* Estilo de la figura (gráfico) */
    .matplotlib {
        padding: none;
        margin-top: 0px !important;
        width: 100%;  /* Asegura que la figura ocupe todo el ancho disponible */
        height: auto;  /* Mantiene la proporción del gráfico */
        display: block;  /* Hace que el gráfico sea un bloque */
        margin-left: auto;  /* Centra el gráfico en el contenedor */
        margin-right: auto;  /* Centra el gráfico en el contenedor */
    }

    </style>
    """, unsafe_allow_html=True)

# Título de la página usando Streamlit (en lugar de HTML)
st.title("Análisis del Lugar de las Raíces del Sistema de Control")

def main():
    # Caja desplegable con los controles deslizantes
    with st.expander("Configurar gráfico", expanded=False):  # Se puede poner expanded=True para que esté expandido por defecto
        # Configuración de la figura
        figure_width = st.slider("Ancho del gráfico (en pulgadas)", min_value=8, max_value=10, value=10)  # Aumentar el tamaño de la figura
        figure_height = st.slider("Alto del gráfico (en pulgadas)", min_value=8, max_value=10, value=9)
        dpi = st.slider("Resolución del gráfico (DPI)", min_value=200, max_value=300, value=290)
    planta_seleccionada = st.selectbox("Selecciona el tipo de planta", ["Planta real", "Planta variable"])
    if planta_seleccionada == "Planta real":
        root_locus(figure_width, figure_height, dpi)
    if planta_seleccionada == "Planta variable":
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

        # Opción para mostrar u ocultar los parámetros
        mostrar_parametros = st.checkbox("Mostrar parámetros")

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
        
        non_root_locus(figure_width, figure_height, dpi, m, r, d, g, l, Kp, Ki, Kd)
        

    
if __name__ == "__main__":
    main()
