import streamlit as st
import pandas as pd

# 1. Configuración de la página
st.set_page_config(page_title="San Marino Logística", layout="centered")

# 2. Diseño del fondo borroso
st.markdown("""
<style>
.stApp {
    background-image: url("https://images.unsplash.com/photo-1587293852726-59cd15a774bd?q=80&w=2000&auto=format&fit=crop");
    background-size: cover;
    background-position: center;
}
.stApp::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: inherit;
    filter: blur(8px);
    z-index: -1;
}
</style>
""", unsafe_allow_html=True)

# 3. Sistema de Memoria (Para no cerrar sesión por accidente)
if 'logeado' not in st.session_state:
    st.session_state['logeado'] = False
    st.session_state['rol'] = None

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    # Centramos el cuadro de login
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        # Intentamos cargar el logo de San Marino
        try:
            st.image("logo.png", use_container_width=True)
        except:
            st.warning("⚠️ Falta subir 'logo.png' a GitHub.")
            
        st.markdown("<h3 style='text-align: center; color: white; background-color: rgba(0,0,0,0.6); padding: 10px; border-radius: 10px;'>Acceso al Sistema</h3>", unsafe_allow_html=True)
        
        usuario = st.text_input("👤 Usuario")
        contrasena = st.text_input("🔒 Contraseña", type="password")
        
        if st.button("Iniciar Sesión", use_container_width=True):
            if usuario == "admin" and contrasena == "123":
                st.session_state['logeado'] = True
                st.session_state['rol'] = "admin"
                st.rerun()
            else:
                st.error("❌ Usuario o contraseña incorrectos")

# --- PANTALLA INTERNA (PANEL DE ADMINISTRACIÓN) ---
else:
    # Menú lateral
    st.sidebar.title("San Marino")
    try:
        st.sidebar.image("logo.png", use_container_width=True)
    except:
        pass
        
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state['logeado'] = False
        st.session_state['rol'] = None
        st.rerun()

    # Pantalla principal del Motor Logístico
    if st.session_state['rol'] == "admin":
        st.title("🚀 Panel de Administración Logística")
        st.success("¡Inicio de sesión exitoso!")
        st.write("Bienvenido al Motor de San Marino. Aquí pronto conectaremos tus archivos de Excel para la programación automática.")
