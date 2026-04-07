import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(
    page_title="San Marino Logística - Bienvenido", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. SISTEMA DE MEMORIA
if 'logeado' not in st.session_state:
    st.session_state['logeado'] = False
    st.session_state['rol'] = None

# --- CSS AVANZADO ---
st.markdown("""
<style>
/* 1. Fondo de Pantalla Original (Granja/Logística) */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1587293852726-59cd15a774bd?q=80&w=2000&auto=format&fit=crop"); 
    background-size: cover;
    background-position: center;
}

/* 2. Estilo para el contenedor general */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {
    background-color: transparent !important;
}

/* 3. Panel Izquierdo (Oscuro, Texto) */
[data-testid="stColumn"]:nth-child(1) {
    background-color: rgba(0, 0, 0, 0.75); 
    padding: 100px 50px !important;
    color: white !important;
    border-radius: 15px 0px 0px 15px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 80vh;
}

[data-testid="stColumn"]:nth-child(1) h1,
[data-testid="stColumn"]:nth-child(1) p {
    color: white !important;
}

/* 4. Panel Derecho (Ligero, Formulario) */
[data-testid="stColumn"]:nth-child(2) {
    background-color: rgba(255, 255, 255, 0.95); 
    padding: 60px 50px !important;
    border-radius: 0px 15px 15px 0px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 10px 0px 20px rgba(0, 0, 0, 0.5); 
    min-height: 80vh;
}

[data-testid="stColumn"]:nth-child(2) h2 {
    color: #333 !important;
    text-align: center;
}

[data-testid="stColumn"]:nth-child(2) label {
    color: #555 !important;
}

.centered-logo {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    col1, col2 = st.columns([3, 2])
    
    # --- COLUMNA 1: PANEL IZQUIERDO ---
    with col1:
        st.markdown("<br><br><h1 style='font-size: 4rem;'>Welcome Back</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem;'>Bienvenido a San Marino motor logístico. Tenga precaución a los datos que va a ingresar.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='display: flex; gap: 15px; font-size: 1.5rem;'>
            🌐 ✉️ 🔒
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<br><br><br>", unsafe_allow_html=True)

    # --- COLUMNA 2: PANEL DERECHO (FORMULARIO) ---
    with col2:
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            st.image("logo.png", width=150)
        except:
            st.warning("⚠️ Falta subir 'logo.png' a GitHub.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Campos de texto simplificados
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón único
        if st.button("Iniciar Sesión", use_container_width=True):
            if usuario == "admin" and contrasena == "123":
                st.session_state['logeado'] = True
                st.session_state['rol'] = "admin"
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")
        
        st.markdown("<br><br><br>", unsafe_allow_html=True)

# --- PANTALLA INTERNA (ADMINISTRADOR) ---
else:
    st.sidebar.title("San Marino")
    try:
        st.sidebar.image("logo.png", use_container_width=True)
    except:
        pass
        
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['logeado'] = False
        st.session_state['rol'] = None
        st.rerun()

    if st.session_state['rol'] == "admin":
        st.title("🚀 Panel de Administración Logística")
        st.write("Bienvenido, Administrador.")
        st.success("¡Inicio de sesión exitoso!")
