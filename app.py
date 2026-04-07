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

# --- CSS AVANZADO: PANEL COMPACTO Y CON ICONOS INTERNOS ---
st.markdown(f"""
<style>
/* Fondo de Pantalla */
.stApp {{
    background-image: url("data:image/avif;base64,{bg_base64}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

.stApp > header {{
    background-color: transparent !important;
}}

/* Estructura general */
.block-container {{
    padding-top: 15vh !important; 
    max-width: 1200px !important;
}}

/* Alinear columnas al centro */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {{
    background-color: transparent !important;
    align-items: center; 
    justify-content: center;
}}

/* PANEL CENTRAL (Aún más corto y ancho) */
[data-testid="stColumn"]:nth-child(2) {{
    background: rgba(255, 255, 255, 0.25); 
    backdrop-filter: blur(15px); 
    -webkit-backdrop-filter: blur(15px);
    border: 1px solid rgba(255, 255, 255, 0.4); 
    /* Padding ultra reducido: Arriba 15px, Lados 40px, Abajo 20px */
    padding: 15px 40px 20px 40px !important; 
    border-radius: 20px !important; 
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.3); 
}}

/* Contenedor del Logo */
.centered-logo {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 0px; 
}}

/* Títulos */
[data-testid="stColumn"]:nth-child(2) h2 {{
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 500; 
    font-size: 1.6rem;
    margin-bottom: 5px; 
    margin-top: 0px; 
}}

/* Textos de las etiquetas (Usuario / Contraseña) */
.stTextInput label p {{
    color: #2c2c2c !important;
    font-weight: 600 !important;
    margin-bottom: -5px !important; /* Acerca el texto a la caja */
    font-size: 0.9rem !important;
}}

/* --- SOLUCIÓN PARA QUE EL OJO QUEDE ADENTRO --- */
/* Le damos estilo al contenedor principal, no al input suelto */
div[data-baseweb="input"] {{
    background-color: rgba(255, 255, 255, 0.6) !important;
    border-radius: 10px !important;
    border: 1px solid rgba(255, 255, 255, 0.8) !important;
    transition: all 0.3s ease;
}}

/* Efecto de brillo al hacer clic (como en tu foto 1) */
div[data-baseweb="input"]:focus-within {{
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(255, 255, 255, 1) !important;
}}

/* Hacemos transparente el input real para que se vea el contenedor */
div[data-baseweb="input"] input {{
    background-color: transparent !important;
    color: #333 !important;
    padding: 8px 10px 8px 35px !important; /* Espacio a la izquierda para el icono */
}}

/* --- ICONOS DENTRO DE LAS CAJAS (Inyectando SVGs) --- */
/* Icono de Usuario (Para la primera caja) */
div[data-testid="stTextInput"]:nth-of-type(1) input {{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: 10px center;
    background-size: 16px;
}}

/* Icono de Llave (Para la segunda caja) */
div[data-testid="stTextInput"]:nth-of-type(2) input {{
    background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23555' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4'/%3E%3C/svg%3E");
    background-repeat: no-repeat;
    background-position: 10px center;
    background-size: 16px;
}}

/* Botón Rojo (Ultra compacto) */
div.stButton > button {{
    background-color: #C01B1B !important; 
    color: white !important;
    border: none !important;
    border-radius: 20px !important; 
    padding: 5px 20px !important; 
    font-weight: bold !important;
    font-size: 1rem !important;
    transition: all 0.3s ease !important;
    margin-top: 5px !important; 
    box-shadow: 0 4px 10px rgba(192, 27, 27, 0.4) !important;
}}

div.stButton > button:hover {{
    background-color: #9A1515 !important;
    transform: translateY(-2px) !important;
}}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    col1, col2, col3 = st.columns([1, 1.3, 1]) 
    
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            st.image("logo.png", width=260)
        except:
            st.warning("⚠️ Recuerda subir 'logo.png' a GitHub.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password") # El ojo nativo ahora está contenido
        
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
