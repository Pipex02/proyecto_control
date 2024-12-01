import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from Root_base import root_locus 

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    /* Ajuste del ancho máximo de la página */
    .block-container {
        max-width: 90%;  /* Ajuste el ancho máximo del contenedor */
        margin: auto;
        padding-top: 20px;
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
        width: 90%;  /* Establecer un 90% de ancho para la figura */
        height: auto;  /* Mantiene la proporción del gráfico */
        display: block;  /* Hace que el gráfico sea un bloque */
        margin: 20px auto;  /* Centra el gráfico y agrega márgenes superior e inferior */
    }
    </style>
    """, unsafe_allow_html=True)

# Título de la página usando Streamlit (en lugar de HTML)
st.title("Análisis del Lugar de las Raíces del Sistema de Control")

def main():
    


    figure_width = st.slider("Ancho del gráfico (en pulgadas)", min_value=6, max_value=8, value=8)
    figure_height = st.slider("Alto del gráfico (en pulgadas)", min_value=6, max_value=8, value=6)
    dpi = st.slider("Resolución del gráfico (DPI)", min_value=200, max_value=300, value=290)
    
    # Llamada a la función principal
    root_locus(figure_width,figure_height,dpi)

if __name__ == "__main__":
    main()
