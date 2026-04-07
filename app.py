import streamlit as st

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

# --- CSS AVANZADO Y AJUSTE DE PANTALLA ---
st.markdown("""
<style>
/* 1. Fondo de Pantalla Original */
.stApp {
    background-color: #0e1117; /* Color de respaldo */
}

/* 2. Reducir los espacios en blanco gigantes de Streamlit arriba y abajo */
.block-container {
    padding-top: 3rem !important; 
    padding-bottom: 1rem !important;
    max-width: 1100px !important; /* Evita que se estire demasiado a los lados */
}

/* 3. Quitar fondo por defecto de las columnas */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {
    background-color: transparent !important;
    align-items: center; /* Centra los paneles verticalmente */
}

/* 4. Panel Izquierdo (Degradado oscuro) */
[data-testid="stColumn"]:nth-child(1) {
    background: linear-gradient(135deg, rgba(15, 15, 15, 0.98) 0%, rgba(60, 10, 10, 0.9) 100%);
    padding: 40px 50px !important; /* Reduje el padding vertical para que quepa mejor */
    color: white !important;
    border-radius: 20px 0px 0px 20px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: -5px 0px 20px rgba(0,0,0,0.3);
    min-height: 60vh; /* Altura más controlada */
}

[data-testid="stColumn"]:nth-child(1) h1,
[data-testid="stColumn"]:nth-child(1) p {
    color: white !important;
}

/* 5. Panel Derecho (Blanco limpio) */
[data-testid="stColumn"]:nth-child(2) {
    background-color: rgba(255, 255, 255, 0.98); 
    padding: 30px 50px !important; /* Reduje el padding para que no empuje el botón hacia abajo */
    border-radius: 0px 20px 20px 0px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 10px 0px 25px rgba(0, 0, 0, 0.6); 
    min-height: 60vh;
}

[data-testid="stColumn"]:nth-child(2) h2 {
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 700;
    margin-top: 0px;
    margin-bottom: 10px;
}

[data-testid="stColumn"]:nth-child(2) label {
    color: #4a4a4a !important;
    font-weight: 600;
}

/* 6. Personalización del Botón al estilo San Marino */
div.stButton > button {
    background-color: #B31B1B !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
    margin-top: 10px !important; /* Un pequeño empujón hacia abajo, pero controlado */
}

div.stButton > button:hover {
    background-color: #8A1515 !important;
    box-shadow: 0px 5px 15px rgba(179, 27, 27, 0.4) !important;
    transform: translateY(-2px) !important;
}

.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    col1, col2 = st.columns([1.1, 1]) # Proporción ligeramente ajustada para balancear la pantalla
    
    # --- COLUMNA 1: PANEL IZQUIERDO ---
    with col1:
        st.markdown("<h1 style='font-size: 3.5rem; line-height: 1.1; margin-bottom: 0;'>Welcome<br>Back</h1>", unsafe_allow_html=True)
        # Línea decorativa roja
        st.markdown("<hr style='border: 2px solid #B31B1B; width: 60px; margin-left: 0; margin-top: 15px; margin-bottom: 20px;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1rem;'>Bienvenido a San Marino motor logístico. Tenga precaución a los datos que va a ingresar.</p>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='display: flex; gap: 15px; font-size: 1.2rem; color: #aaa; margin-top: 30px;'>
            🌐 ✉️ 🔒
        </div>
        """, unsafe_allow_html=True)

    # --- COLUMNA 2: PANEL DERECHO (FORMULARIO Y LOGO) ---
    with col2:
        # Contenedor del logo
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            # Forzamos un ancho para que no se estire de forma descontrolada hacia abajo
            st.image("logo.png", width=220)
        except:
            st.warning("⚠️ Falta subir 'logo.png' a GitHub.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        
        # Campos de texto (Streamlit los apila automáticamente sin necesidad de espacios extra)
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        
        # Botón único
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
