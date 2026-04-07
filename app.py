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

# --- CSS AVANZADO: EFECTO VIDRIO COMPACTO Y ROBUSTO ---
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
    padding-top: 10vh !important; /* Empuja un poco desde arriba */
    max-width: 1200px !important;
}}

/* Alinear columnas al centro */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {{
    background-color: transparent !important;
    align-items: center; 
    justify-content: center;
}}

/* Panel Central (Más corto de altura, más ancho) */
[data-testid="stColumn"]:nth-child(2) {{
    background: rgba(255, 255, 255, 0.35); 
    backdrop-filter: blur(12px); 
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.5); 
    padding: 30px 50px 40px 50px !important; /* Menos espacio arriba y abajo, más a los lados */
    border-radius: 20px !important; 
    box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.4); 
}}

/* Textos y Títulos */
[data-testid="stColumn"]:nth-child(2) h2 {{
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 500; 
    font-size: 2rem;
    margin-bottom: 20px;
    margin-top: 0px;
}}

.stTextInput label p {{
    color: #2c2c2c !important;
    font-weight: 600 !important;
    margin-bottom: 2px !important;
}}

/* Cajas de texto */
.stTextInput input {{
    background-color: rgba(255, 255, 255, 0.7) !important;
    border-radius: 8px !important;
    border: 1px solid rgba(255, 255, 255, 0.9) !important;
    color: #333 !important;
}}

/* Botón Rojo */
div.stButton > button {{
    background-color: #C01B1B !important; 
    color: white !important;
    border: none !important;
    border-radius: 20px !important; 
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    margin-top: 20px !important; 
    box-shadow: 0 4px 15px rgba(192, 27, 27, 0.4) !important;
}}

div.stButton > button:hover {{
    background-color: #9A1515 !important;
    transform: translateY(-2px) !important;
}}

/* Contenedor del Logo */
.centered-logo {{
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    margin-top: -10px; /* Sube el logo un poquito */
}}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    # Ajustamos proporciones para que el panel central sea más robusto (más ancho)
    col1, col2, col3 = st.columns([1, 1.4, 1]) 
    
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            # Aumentamos el tamaño del logo
            st.image("logo.png", width=290)
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
