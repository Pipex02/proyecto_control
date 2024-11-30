import streamlit as st
import serial
import time

# Configura el puerto serial del Arduino
arduino_port = "COM4"  # Cambia esto según tu puerto (ej. "/dev/ttyUSB0" en Linux)
baud_rate = 9600
ser = serial.Serial(arduino_port, baud_rate, timeout=1)

# Inicializa el almacenamiento de datos
if "data" not in st.session_state:
    st.session_state["data"] = []

# Título de la aplicación Streamlit
st.title("Lectura en Tiempo Real")
st.write("Sensor de tensión")

# Contenedor para la gráfica
chart_placeholder = st.empty()

# Contenedor para mostrar el voltaje actual
voltage_placeholder = st.empty()

# Lectura de datos en tiempo real
while True:
    try:
        # Lee una línea del puerto serial
        line = ser.readline().decode("utf-8").strip()
        
        if line:
            try:
                # Convierte el valor leído a float (asumiendo que es un voltaje en formato decimal)
                voltage = float(line)
                # Redondear a 3 decimales de precisión
                voltage_rounded = round(voltage, 3)
                
                # Agregar el voltaje a la lista de datos
                st.session_state["data"].append(voltage_rounded)
                
                # Limita los datos almacenados a los últimos 100 valores
                st.session_state["data"] = st.session_state["data"][-100:]

                # Actualiza el valor de voltaje actual en la interfaz
                with voltage_placeholder.container():
                    st.write(f"**Voltaje Actual:** {voltage_rounded} V")

            except ValueError:
                # Si no se puede convertir la línea a un número, simplemente la ignoramos
                pass
        
        # Muestra la gráfica con los datos actualizados
        with chart_placeholder.container():
            st.line_chart(st.session_state["data"])

        # Pausa para no saturar la interfaz y permitir la actualización de datos
        time.sleep(0.1)

    except KeyboardInterrupt:
        break
    except Exception as e:
        st.error(f"Error: {e}")
        pass
