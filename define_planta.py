import sympy as sp
import control as ct
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

def define_parameters():
    m = 0.0464  # Masa de la bola en Kg
    r = 0.02    # Radio de la bola
    d = 0.04    # Desplazamiento del brazo
    g = 9.8     # Gravedad
    l = 0.37    # Longitud de la viga
    j = (2/5)*m*r*r  # Momento de inercia
    Kp = 26
    Ki = 13
    Kd = 30
    
    return m, r, d, g, l, j, Kp, Ki, Kd

# 1. Definir la planta simbólicamente
def define_plant_symbolic(num, den):
    s = sp.symbols('s')
    num_sym = sum([coef * s**i for i, coef in enumerate(num[::-1])])
    den_sym = sum([coef * s**(i*3) for i, coef in enumerate(den[::-1])])
    plant_tf_sym = num_sym / den_sym
    return plant_tf_sym

# 2. Definir la planta numérica
def define_plant_numeric(num, den):
    plant_tf_num = ct.TransferFunction(num, den)
    return plant_tf_num

# 3. Definir el controlador PID simbólicamente
def design_pid_controller_symbolic(kp, ki, kd):
    s = sp.symbols('s')
    num = kd * s**2 + kp * s + ki
    den = s
    if ki == 0:
        num = kd * s + kp
        den = 1
    if kd == 0:
        num = kp * s + ki
        den = s
    pid_tf_sym = num / den
    return pid_tf_sym

# 4. Definir el controlador PID numéricamente
def design_pid_controller_numeric(kp, ki, kd):
    pid_tf = ct.TransferFunction([kd, kp, ki], [1, 0])
    if ki == 0:
        pid_tf = ct.TransferFunction([kd, kp], [1])
    return pid_tf

# 5. Función para obtener la planta a partir de parámetros físicos
def calculate_plant_parameters(m, r, d, g, l):
    j = (2/5) * m * r * r  # Momento de inercia
    numerador = (m * g * d) / (l * ((j / (r * r)) + m))
    return round(numerador, 3)  # Redondear el numerador a 3 decimales

# 6. Función para definir la planta con parámetros físicos y PID
def define_system(m, r, d, g, l, Kp, Ki, Kd):
    # Calcula los parámetros físicos de la planta
    numerador = calculate_plant_parameters(m, r, d, g, l)

    # Definir la planta simbólica y numérica
    plant_num = [numerador]        # Numerador de la planta
    plant_den = [1, 0, 0]         # Denominador de la planta

    plant_tf_sym = define_plant_symbolic(plant_num, plant_den)
    plant_tf_num = define_plant_numeric(plant_num, plant_den)

    # Definir el controlador PID simbólico y numérico
    pid_tf_sym = design_pid_controller_symbolic(Kp, Ki, Kd)
    pid_tf_num = design_pid_controller_numeric(Kp, Ki, Kd)

    return plant_tf_sym, plant_tf_num, pid_tf_sym, pid_tf_num

# 6.2 Función para definir la planta con parámetros físicos y PID
def define_system2(m, r, d, g, l, Kp, Ki, Kd):
    # Calcula los parámetros físicos de la planta
    numerador = calculate_plant_parameters(m, r, d, g, l)

    # Definir la planta simbólica y numérica
    plant_num = [numerador]        # Numerador de la planta
    plant_den = [1, 0, 0]         # Denominador de la planta

    plant_tf_sym = define_plant_symbolic(plant_num, plant_den)
    plant_tf_num = define_plant_numeric(plant_num, plant_den)

    # Definir el controlador PID simbólico y numérico
    pid_tf_sym = design_pid_controller_symbolic(Kp, Ki, Kd)
    pid_tf_num = design_pid_controller_numeric(Kp, Ki, Kd)

    # Generate LaTeX strings for PID and plant transfer functions
    pid_latex = print_pid_tf_latex(Kp, Ki, Kd)
    plant_latex = print_plant_tf_latex(m, r, d, g, l)

    return plant_tf_sym, plant_tf_num, pid_tf_sym, pid_tf_num, pid_latex, plant_latex
