import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st
from define_planta import define_parameters, define_plant, design_pid_controller, define_open_loop_system

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

def root_locus():
    m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
    j = (2/5)*m*r*r  # Momento de inercia

    # Fórmula para el numerador
    numerador = (m * g * d) / (l * ((j / (r * r)) + m))

    plant_tf = define_plant([numerador], [1, 0, 0])
    pid_tf = design_pid_controller(Kp, Ki, Kd)

    # Open loop function
    open_loop_tf = define_open_loop_system(plant_tf, pid_tf)

    def plot_root_locus(sys_tf, k):
        # Crear el gráfico del root locus con la cuadrícula activada
        plt.figure(figsize=(9, 7))
        cplt = ct.root_locus_plot(sys_tf, grid=True, initial_gain= pid_tf)

        # Configurar el título y etiquetas
        plt.title('Lugar de las Raíces del Sistema')
        plt.xlabel('Parte Real')
        plt.ylabel('Parte Imaginaria')

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)  # Cambié plt.show() por st.pyplot()

    plot_root_locus(open_loop_tf, pid_tf)

# Llamada a la función root_locus
root_locus()

if __name__ == "__main__":
    # No es necesario agregar main() aquí si no hay otras funcionalidades principales
    pass
