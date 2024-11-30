import streamlit as st


# CSS para ajustar el ancho del contenedor
st.markdown(
    """
    <style>
    .block-container {
        max-width: 72%;
        overflow: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Análisis de Respuesta Transitoria")
st.write("Esta página está en desarrollo. Pronto podrás visualizar la respuesta transitoria del sistema.")

