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

# --- CSS AVANZADO Y PALETA DE COLORES ---
st.markdown("""
<style>
/* 1. Fondo de Pantalla Original */
.stApp {
    background-image: url("https://images.unsplash.com/photo-1587293852726-59cd15a774bd?q=80&w=2000&auto=format&fit=crop"); 
    background-size: cover;
    background-position: center;
}

/* 2. Quitar fondo por defecto de las columnas */
[data-testid="stVerticalBlock"] > [data-testid="stColumns"] {
    background-color: transparent !important;
}

/* 3. Panel Izquierdo (Degradado oscuro elegante) */
[data-testid="stColumn"]:nth-child(1) {
    /* Degradado sutil de negro a un rojo muy oscuro corporativo */
    background: linear-gradient(135deg, rgba(15, 15, 15, 0.9) 0%, rgba(60, 10, 10, 0.85) 100%);
    padding: 100px 50px !important;
    color: white !important;
    border-radius: 20px 0px 0px 20px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 80vh;
    box-shadow: -5px 0px 20px rgba(0,0,0,0.3);
}

[data-testid="stColumn"]:nth-child(1) h1,
[data-testid="stColumn"]:nth-child(1) p {
    color: white !important;
}

/* 4. Panel Derecho (Blanco limpio) */
[data-testid="stColumn"]:nth-child(2) {
    background-color: rgba(255, 255, 255, 0.98); 
    padding: 40px 50px !important;
    border-radius: 0px 20px 20px 0px; 
    display: flex;
    flex-direction: column;
    justify-content: center;
    box-shadow: 10px 0px 25px rgba(0, 0, 0, 0.6); 
    min-height: 80vh;
}

[data-testid="stColumn"]:nth-child(2) h2 {
    color: #1a1a1a !important;
    text-align: center;
    font-weight: 700;
    margin-top: 10px;
}

[data-testid="stColumn"]:nth-child(2) label {
    color: #4a4a4a !important;
    font-weight: 600;
}

/* 5. Personalización del Botón al estilo San Marino */
div.stButton > button {
    background-color: #B31B1B !important; /* Rojo San Marino */
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    font-weight: bold !important;
    font-size: 1.1rem !important;
    transition: all 0.3s ease !important;
}

div.stButton > button:hover {
    background-color: #8A1515 !important; /* Rojo más oscuro al pasar el mouse */
    box-shadow: 0px 5px 15px rgba(179, 27, 27, 0.4) !important;
    transform: translateY(-2px) !important;
}

.centered-logo {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
    padding: 0px 20px;
}
</style>
""", unsafe_allow_html=True)

# --- PANTALLA DE INICIO DE SESIÓN ---
if not st.session_state['logeado']:
    
    col1, col2 = st.columns([3, 2])
    
    # --- COLUMNA 1: PANEL IZQUIERDO ---
    with col1:
        st.markdown("<br><h1 style='font-size: 4.5rem; line-height: 1.1;'>Welcome<br>Back</h1>", unsafe_allow_html=True)
        # Línea decorativa roja
        st.markdown("<hr style='border: 2px solid #B31B1B; width: 50px; margin-left: 0;'>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.2rem; margin-top: 20px;'>Bienvenido a San Marino motor logístico. Tenga precaución a los datos que va a ingresar.</p>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown("""
        <div style='display: flex; gap: 15px; font-size: 1.5rem; color: #ddd;'>
            🌐 ✉️ 🔒
        </div>
        """, unsafe_allow_html=True)

    # --- COLUMNA 2: PANEL DERECHO (FORMULARIO Y LOGO MAXIMIZADO) ---
    with col2:
        # Contenedor del logo: Usamos todo el ancho de la columna
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try:
            # Quitamos el límite de 'width' para que ocupe todo el espacio elegantemente
            st.image("logo.png", use_container_width=True)
        except:
            st.warning("⚠️ Falta subir 'logo.png' a GitHub.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("<h2>Iniciar Sesión</h2>", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Campos de texto
        usuario = st.text_input("Usuario")
        contrasena = st.text_input("Contraseña", type="password")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Botón único con el nuevo estilo rojo
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
