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

    # Llamada a la función root_locus con los parámetros de tamaño y resolución
    root_locus(figure_width, figure_height, dpi)

if __name__ == "__main__":
    main()
