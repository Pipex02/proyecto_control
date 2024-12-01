import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from define_planta import graficas, ecuaciones, define_parameters
from non_define_planta import graficas, ecuaciones

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

st.header("Respuestas al Impulso y Escalón del Sistema")
        
# Agregar un menú desplegable en la barra lateral
menu = st.sidebar.selectbox("Selecciona una opción", ["Planta del sistema"])

if menu == "Planta del sistema":
    # Menú desplegable para seleccionar el tipo de planta
    planta_seleccionada = st.selectbox("Selecciona el tipo de planta", ["Planta real", "Planta variable"])

    # Cargar las funciones según la selección

    # === 5. Ejecutar en Streamlit ===
    def main():
        
        # Opción para seleccionar entre 'Gráficas' o 'Ecuaciones'
        seleccion = st.radio("Selecciona lo que deseas ver:", ("Gráficas", "Ecuaciones"))
        
        # Parámetros para la Planta real
        if planta_seleccionada == "Planta real":
            m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
        
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

        # Mostrar gráficas o ecuaciones según la selección
        if seleccion == "Gráficas":
            graficas(m, r, d, g, l, Kp, Ki, Kd)
        elif seleccion == "Ecuaciones":
            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            ecuaciones(m, r, d, g, l, Kp, Ki, Kd)

    # Ejecutar directamente la función main cuando se cargue la página
    main()
