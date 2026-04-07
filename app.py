import streamlit as st
import base64

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
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("imagen fondo 1.avif")

# --- CSS AVANZADO: BLOQUEO TOTAL DE SCROLL Y PANEL TIPO CAJA ---
st.markdown(f"""
<style>
/* 1. ELIMINAR EL SCROLL (El movimiento de la pantalla) */
html, body, .stApp {{
    overflow: hidden !important; 
    margin: 0 !important;
    padding: 0 !important;
    height: 100vh !important;
}}

/* Ocultar la barra superior invisible de Streamlit que causa el salto */
header[data-testid="stHeader"] {{
    display: none !important; 
}}

/* 2. FONDO DE PANTALLA */
.stApp {{
    background-image: url("data:image/avif;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

/* 3. CENTRADO ABSOLUTO (Convierte la pantalla en una mesa para centrar la caja) */
.block-container {{
    padding: 0 !important;
    margin: 0 auto !important;
    max-width: 100% !important;
    height: 100vh !important;
    display: flex !important;
    flex-direction: column !important;
    justify-content: center !important; 
    align-items: center !important;
}}

/* 4. EL PANEL CENTRAL (Compacto, no estirado) */
[data-testid="stColumn"]:nth-child(2) {{
    background: rgba(255, 255, 255, 0.25) !important; /* Vidrio claro */
    backdrop-filter: blur(15px) !important; 
    -webkit-backdrop-filter: blur(15px) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 20px !important; 
    padding: 40px 50px !important; 
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.3) !important;
    width: 420px !important; /* Ancho fijo */
    min-width: 420px !important;
    flex: none !important; 
    height: auto !important; /* ESTO ARREGLA LO LARGO, se adapta al contenido */
}}

/* Textos y Títulos */
[data-testid="stColumn"]:nth-child(2) h2 {{
    color: #1a1a1a !important;
    text-align: center !important;
    font-weight: 500 !important;
    font-size: 2rem !important;
    margin-top: 0 !important;
    margin-bottom: 25px !important;
}}

.stTextInput label p {{
    color: #2c2c2c !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
}}

/* 5. CAJAS DE TEXTO TRANSPARENTES (Efecto Vidrio Integrado) */
div[data-baseweb="input"] {{
    background-color: rgba(255, 255, 255, 0.35) !important; /* Más transparente */
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.6) !important;
}}

div[data-baseweb="input"]:focus-within {{
    background-color: rgba(255, 255, 255, 0.6) !important;
    border: 1px solid white !important;
    box-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important;
}}

/* Hace que el fondo real del input y el ojo sean invisibles para que se vea el contenedor */
div[data-baseweb="input"] > div, div[data-baseweb="input"] input, div[data-baseweb="input"] button {{
    background-color: transparent !important;
}}

div[data-baseweb="input"] input {{
    color: #111 !important; /* Texto oscuro para que se lea bien */
}}

/* 6. BOTÓN ROJO */
div.stButton > button {{
    background-color: #C01B1B !important; 
    color: white !important;
    border: none !important;
    border-radius: 25px !important; 
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    width: 100% !important;
    margin-top: 20px !important; 
    box-shadow: 0 4px 15px rgba(192, 27, 27, 0.4) !important;
}}

div.stButton > button:hover {{
    background-color: #9A1515 !important;
    transform: translateY(-2px) !important;
}}

.centered-logo {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
}}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    col1, col2, col3 = st.columns([1, 1, 1]) 
    
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            st.image("logo.png", width=280)
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
