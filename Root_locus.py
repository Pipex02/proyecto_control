import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from define_planta import define_parameters, define_plant, design_pid_controller, define_open_loop_system, calculate_plant_parameters

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

# Definir parámetros y calcular la planta
m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
numerador = calculate_plant_parameters(m, r, d, g, l)
plant_num = [numerador]        # Numerador de la planta
plant_den = [1, 0, 0]         # Denominador de la planta

# Definir la planta
plant_tf_sym = define_plant(plant_num, plant_den)  
# Diseñar el controlador PID
pid_tf = design_pid_controller(Kp, Ki, Kd)

# Extraer los coeficientes numéricos del PID
numerador_pid = pid_tf.num[0]  # Numerador de PID
denominador_pid = pid_tf.den[0]  # Denominador de PID

# Open loop function
open_loop_tf = define_open_loop_system(plant_tf_sym, pid_tf)

# Crear el gráfico del root locus utilizando ct.root_locus
plt.figure(figsize=(9, 7))
# Generar los puntos del root locus
ax = plt.subplots(figsize=(9, 7))
ct.root_locus(sys_tf, ax=ax, grid=True, initial_gain=pid_tf)

# Configurar el título y etiquetas
ax.set_title('Lugar de las Raíces del Sistema')
ax.set_xlabel('Parte Real')
ax.set_ylabel('Parte Imaginaria')

# Mostrar el gráfico en Streamlit
st.pyplot(plt)