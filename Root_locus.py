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
        
        # Extraer los coeficientes numéricos del PID
        numerador_pid = pid_tf.num[0]  # Numerador de PID
        denominador_pid = pid_tf.den[0]  # Denominador de PID
        
        # Open loop function
        open_loop_tf = define_open_loop_system(plant_tf_sym, pid_tf)
        
        # Usar el PID como un valor para k (ganancia inicial)
        k = pid_tf

        def plot_root_locus(sys_tf, k):
            # Crear el gráfico del root locus con la cuadrícula activada
            plt.figure(figsize=(9, 7))
            cplt = ct.root_locus_plot(sys_tf, grid=True, initial_gain=k)

            # Configurar el título y etiquetas
            plt.title('Lugar de las Raíces del Sistema')
            plt.xlabel('Parte Real')
            plt.ylabel('Parte Imaginaria')

            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)

        plot_root_locus(open_loop_tf, k)
    
    root_locus()
        
if __name__ == "__main__":
    main()
