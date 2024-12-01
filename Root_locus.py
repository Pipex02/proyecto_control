import sympy as sp

# Asumiendo que 'design_pid_controller_symbolic' ya está definida:

def root_locus(m, r, d, g, l, j, Kp, Ki, Kd):
    
    numerador=calculate_plant_parameters(m, r, d, g, l)
    plant_num = [numerador]        # Numerador de la planta
    plant_den = [1, 0, 0]         # Denominador de la planta

    plant_tf_sym = define_plant_symbolic(plant_num, plant_den)
    pid_tf = design_pid_controller(Kp, Ki, Kd)

    # Evaluar pid_tf para obtener un valor real
    # Convertimos el PID simbólico a una expresión
    pid_tf_sym = design_pid_controller_symbolic(Kp, Ki, Kd)
    
    # Evaluamos la expresión simbólica en s=0 para obtener un valor real
    pid_tf_real_at_s0 = pid_tf_sym.subs('s', 0)
    
    # Convertimos la expresión evaluada a un valor numérico real
    k = float(pid_tf_real_at_s0)

    # Open loop function
    open_loop_tf = define_open_loop_system(plant_tf, pid_tf)

    def plot_root_locus(sys_tf, k):
        # Crear el gráfico del root locus con la cuadrícula activada
        plt.figure(figsize=(9, 7))
        cplt = ct.root_locus_plot(sys_tf, grid=True, initial_gain=k)

        # Configurar el título y etiquetas
        plt.title('Lugar de las Raíces del Sistema')
        plt.xlabel('Parte Real')
        plt.ylabel('Parte Imaginaria')

        # Mostrar el gráfico en Streamlit
        st.pyplot(plt)  # Cambié plt.show() por st.pyplot()

    plot_root_locus(open_loop_tf, k)

m, r, d, g, l, j, Kp, Ki, Kd = define_parameters()
root_locus(m, r, d, g, l, j, Kp, Ki, Kd)
