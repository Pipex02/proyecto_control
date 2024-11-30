import streamlit as st
import os  # Para cargar la imagen

# Configuración de la página principal
st.set_page_config(
    page_title="Proyecto Integrador de Control",
    page_icon="⚙️",
    layout="centered",
)
# CSS para ajustar el ancho del contenedor
st.markdown(
    """
    <style>
    .block-container {
        max-width: 72%;
        margin: auto;
        overflow: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenido de la página principal
st.title("Bienvenidos al Proyecto Integrador de Control")
st.subheader("Exploración de Sistemas de Control en Tiempo Real")

# Muestra una imagen desde la carpeta 'static'
st.image(os.path.join(os.getcwd(), "static", "sistema.png"), caption="Control Automático - Proyecto Integrador", use_container_width=True)

st.write(
    """
    Este proyecto integrador está diseñado para demostrar aplicaciones de sistemas 
    de control utilizando hardware y software en tiempo real. Puedes explorar las 
    diferentes páginas para visualizar gráficas de respuestas en tiempo real y 
    comportamiento transitorio.
    """
)

st.write("Utiliza el menú lateral para navegar entre las diferentes secciones del proyecto.")