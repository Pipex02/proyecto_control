import streamlit as st


# iconos: https://fonts.google.com/icons
# Definir todas las páginas
p1 = st.Page("pages/main_page.py", title="Home", icon=":material/home:", default=True)
p2 = st.Page("pages/tiempo_real.py", title="Sistema real", icon=":material/monitoring:")
p3 = st.Page("pages/transitoria.py", title="Respuesta transitoria", icon=":material/planner_review:")
p4 = st.Page("Planta_code.py", title="Definición del sistema", icon=":material/settings:")
p5 = st.Page("Root_Locus.py", title="Lugar de las raíces del sistema", icon=":material/settings:")

# Definir navegacion
pg = st.navigation(
    {
        "": [p1],
        "Herramientas": [p4, p2, p3, p5],            
    }
)
pg.run()

st.logo("static/logo.png")


st.sidebar.markdown('''
    <style>
        .sidebar-text {
            font-size: 13px;
            font-family: monospace;
            font-weight: bold;
            padding-top: 10px;
        }
    </style>
    <div class="sidebar-text">
        Control Automático  | Nov 2024
    </div>
''', unsafe_allow_html=True)