#7. Imprimir funcion de transferencia del controlador
def print_pid_tf_latex(kp, ki, kd):
    if ki == 0:
        if kd == 0:
            return f"PID : G_1 = {kp}"
        else:
            return f"PID : G_1 = {kd}s + {kp}"
    else:
        if kd == 0:
            return f"PID : G_1 = \\frac{{{kp}s + {ki}}}{{s}}"
        else:
            return f"PID : G_1 = \\frac{{{kd}s^2 + {kp}s + {ki}}}{{s}}"

#8. Imprimir funcion de transferencia del controlador
def print_plant_tf_latex(m, r, d, g, l):
    numerador = calculate_plant_parameters(m, r, d, g, l)
    return f"Planta : G_2 = \\frac{{{numerador}}}{{s^2}}"

#9. Calcular los parametros de respuesta al impulso de amplitud x
def calculate_step_response_parameters(closed_loop_tf, x):
    # Define the time vector
    t = np.linspace(0, 40, 2000)

    # Calculate the step response
    t_step, y_closed_loop = ct.step_response(closed_loop_tf, T=t)
    y_closed_loop = x * y_closed_loop + 20

    # Calculate the step response parameters
    info = ct.step_info(y_closed_loop, t_step, SettlingTimeThreshold=0.02)
    tr = info['RiseTime']
    ts = info['SettlingTime']
    mp = info['Overshoot']
    tp = info['PeakTime']
    pk = info['Peak']
    yss = y_closed_loop[-1]
    ess = x - (yss - 20)

    return tr, ts, mp, tp, pk, yss, ess, t_step, y_closed_loop    

# === 1. Definir la planta simbólicamente ===
def translate_sym(m, r, d, g, l, Kp, Ki, Kd):
    m=m
    r=r
    d=d
    g=g
    l=l
    Kp=Kp
    Ki=Ki
    Kd=Kd
    return m,r,d,g,l,Kp,Ki,Kd

# 1. Definir el sistema de planta en términos de su función de transferencia
def define_plant(num, den):
    plant_tf = ct.TransferFunction(num, den)
    return plant_tf

# 2. Definir el controlador PID
def design_pid_controller(Kp, Ki, Kd):
    num = [Kd, Kp, Ki]
    den = [1, 0]
    if Ki == 0:
        num = [Kd, Kp]
        den = [1]
    if Kd == 0:
        num = [Kp, Ki]
        den = [1, 0]
    
    pid_tf = ct.TransferFunction(num, den)
    return pid_tf


# 3. Definir el sistema en lazo abierto
def define_open_loop_system(plant_tf, pid_tf):
    open_loop_tf = plant_tf * pid_tf
    return open_loop_tf

# 4. Definir el sistema en lazo cerrado
def define_closed_loop_system(open_loop_tf):
    closed_loop_tf = ct.feedback(open_loop_tf, 1)  # Retroalimentación unitaria
    return closed_loop_tf

# 5. Definir el impulso unitario (aproximación a la delta de Dirac) que comienza en t=2
def impulso_unitario_continuo(t):
    epsilon = 0.02  # Ancho del pulso
    return (np.where(np.abs(t - 2) < epsilon, 1 / epsilon, 0))/3

# 6. Definir el escalón unitario (Heaviside) en una función continua que comienza en t=2
def escalon_unitario_continuo(t):
    return 11 * np.where(t >= 2, 1, 0)  # Escalón de amplitud 5 que comienza en t=2

# 7. Respuesta al impulso en lazo abierto
def simulate_open_loop_impulse_response(open_loop_tf):
    t = np.linspace(0, 10, 500)  # Tiempo de simulación
    # Generar impulso unitario usando nuestra función personalizada
    impulse = impulso_unitario_continuo(t)
    t, y_open_loop = ct.forced_response(open_loop_tf, T=t, U=impulse)  # Respuesta del sistema
    return t, impulse, t, y_open_loop

