import streamlit as st
import numpy as np
import control as ct
import os
import plotly.graph_objects as go
import pandas as pd

# Importar las funciones definidas
from define_planta import define_parameters, define_system2, calculate_step_response_parameters

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    .block-container {
        max-width: 90%;
        margin: auto;
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)


st.title("Análisis de Respuesta Transitoria")

# Título de la página
st.subheader("Respuesta al Escalón del Sistema")

#st.image(os.path.join(os.getcwd(), "static", "transitoria.png"), caption="Step response", width=390)

col1, col2 = st.columns([2, 5])

with col1:
    # Seleccionar el tipo de planta
    planta_seleccionada = st.selectbox("Selecciona el tipo de planta", ["Planta real", "Planta variable"])

# Si se selecciona "Planta real"
if planta_seleccionada == "Planta real":
    # Parámetros para la Planta real
    m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()

# Si se selecciona "Planta variable"
if planta_seleccionada == "Planta variable":
    # Modificar parámetros del sistema
    col1, col2 = st.columns([5, 1])

    with col1:  
        with st.expander("Modificar parámetros del sistema", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                m = st.number_input("Masa de la bola [kg]", value=1.0, min_value=0.01, step=0.05)
                r = st.number_input("Radio de la bola [m]", value=0.1, min_value=0.01, step=0.05)
                
            with col2:
                g = st.number_input("Gravedad [m/s²]", value=9.81, min_value=0.1, step=0.05)
                l = st.number_input("Longitud [m]", value=1.0, min_value=0.1, step=0.01)
                
            with col3:
                d = st.number_input("Desplazamiento [m]", value=1.0, min_value=0.01, step=0.02)
                
col1, col2, col3, col4 = st.columns([5, 5, 5, 3])


col1, col2   = st.columns([2, 5], vertical_alignment="top")
with col1:
    col3, col4 = st.columns(2)
    with col3:    
        a_x = st.number_input("Amplitud del escalón", value=1.0, step=1.0)
        Kp = st.number_input("Proporcional (Kp)", value=10.0, step=1.0)
        Kd = st.number_input("Derivativo (Kd)", value=1.0, step=0.25)

    with col4:
        t = st.number_input("Tiempo", value=15.0, step=1.0)
        Ki = st.number_input("Integral (Ki)", value=1.0, step=1.0)
        
    # Aquí comienza el cálculo de la respuesta transitoria al escalón

    # Definir las funciones de transferencia del sistema
    plant_tf_sym, plant_tf_num, pid_tf_sym, pid_tf_num, pid_latex, plant_latex = define_system2(m, r, d, g, l, Kp, Ki, Kd)
    open_loop_tf = plant_tf_num * pid_tf_num
    closed_loop_tf = ct.feedback(open_loop_tf, 1)
    tr, ts, mp, tp, pk, yss, ess, t_step, y_closed_loop = calculate_step_response_parameters(closed_loop_tf, a_x)
    parameters = {
        'Tiempo de subida (tr)': tr,
        'Tiempo de asentamiento (ts)': ts,
        'Sobresalto (mp)': mp,
        'Tiempo pico (tp)': tp,
        'Valor pico (pk)': pk,
        'Valor en estado estacionario (yss)': yss,
        'Error en estado estacionario (ess)': ess
    }

    st.table(pd.DataFrame(list(parameters.items()), columns=['Parameter', 'Value']))

with col2:
    # Crear la gráfica de Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=t_step,
        y=y_closed_loop,
        mode='lines',
        name='Respuesta al escalón',
        line=dict(color='rgb(0, 254, 129)', width=3),
    ))

    # Configurar la apariencia de la gráfica
    fig.update_layout(
        title='Respuesta al escalón',
        xaxis_title='Tiempo (segundos)',
        yaxis_title='Amplitud',
        width=720,
        height=480,
        xaxis=dict(range=[0, t]),  # Establece el rango del eje X
        #yaxis=dict(range=[20, 40]),  # Establece el rango del eje Y
    
    )
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig) 

col1, col2 = st.columns(2)

with col1:
    st.latex(pid_latex)
with col2:
    st.latex(plant_latex)
     
col1, col2, col3 = st.columns([2, 4, 2])
with col2:
    # Create a dictionary to store the parameters
    st.markdown(
        """
        <style>
        table {
            width: 100%;
            border-collapse: collapse;
            border: 1px solid #333;
            background-color: #222;
            color: #fff;
            font-size: 12px;
        }

        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #333;
        }

        th {
            background-color: #333;
        }

        tr:nth-child(even) {
            background-color: #444;
        }

        tr:hover {
            background-color: #555;
        }

        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
    """
    <style>
        .stNumberInput > div > div > input {
            height: 20px; /* Adjust this value for the desired height */
            font-size: 6px; /* You can also adjust the font size */
        }
    </style>
    """, 
    unsafe_allow_html=True
)