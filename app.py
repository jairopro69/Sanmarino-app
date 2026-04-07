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
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("imagen fondo 1.avif")

# --- CSS AVANZADO: PANTALLA FIJA Y CAJAS TRANSPARENTES ---
st.markdown(f"""
<style>
/* 1. Fondo de Pantalla Completo y FIJO (para que no se mueva al scrollear) */
.stApp {{
    background-image: url("data:image/avif;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    height: 100vh !important; /* Fuerza a que la página ocupe solo el alto de la pantalla */
    overflow: hidden !important; /* Desactiva el scroll de la página completa */
}}

.stApp > header {{
    background-color: transparent !important;
}}

/* 2. Estructura para Centrar el Panel */
.block-container {{
    padding-top: 0vh !important; /* Ajuste para centrado vertical */
    padding-bottom: 0vh !important;
    height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    max-width: 1200px !important;
}}

/* Asegurar que el contenedor de columnas esté centrado */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {{
    background-color: transparent !important;
    align-items: center; 
    justify-content: center;
    height: 100%; /* Ocupa el centro vertical */
}}

/* 3. Panel Central (Vidrio Esmerilado) */
[data-testid="stColumn"]:nth-child(2) {{
    background: rgba(255, 255, 255, 0.4); /* Blanco semi-transparente y claro */
    backdrop-filter: blur(15px); 
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.5); 
    padding: 30px 50px 40px 50px !important; 
    border-radius: 20px !important; 
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4); 
    width: 420px !important; /* Ancho fijo y robusto */
    max-width: 420px !important;
    flex: none !important;
}}

/* 4. Títulos y Textos */
[data-testid="stColumn"]:nth-child(2) h2 {{
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 500; 
    font-size: 2.2rem;
    margin-bottom: 25px;
    margin-top: 0px;
}}

.stTextInput label p {{
    color: #2c2c2c !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
}}

/* --- 5. SOLUCIÓN CAJAS TRANSPARENTES (MÁS CLARAS Y LUMINOSAS) --- */
.stTextInput input {{
    /* Cambiamos a blanco semi-transparente para el efecto 'vidrio' claro */
    background-color: rgba(255, 255, 255, 0.8) !important; 
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
    color: #111 !important; /* Texto un poco más oscuro para buen contraste */
    box-shadow: inset 0 2px 5px rgba(255, 255, 255, 0.2); /* Sombra interna sutil */
}}

/* Brillo al hacer foco en la caja (claro e intenso) */
.stTextInput input:focus {{
    box-shadow: 0 0 12px rgba(255, 255, 255, 0.9) !important;
    background-color: rgba(255, 255, 255, 0.95) !important;
}}

/* 6. Botón Rojo */
div.stButton > button {{
    background-color: #C01B1B !important; 
    color: white !important;
    border: none !important;
    border-radius: 30px !important; /* Forma de píldora */
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    margin-top: 25px !important; 
    box-shadow: 0 4px 15px rgba(192, 27, 27, 0.4) !important;
}}

div.stButton > button:hover {{
    background-color: #9A1515 !important;
    transform: translateY(-2px) !important;
}}

/* Centrar logo y reducir espacios */
.centered-logo {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    margin-top: -15px; /* Sube el logo */
}}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    # Usamos 3 columnas, la central (1.3) para el panel centrado
    col1, col2, col3 = st.columns([1, 1.3, 1]) 
    
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            # Tamaño de logo grande para impacto visual
            st.image("logo.png", width=310)
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
