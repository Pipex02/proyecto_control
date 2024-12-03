import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from define_planta import define_parameters, define_plant, design_pid_controller, define_open_loop_system, calculate_plant_parameters, define_closed_loop_system

# Establecer estilo de Seaborn para los gráficos
sns.set(style="whitegrid")

# Función para generar el diagrama de Nyquist
def plot_nyquist_diagram(sys_tf, figure_width, figure_height, dpi):
    # Crear el diagrama de Nyquist utilizando control.nyquist
    plt.figure(figsize=(figure_width, figure_height), dpi=dpi)
    sns.set_context("talk", font_scale=1.8)

    # El método ct.nyquist traza el diagrama de Nyquist directamente
    ct.nyquist(sys_tf, omega=np.logspace(-2, 2, 100), plot=True)

    # Configuración de la gráfica
    plt.title('Diagrama de Nyquist del Sistema', fontsize=20)
    plt.xlabel('Parte Real', fontsize=14)
    plt.ylabel('Parte Imaginaria', fontsize=14)
    
    # Cuadrícula para mejor visualización
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()

    # Mostrar la gráfica en Streamlit
    st.pyplot(plt)

# Función principal para generar y mostrar el gráfico de Nyquist
def nyquist_criterion_plot(figure_width, figure_height, dpi):
    # Definir la planta y el controlador (suponiendo que tienes las funciones de plant y PID definidas)
    m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
    numerador = calculate_plant_parameters(m, r, d, g, l)
    plant_num = [numerador]
    plant_den = [1, 0, 0]

    # Definir la planta
    plant_tf_sym = define_plant(plant_num, plant_den)

    # Diseñar el controlador PID
    pid_tf = design_pid_controller(Kp, Ki, Kd)

    # Definir el sistema en lazo abierto
    open_loop_tf = define_open_loop_system(plant_tf_sym, pid_tf)

    # Graficar el diagrama de Nyquist
    plot_nyquist_diagram(open_loop_tf, figure_width, figure_height, dpi)
