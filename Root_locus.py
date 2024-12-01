import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from define_planta import define_parameters, define_plant, design_pid_controller, define_open_loop_system, calculate_plant_parameters, define_closed_loop_system

# === Establecer el estilo de la página ===
st.markdown(
    """
    <style>
    /* Establecer el ancho máximo de la página al 72% del ancho total */
    .block-container {
        max-width: 72%;
        margin: auto;
        overflow: auto;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    
    def root_locus():
        # Definir parámetros y calcular la planta
        m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
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
        
        def plot_closed_loop_poles_zeros(sys_tf):
            # Crear el sistema en lazo cerrado con retroalimentación unitaria
            sys_cl = ct.feedback(sys_tf, 1)
            
            # Crear el gráfico del lugar de las raíces utilizando ct.pole_zero_plot
            plt.figure(figsize=(9, 7))
            ct.pole_zero_plot(sys_cl, grid=True)
            
            # Configurar el título y etiquetas
            plt.title('Lugar de las Raíces del Sistema')
            plt.xlabel('Parte Real')
            plt.ylabel('Parte Imaginaria')

            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)
        
        # Mostrar la gráfica y los polos en lazo cerrado
        plot_closed_loop_poles_zeros(open_loop_tf)
        ct.damp(closed_loop_tf, doprint=True)

    # Llamada a la función principal
    root_locus()

if __name__ == "__main__":
    main()
