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
            # Crear el sistema en lazo cerrado con retroalimentación unitaria
            sys_cl = ct.feedback(sys_tf, 1)
            
            # Crear el gráfico del lugar de las raíces (Root Locus)
            plt.figure(figsize=(9, 7))
            # Gráfico del lugar de las raíces
            ct.root_locus(sys_cl, grid=True)  # Elimino el argumento print_array=True
            
            # Configurar el título y etiquetas
            plt.title('Lugar de las Raíces del Sistema')
            plt.xlabel('Parte Real')
            plt.ylabel('Parte Imaginaria')
            
            # Graficar los polos y ceros
            poles = np.array(ct.pole(sys_cl))
            zeros = np.array(ct.zero(sys_cl))
            plt.scatter(np.real(poles), np.imag(poles), color='red', label='Polos', marker='x')
            plt.scatter(np.real(zeros), np.imag(zeros), color='blue', label='Ceros', marker='o')
            
            # Añadir leyenda
            plt.legend()
            
            # Mostrar el gráfico en Streamlit
            st.pyplot(plt)
        
        # Mostrar la gráfica y los polos en lazo cerrado
        plot_root_locus(open_loop_tf)
        
        # Mostrar información sobre los polos
        st.write("Análisis de los polos en el lazo cerrado:")
        ct.damp(closed_loop_tf, doprint=True)

    # Llamada a la función principal
    root_locus()

if __name__ == "__main__":
    main()
