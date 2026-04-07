import streamlit as st
import base64
import os

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

# --- FUNCIÓN DE IMAGEN DE FONDO ---
# Esto lee tu archivo local y lo inyecta en el diseño (evita fallos de carga en la nube)
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# Cargamos tu nueva imagen de fondo
bg_base64 = get_base64_of_bin_file("imagen fondo 1.avif")

# --- CSS AVANZADO: EFECTO VIDRIO Y CENTRADO ---
st.markdown(f"""
<style>
/* 1. Fondo de Pantalla Completo */
.stApp {{
    background-image: url("data:image/avif;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Quitar fondos por defecto de Streamlit */
.stApp > header {{
    background-color: transparent !important;
}}

/* 2. Estructura para Centrar Todo */
.block-container {{
    padding-top: 5vh !important; 
    max-width: 1200px !important;
}}

[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {{
    background-color: transparent !important;
    align-items: center; 
    justify-content: center;
    margin-top: 8vh; /* Empuja el panel hacia el centro vertical de la pantalla */
}}

/* 3. Panel Central (Efecto Vidrio Esmerilado) */
[data-testid="stColumn"]:nth-child(2) {{
    background: rgba(255, 255, 255, 0.35); /* Blanco semi-transparente */
    backdrop-filter: blur(12px); /* Efecto de desenfoque del fondo */
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.4); /* Borde sutil brillante */
    padding: 50px 40px !important; 
    border-radius: 25px !important; /* Bordes redondeados como en tu imagen */
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3); /* Sombra suave */
}}

/* 4. Estilo de los Textos */
[data-testid="stColumn"]:nth-child(2) h2 {{
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 400; /* Letra elegante y sin negrita gruesa */
    font-size: 2.2rem;
    margin-bottom: 25px;
}}

.stTextInput label p {{
    color: #2c2c2c !important;
    font-weight: 600 !important;
}}

/* Cajas de texto estilizadas */
.stTextInput input {{
    background-color: rgba(255, 255, 255, 0.65) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
    color: #333 !important;
}}

/* 5. Personalización del Botón (Estilo Píldora Roja) */
div.stButton > button {{
    background-color: #C01B1B !important; /* Rojo San Marino */
    color: white !important;
    border: none !important;
    border-radius: 30px !important; /* Forma redondeada completa */
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.2rem !important;
    transition: all 0.3s ease !important;
    margin-top: 25px !important; 
    box-shadow: 0 4px 15px rgba(192, 27, 27, 0.5) !important;
}}

div.stButton > button:hover {{
    background-color: #9A1515 !important;
    transform: translateY(-2px) !important;
}}

/* Centrar logo */
.centered-logo {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    # Creamos 3 columnas. La central es donde irá el login.
    # Proporción: 1 espacio vacío - 1.2 caja de login - 1 espacio vacío
    col1, col2, col3 = st.columns([1, 1.2, 1]) 
    
    # --- COLUMNA 2: PANEL CENTRAL ---
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            st.image("logo.png", width=220)
        except:
            st.warning("⚠️ Recuerda subir 'logo.png' a GitHub.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        
        if st.button("Iniciar Sesión", use_container_width=True):
            if usuario == "admin" and contrasena == "123":
                st.session_state['logeado'] = True
                st.session_state['rol'] = "admin"
                st.rerun()
            else:
                st.error("❌ Credenciales incorrectas.")

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
        st.write("Bienvenido, Administrador. Este es el centro de control.")
        st.success("¡Inicio de sesión exitoso!")
