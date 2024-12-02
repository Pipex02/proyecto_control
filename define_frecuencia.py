import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from define_planta import define_parameters, calculate_plant_parameters, define_plant, design_pid_controller, define_open_loop_system

# Establecer el estilo de Seaborn para los gráficos
sns.set(style="whitegrid")  # Fondo limpio con líneas de cuadrícula suaves

# Función principal para la respuesta de frecuencia en el sistema en lazo abierto
def Respuesta_frecuencia_abierto():
    # Recuperar parámetros desde una función definida en otro archivo (ajustar según corresponda)
    m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()

    # Calcular los parámetros de la planta
    numerador = calculate_plant_parameters(m, r, d, g, l)
    plant_num = [numerador]  # Numerador de la planta
    plant_den = [1, 0, 0]   # Denominador de la planta

    # Definir la planta
    plant_tf_sym = define_plant(plant_num, plant_den)

    # Diseñar el controlador PID
    pid_tf = design_pid_controller(Kp, Ki, Kd)

    # Definir sistema en lazo abierto
    open_loop_tf = define_open_loop_system(plant_tf_sym, pid_tf)

    # Llamar a la función para graficar el diagrama de Bode
    plot_bode_with_margins(open_loop_tf)

# Función para graficar el Diagrama de Bode con márgenes de ganancia y fase
def plot_bode_with_margins(sys_tf):
    # Calcular márgenes de ganancia y fase
    gm, pm, Wcg, Wcp = ct.margin(sys_tf)

    # Imprimir los márgenes y frecuencias de interés en el formato adecuado
    if gm is not None and gm > 0:
        print(f"Margen de ganancia: {20 * np.log10(gm):.2f} dB")
    else:
        print("Margen de ganancia: Infinito (estable)")
    print(f"Margen de fase: {pm:.2f} grados")
    print(f"Frecuencia de cruce de ganancia: {Wcg:.2f} rad/s" if Wcg and np.isfinite(Wcg) else "Frecuencia de cruce de ganancia: No definida")
    print(f"Frecuencia de cruce de fase: {Wcp:.2f} rad/s" if Wcp and np.isfinite(Wcp) else "Frecuencia de cruce de fase: No definida")

    # Obtener datos para la magnitud, fase y frecuencias
    mag, phase, omega = ct.bode(sys_tf, dB=True, Hz=False, deg=True, plot=False)

    # Crear una figura para magnitud y fase
    fig, axs = plt.subplots(2, 1, figsize=(10, 7))

    # Graficar la magnitud (en dB)
    axs[0].semilogx(omega, 20 * np.log10(mag), label="Magnitud (dB)")
    if Wcg is not None and np.isfinite(Wcg):
        axs[0].axvline(x=Wcg, color='r', linestyle='--', label=f"Frec. cruce ganancia: {Wcg:.2f} rad/s")
    axs[0].set_ylabel("Magnitud (dB)")
    axs[0].grid(True)
    axs[0].legend()

    # Graficar la fase (en grados)
    axs[1].semilogx(omega, phase * (180 / np.pi), label="Fase (°)")
    if Wcp is not None and np.isfinite(Wcp):
        axs[1].axvline(x=Wcp, color='b', linestyle='--', label=f"Frec. cruce fase: {Wcp:.2f} rad/s")
    axs[1].set_ylabel("Fase (°)")
    axs[1].set_xlabel("Frecuencia (rad/s)")
    axs[1].grid(True)
    axs[1].legend()

    # Configurar el título
    plt.suptitle('Diagrama de Bode del Sistema con Márgenes de Ganancia y Fase', fontsize=14)

    # Mostrar la gráfica en Streamlit
    st.pyplot(fig)