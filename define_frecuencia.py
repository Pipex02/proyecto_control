import control as ct
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from define_planta import root_locus  # Asegúrate de tener la función root_locus definida en el archivo 'Root_base.py'

def Respuesta_frecuencia_abierto():
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