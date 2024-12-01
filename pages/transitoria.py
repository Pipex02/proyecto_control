import streamlit as st
import numpy as np
import control as ct
import os

# Importar las funciones definidas
from define_planta import define_parameters  # Asegúrate de que esta función esté definida en 'define_planta'

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    .block-container {
        max-width: 72%;
        margin: auto;
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("Análisis de Respuesta Transitoria")

# Título de la página
st.subheader("Respuesta al Escalón del Sistema")

st.image(os.path.join(os.getcwd(), "static", "transitoria.png"), caption="Step response", width=390)


# Menú desplegable en la barra lateral
menu = st.sidebar.selectbox("Selecciona una opción", ["Planta del sistema"])

# Si se selecciona "Planta del sistema"
if menu == "Planta del sistema":
    # Seleccionar el tipo de planta
    planta_seleccionada = st.selectbox("Selecciona el tipo de planta", ["Planta real", "Planta variable"])

    # Función principal
    def main():
        # Si se selecciona "Planta real"
        if planta_seleccionada == "Planta real":
            # Parámetros para la Planta real
            m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()

        # Si se selecciona "Planta variable"
        if planta_seleccionada == "Planta variable":
            # Modificar parámetros del sistema
            with st.expander("Modificar parámetros del sistema", expanded=False):
                col1, col2, col3 = st.columns(3)

                with col1:
                    m = st.number_input("Masa de la bola [kg]", value=1.0, min_value=0.1)
                    r = st.number_input("Radio de la bola [m]", value=0.1, min_value=0.01)
                    d = st.number_input("Desplazamiento [m]", value=1.0, min_value=0.1)

                with col2:
                    g = st.number_input("Gravedad [m/s²]", value=9.81, min_value=0.1)
                    l = st.number_input("Longitud [m]", value=1.0, min_value=0.1)
                    Kp = st.number_input("Proporcional (Kp)", value=1.0, min_value=0.1)

                with col3:
                    Ki = st.number_input("Integral (Ki)", value=1.0, min_value=0.1)
                    Kd = st.number_input("Derivativo (Kd)", value=1.0, min_value=0.1)

        # Aquí comienza el cálculo de la respuesta transitoria al escalón
        # Define el factor de escalamiento del escalón
        x = st.number_input("Factor de escalamiento del escalón", value=10.0)

        # Definir la función de transferencia del sistema cerrado (esto debe estar definido previamente)
        # Nota: Debes tener la transferencia cerrada 'closed_loop_tf' para este cálculo
        closed_loop_tf = ct.TransferFunction([Kp], [m, r, d, g, l])  # Aquí debes reemplazar por tu transferencia

        # 2. Simular la respuesta al escalón con escalamiento y valor inicial de 20
        t = np.linspace(0, 10, 500)
        t_step, y_closed_loop = ct.step_response(closed_loop_tf, T=t)

        # Escalar la respuesta y el escalón
        y_closed_loop = x * y_closed_loop + 20  # Escalar y ajustar el valor inicial a 20

        # 3. Calcular los parámetros transitorios
        info = ct.step_info(closed_loop_tf)

        tr = info['RiseTime']        # Tiempo de subida
        ts = info['SettlingTime']    # Tiempo de asentamiento
        mp = info['Overshoot']       # Sobresalto (overshoot)
        tp = info['PeakTime']        # Tiempo pico
        pk = info['Peak']            # Valor pico
        yss = y_closed_loop[-1]      # Valor en estado estacionario
        ess = x - (yss - 20)         # Error en estado estacionario considerando el desplazamiento

        # Mostrar los parámetros transitorios en Streamlit
        st.subheader("Parámetros de la Respuesta Transitoria")
        st.write(f"Tiempo de subida (tr): {tr} segundos")
        st.write(f"Tiempo de asentamiento (ts): {ts} segundos")
        st.write(f"Sobresalto (mp): {mp}%")
        st.write(f"Tiempo pico (tp): {tp} segundos")
        st.write(f"Valor pico (pk): {pk}")
        st.write(f"Valor en estado estacionario (yss): {yss}")
        st.write(f"Error en estado estacionario (ess): {ess}")

    # Ejecutar la función principal
    main()
