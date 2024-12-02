import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from non_define_planta import define_plant, design_pid_controller, define_open_loop_system, calculate_plant_parameters, define_closed_loop_system

# Establecer estilo de Seaborn
sns.set(style="whitegrid")  # Aplicar un fondo limpio con líneas de cuadrícula suaves

def non_root_locus(figure_width, figure_height, dpi, m, r, d, g, l, Kp, Ki, Kd):
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

    # Función para graficar el lugar de las raíces
    def plot_root_locus(sys_tf, width, height, dpi):
        # Crear el sistema en lazo abierto
        sys_open_loop = ct.feedback(sys_tf, 1)

        # Crear el gráfico del lugar de las raíces usando root_locus de control
        plt.figure(figsize=(width, height), dpi=dpi)  # Tamaño ajustado dinámicamente
        
        # Establecer un tema en Seaborn para el gráfico
        sns.set_context("talk", font_scale=1.8)  # Aumentar tamaño de fuentes y elementos visuales
        sns.set_context("poster", font_scale=1.4)

        ct.root_locus(sys_open_loop, grid=True)

        # Configurar título y etiquetas
        plt.title('Lugar de las Raíces del Sistema', fontsize=35)
        plt.xlabel('Parte Real', fontsize=14)
        plt.ylabel('Parte Imaginaria', fontsize=14)
        
        # Etiquetar los polos y ceros
        poles = ct.poles(sys_open_loop)  # Cambiado a ct.poles()
        zeros = ct.zeros(sys_open_loop)  # Cambiado a ct.zeros()
        
            # Calcular el valor más pequeño en la parte real de los polos
        real_poles = np.real(poles)
        min_real_pole = np.min(real_poles)  # Polo más pequeño en la parte real
        max_real_pole = np.max(real_poles)
        
        real_zeros =np.real(zeros)
        min_real_zero = np.min(real_zeros)
        max_real_zero = np.max(real_zeros)
        
        # Ajustar límites de los ejes
        plt.xlim(min_real_pole - 7, max_real_pole + 7)  # Ajustar el rango del eje x según el polo más pequeño y un valor fijo
        plt.ylim(min_real_zero - 7, max_real_zero + 7)  # Ajustar el rango de la parte imaginaria (puedes modificar este valor también)

        for p in poles:
            plt.plot(np.real(p), np.imag(p), 'rx', label='Polos', markersize=17, markeredgewidth=5)  # Aumentar el tamaño de los marcadores y grosor
        for z in zeros:
            plt.plot(np.real(z), np.imag(z), 'bo', label='Ceros', markersize=5, markeredgewidth=5)  # Aumentar el tamaño de los marcadores y grosor

        # Leyenda con fuente más grande
        plt.legend(fontsize=14)
        plt.tight_layout()  # Ajusta automáticamente los subgráficos para evitar superposición

        # Añadir una pequeña separación adicional para evitar el solapamiento de etiquetas
        plt.subplots_adjust(hspace=0.4, wspace=0.3)

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)
    
    # Contenedor para el gráfico
    with st.container():
        # Mostrar la gráfica y los polos en lazo cerrado
        plot_root_locus(open_loop_tf, figure_width, figure_height, dpi)

    # Mostrar información de los polos del sistema en lazo cerrado
    ct.damp(closed_loop_tf, doprint=True)
