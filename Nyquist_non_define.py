import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from non_define_planta import define_plant, design_pid_controller, define_open_loop_system, calculate_plant_parameters, define_closed_loop_system

# Establecer estilo de Seaborn
sns.set(style="whitegrid")  # Aplicar un fondo limpio con líneas de cuadrícula suaves

def non_nyquist_criterion(figure_width, figure_height, dpi, m, r, d, g, l, Kp, Ki, Kd):
    # Definir parámetros y calcular la planta
    numerador = calculate_plant_parameters(m, r, d, g, l)
    plant_num = [numerador]        # Numerador de la planta
    plant_den = [1, 0, 0]         # Denominador de la planta

    # Definir la planta
    plant_tf_sym = define_plant(plant_num, plant_den)  

    # Diseñar el controlador PID
    pid_tf = design_pid_controller(Kp, Ki, Kd)
    
    # Definir sistema en lazo abierto
    open_loop_tf = define_open_loop_system(plant_tf_sym, pid_tf)
    
    # Definir sistema en lazo cerrado
    closed_loop_tf = define_closed_loop_system(open_loop_tf)

    # Función para graficar el diagrama de Nyquist
    def plot_nyquist_diagram(sys_tf, width, height, dpi):
        # Crear el gráfico del diagrama de Nyquist usando control.nyquist
        plt.figure(figsize=(width, height), dpi=dpi)  # Tamaño ajustado dinámicamente
        
        # Establecer un tema en Seaborn para el gráfico
        sns.set_context("talk", font_scale=1.8)  # Aumentar tamaño de fuentes y elementos visuales
        sns.set_context("poster", font_scale=1.4)

        # El método ct.nyquist traza el diagrama de Nyquist directamente
        ct.nyquist(sys_tf, omega=np.logspace(-2, 2, 100), plot=True)

        # Configurar título y etiquetas
        plt.title('Diagrama de Nyquist del Sistema', fontsize=35)
        plt.xlabel('Parte Real', fontsize=14)
        plt.ylabel('Parte Imaginaria', fontsize=14)
        
        # Cuadrícula para mejor visualización
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
        
        # Ajuste automático para que las etiquetas no se solapen
        plt.tight_layout()

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)
    
    # Contenedor para el gráfico
    with st.container():
        # Mostrar la gráfica de Nyquist
        plot_nyquist_diagram(open_loop_tf, figure_width, figure_height, dpi)

    # Mostrar información de los polos del sistema en lazo cerrado
    ct.damp(closed_loop_tf, doprint=True)