# 8. Respuesta al impulso en lazo cerrado
def simulate_closed_loop_impulse_response(closed_loop_tf):
    t = np.linspace(0, 15, 500)  # Tiempo de simulación
    # Generar impulso unitario usando nuestra función personalizada
    impulse = impulso_unitario_continuo(t)
    t, y_closed_loop = ct.forced_response(closed_loop_tf, T=t, U=impulse)  # Respuesta del sistema
    return t, impulse, t, y_closed_loop

# 9. Respuesta al escalón en lazo abierto
def simulate_open_loop_step_response(open_loop_tf):
    t = np.linspace(0, 10, 500)  # Tiempo de simulación
    # Generar escalón unitario usando nuestra función personalizada
    step = escalon_unitario_continuo(t)
    t, y_open_loop = ct.forced_response(open_loop_tf, T=t, U=step)  # Respuesta del sistema
    return t, step, t, y_open_loop

# 10. Respuesta al escalón en lazo cerrado
def simulate_closed_loop_step_response(closed_loop_tf):
    t = np.linspace(0, 15, 500)  # Tiempo de simulación
    # Generar escalón unitario usando nuestra función personalizada
    step = escalon_unitario_continuo(t)
    t, y_closed_loop = ct.forced_response(closed_loop_tf, T=t, U=step)  # Respuesta del sistema
    return t, step, t, y_closed_loop


# === 4. Graficar respuestas al impulso y al escalón en una sola página (2x2) ===
def plot_responses(t_impulse_open, impulse_open, t_open, y_open_loop, t_impulse_closed, impulse_closed, t_closed, y_closed_loop,
                   t_step_open, step_open, t_open_step, y_open_step, t_step_closed, step_closed, t_closed_step, y_closed_step):
    plt.figure(figsize=(12, 10))  # Tamaño de la figura

    # Respuesta al impulso (Lazo Abierto)
    plt.subplot(2, 2, 1)  # 2 filas, 2 columnas, primer gráfico
    plt.plot(t_impulse_open, impulse_open, 'r--', label="Impulso unitario")
    plt.plot(t_open, y_open_loop, 'b-', label="Respuesta al impulso (Lazo Abierto)")
    plt.title("Respuesta al Impulso (Lazo Abierto)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (cm)")
    plt.legend()
    plt.grid(True)
    plt.ylim(-20, 20)  # Limitar el eje y de -20 a 20
    plt.xlim(0, 6)  # Limitar el eje y de -20 a 20

    # Respuesta al impulso (Lazo Cerrado)
    plt.subplot(2, 2, 2)  # 2 filas, 2 columnas, segundo gráfico
    plt.plot(t_impulse_closed, impulse_closed, 'r--', label="Impulso unitario")
    plt.plot(t_closed, y_closed_loop, 'b-', label="Respuesta al impulso (Lazo Cerrado)")
    plt.title("Respuesta al Impulso (Lazo Cerrado)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (cm)")
    plt.legend()
    plt.grid(True)
    plt.ylim(-20, 20)  # Limitar el eje y de -20 a 20
    plt.xlim(0, 6)  # Limitar el eje y de -20 a 20

    # Respuesta al escalón (Lazo Abierto)
    plt.subplot(2, 2, 3)  # 2 filas, 2 columnas, tercer gráfico
    plt.plot(t_step_open, step_open, 'r--', label="Escalón unitario")
    plt.plot(t_open_step, y_open_step, 'b-', label="Respuesta al escalón (Lazo Abierto)")
    plt.title("Respuesta al Escalón (Lazo Abierto)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (cm)")
    plt.legend()
    plt.grid(True)
    plt.ylim(-20, 20)  # Limitar el eje y de -20 a 20
    plt.xlim(0, 6)  # Limitar el eje y de -20 a 20

    # Respuesta al escalón (Lazo Cerrado)
    plt.subplot(2, 2, 4)  # 2 filas, 2 columnas, cuarto gráfico
    plt.plot(t_step_closed, step_closed, 'r--', label="Escalón unitario")
    plt.plot(t_closed_step, y_closed_step, 'b-', label="Respuesta al escalón (Lazo Cerrado)")
    plt.title("Respuesta al Escalón (Lazo Cerrado)")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Amplitud (cm)")
    plt.legend()
    plt.grid(True)
    plt.ylim(-20, 20)  # Limitar el eje y de -20 a 20
    plt.xlim(0, 6)  # Limitar el eje y de -20 a 20

    # Ajustar el espacio entre los subgráficos
    plt.tight_layout()  # Ajusta automáticamente los subgráficos para evitar superposición

    # Añadir una pequeña separación adicional para evitar el solapamiento de etiquetas
    plt.subplots_adjust(hspace=0.4, wspace=0.3)

    # Mostrar los gráficos
    st.pyplot(plt)

