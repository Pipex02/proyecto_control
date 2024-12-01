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

        def plot_root_locus(sys_tf):
            # Crear el sistema en lazo abierto
            sys_open_loop = ct.feedback(sys_tf, 1)

            # Crear el gráfico del lugar de las raíces usando root_locus de control
            plt.figure(figsize=(9, 7))
            # Generar el lugar de las raíces
            ct.root_locus(sys_open_loop, print_array=True, grid=True)

            # Configurar título y etiquetas
            plt.title('Lugar de las Raíces del Sistema')
            plt.xlabel('Parte Real')
            plt.ylabel('Parte Imaginaria')
            
            # Etiquetar los polos y ceros
            poles = sys_open_loop.pole()
            zeros = sys_open_loop.zero()
            for p in poles:
                plt.plot(np.real(p), np.imag(p), 'rx', label='Polos')  # Polos marcados con 'x'
            for z in zeros:
                plt.plot(np.real(z), np.imag(z), 'bo', label='Ceros')  # Ceros marcados con 'o'

            # Leyenda
            plt.legend()

            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)
        
        # Mostrar la gráfica y los polos en lazo cerrado
        plot_root_locus(open_loop_tf)

        # Mostrar información de los polos del sistema en lazo cerrado
        ct.damp(closed_loop_tf, doprint=True)

    # Llamada a la función principal
    root_locus()

if __name__ == "__main__":
    main()