def graficas(m, r, d, g, l, Kp, Ki, Kd):
    masa,radio,desplazamiento,gravity,long,kp,ki,kd = translate_sym(m, r, d, g, l, Kp, Ki, Kd)

    j = (2/5)*masa*radio*radio  # Momento de inercia

    # Fórmula para el numerador
    numerador = (masa * gravity * desplazamiento) / (l * ((j / (radio * radio)) + masa))

    # Definir el sistema de planta
    plant_tf = define_plant([numerador], [1, 0, 0])

    # Definir controlador PID
    pid_tf = design_pid_controller(kp, ki, kd)

    # === 2. Definir sistema en lazo abierto y cerrado ===
    open_loop_tf = define_open_loop_system(plant_tf, pid_tf)
    closed_loop_tf = define_closed_loop_system(open_loop_tf)

    # === 3. Simulaciones ===
    # 3.1. Respuesta al impulso en lazo abierto
    t_impulse_open, impulse_open, t_open, y_open_loop = simulate_open_loop_impulse_response(open_loop_tf)
    # 3.2. Respuesta al impulso en lazo cerrado
    t_impulse_closed, impulse_closed, t_closed, y_closed_loop = simulate_closed_loop_impulse_response(closed_loop_tf)

    # 3.3. Respuesta al escalón en lazo abierto
    t_step_open, step_open, t_open_step, y_open_step = simulate_open_loop_step_response(open_loop_tf)
    # 3.4. Respuesta al escalón en lazo cerrado
    t_step_closed, step_closed, t_closed_step, y_closed_step = simulate_closed_loop_step_response(closed_loop_tf)
    plot_responses(t_impulse_open, impulse_open, t_open, y_open_loop, t_impulse_closed, impulse_closed, t_closed, y_closed_loop,
                   t_step_open, step_open, t_open_step, y_open_step, t_step_closed, step_closed, t_closed_step, y_closed_step)
    
def ecuaciones(m, r, d, g, l, Kp, Ki, Kd):
    # Llamar a la función para obtener el sistema completo
    plant_tf_sym, plant_tf_num, pid_tf_sym, pid_tf_num = define_system(m, r, d, g, l, Kp, Ki, Kd)

    # Traducir parámetros para obtener el sistema completo

    # Calcular la función de transferencia de trayectoria directa (lazo abierto)
    direct_trajectory_tf_sym = plant_tf_sym * pid_tf_sym

    # Calcular la función de transferencia de lazo cerrado
    closed_loop_tf_sym = direct_trajectory_tf_sym / (1 + direct_trajectory_tf_sym)

    # Crear las columnas adicionales para las nuevas funciones de transferencia

    # Crear columnas para las funciones de transferencia
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("FDT planta:")
        st.latex(f'\\text{{Planta: }} {sp.latex(plant_tf_sym)}')

    with col2:
        st.subheader("FDT controlador PID:")
        st.latex(f'\\text{{PID: }} {sp.latex(pid_tf_sym)}')

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("FDT trayectoria directa:")
        st.latex(f'\\text{{Lazo abierto: }} {sp.latex(direct_trajectory_tf_sym)}')

    with col4:
        st.subheader("FDT lazo cerrado:")
        st.latex(f'\\text{{Lazo cerrado: }} {sp.latex(closed_loop_tf_sym)}')
