import streamlit as st
import base64
import pandas as pd
import time # Para simular el tiempo de cálculo

# 1. Configuración de la página
st.set_page_config(
    page_title="San Marino Logística", 
    layout="wide", 
    initial_sidebar_state="expanded" # Ahora lo dejamos abierto para el menú
)

# 2. SISTEMA DE MEMORIA
if 'logeado' not in st.session_state:
    st.session_state['logeado'] = False
    st.session_state['rol'] = None
if 'maestra_actual' not in st.session_state:
    st.session_state['maestra_actual'] = None
# NUEVA MEMORIA: Para saber en qué pestaña del menú estamos
if 'menu_actual' not in st.session_state:
    st.session_state['menu_actual'] = "Despachos" # Que inicie por defecto en despachos

# --- DICCIONARIO DE ARCHIVOS EXACTOS ---
ARCHIVOS_EXCEL = {
    "Conductores": "Conductores Sanmarino.xlsx", 
    "Vendedores": "Vendedores sanmarino.xlsx",
    "Carros": "Carros sanmarino.xlsx",
    "Rutas": "Rutas sanmarino.xlsx",
    "Clientes": "Clientes sanmarino.xlsx",
    "Vacunas": "Vacunas sanmarino.xlsx",
    "Granjas": "Granjas sanmarino.xlsx"
}

# --- FUNCIÓN DE IMAGEN DE FONDO ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("imagen fondo 1.avif")

# ==========================================
# PANTALLA DE INICIO DE SESIÓN
# ==========================================
if not st.session_state['logeado']:
    st.markdown(f"""
    <style>
    html, body, .stApp {{ overflow: hidden !important; margin: 0 !important; padding: 0 !important; height: 100vh !important; }}
    header[data-testid="stHeader"] {{ display: none !important; }}
    .stApp {{ background-image: url("data:image/avif;base64,{bg_base64}"); background-size: cover; background-position: center; background-repeat: no-repeat; }}
    .block-container {{ padding: 0 !important; margin: 0 auto !important; max-width: 100% !important; height: 100vh !important; display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: center !important; }}
    [data-testid="stColumn"]:nth-child(2) {{ background: rgba(255, 255, 255, 0.25) !important; backdrop-filter: blur(15px) !important; -webkit-backdrop-filter: blur(15px) !important; border: 1px solid rgba(255, 255, 255, 0.4) !important; border-radius: 20px !important; padding: 35px 45px !important; box-shadow: 0 10px 40px 0 rgba(0, 0, 0, 0.3) !important; width: 400px !important; min-width: 400px !important; flex: none !important; height: auto !important; }}
    [data-testid="stColumn"]:nth-child(2) h2 {{ color: #1a1a1a !important; text-align: center !important; font-weight: 500 !important; font-size: 1.8rem !important; margin-top: 0 !important; margin-bottom: 20px !important; }}
    .stTextInput label p {{ color: #2c2c2c !important; font-weight: 600 !important; margin-bottom: 2px !important; }}
    div[data-baseweb="input"] {{ background-color: rgba(255, 255, 255, 0.35) !important; border-radius: 10px !important; border: 1px solid rgba(255, 255, 255, 0.6) !important; transition: all 0.3s ease; }}
    div[data-baseweb="input"]:focus-within {{ background-color: rgba(255, 255, 255, 0.6) !important; border: 1px solid white !important; box-shadow: 0 0 10px rgba(255, 255, 255, 0.5) !important; }}
    div[data-baseweb="input"] > div, div[data-baseweb="input"] button {{ background-color: transparent !important; }}
    div[data-baseweb="input"] input {{ background-color: transparent !important; color: #111 !important; padding-left: 35px !important; }}
    div[data-testid="stTextInput"]:nth-of-type(1) input {{ background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2'/%3E%3Ccircle cx='12' cy='7' r='4'/%3E%3C/svg%3E") !important; background-repeat: no-repeat !important; background-position: 10px center !important; background-size: 16px !important; }}
    div[data-testid="stTextInput"]:nth-of-type(2) input {{ background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%23333' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M21 2l-2 2m-7.61 7.61a5.5 5.5 0 1 1-7.778 7.778 5.5 5.5 0 0 1 7.777-7.777zm0 0L15.5 7.5m0 0l3 3L22 7l-3-3m-3.5 3.5L19 4'/%3E%3C/svg%3E") !important; background-repeat: no-repeat !important; background-position: 10px center !important; background-size: 16px !important; }}
    div.stButton > button {{ background-color: #C01B1B !important; color: white !important; border: none !important; border-radius: 25px !important; padding: 8px 20px !important; font-weight: bold !important; font-size: 1.1rem !important; width: 100% !important; margin-top: 15px !important; box-shadow: 0 4px 15px rgba(192, 27, 27, 0.4) !important; }}
    div.stButton > button:hover {{ background-color: #9A1515 !important; transform: translateY(-2px) !important; }}
    .centered-logo {{ display: flex; justify-content: center; align-items: center; margin-bottom: 5px; }}
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1]) 
    with col2:
        st.markdown('<div class="centered-logo">', unsafe_allow_html=True)
        try: st.image("logo.png", width=260)
        except: st.warning("⚠️ Falta 'logo.png'")
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

# ==========================================
# PANTALLA INTERNA (PANEL DE ADMINISTRADOR)
# ==========================================
else:
    st.markdown("""
    <style>
    .stApp { background-image: none !important; background-color: #353846 !important; }
    html, body { overflow: auto !important; height: auto !important; }
    .block-container { padding-top: 2rem !important; display: block !important; max-width: 95% !important; }
    h1, h2, h3, p, span, label, li { color: #F0F2F6 !important; }
    
    /* Botón de cerrar sesión */
    .btn-cerrar div.stButton > button { background-color: #C01B1B !important; color: white !important; border: none !important; border-radius: 8px !important; width: 100% !important; }
    /* Botones de menú lateral (gris) */
    .btn-menu div.stButton > button { background-color: #262730 !important; color: white !important; border: 1px solid #4a4c59 !important; border-radius: 8px !important; width: 100% !important; text-align: left !important; padding-left: 20px !important; }
    .btn-menu div.stButton > button:hover { border-color: #C01B1B !important; color: #C01B1B !important; }
    
    div[data-testid="stExpanderDetails"] div.stButton > button { background-color: #262730 !important; border: 1px solid #4a4c59 !important; transition: all 0.2s ease-in-out !important; }
    div[data-testid="stExpanderDetails"] div.stButton > button:hover { border-color: #C01B1B !important; color: #C01B1B !important; }
    
    /* Cajita para arrastrar archivos (Uploader) */
    [data-testid="stFileUploader"] { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; border: 2px dashed #4a4c59; }
    </style>
    """, unsafe_allow_html=True)

    # --- MENÚ LATERAL (NAVEGACIÓN) ---
    st.sidebar.title("San Marino")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown('<div class="btn-menu">', unsafe_allow_html=True)
    if st.sidebar.button("📦 Programar Despachos"):
        st.session_state['menu_actual'] = "Despachos"
    if st.sidebar.button("📁 Bases de Datos (Maestras)"):
        st.session_state['menu_actual'] = "Maestras"
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown('<div class="btn-cerrar">', unsafe_allow_html=True)
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear() # Limpia toda la memoria
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)


    # ==========================================
    # PESTAÑA 1: PROGRAMAR DESPACHOS
    # ==========================================
    if st.session_state['menu_actual'] == "Despachos":
        st.title("📦 Motor de Asignación y Despachos")
        st.write("Sube el archivo de Excel más reciente del **Área de Ventas** para calcular las rutas y asignaciones óptimas.")
        
        # 1. Cargador de archivos
        archivo_ventas = st.file_uploader("Arrastra tu Excel de Ventas aquí (o haz clic para buscar)", type=["xlsx", "xls"])
        
        if archivo_ventas is not None:
            st.success("✅ Archivo cargado correctamente.")
            
            # El "Cerebro" esperando que aprietes el botón
            st.markdown("---")
            col_izq, col_der = st.columns([2, 1])
            with col_izq:
                st.info("El sistema cruzará la cantidad de productos de este archivo con la disponibilidad de las Granjas, Carros y Conductores.")
            with col_der:
                # ¡EL BOTÓN QUE PEDISTE!
                if st.button("🚀 Calcular y Programar Todo", use_container_width=True):
                    # Simulamos que Python está pensando
                    with st.spinner('Procesando datos, cruzando con Maestras y calculando rutas óptimas...'):
                        time.sleep(3) # Simula 3 segundos de cálculo
                    
                    st.success("🎉 ¡Programación completada con éxito!")
                    st.balloons()
                    st.warning("🚧 El algoritmo interno de cruce está en construcción. Aquí aparecerá la tabla final con la asignación por conductor.")


    # ==========================================
    # PESTAÑA 2: BASES DE DATOS (MAESTRAS)
    # ==========================================
    elif st.session_state['menu_actual'] == "Maestras":
        st.title("📁 Gestión de Bases de Datos")
        
        with st.expander("Seleccionar Maestra para editar", expanded=True):
            espacio_izq, col_centro1, col_centro2, col_centro3, espacio_der = st.columns([1, 2, 2, 2, 1])
            
            with col_centro1:
                if st.button("🧑‍✈️ Conductores", use_container_width=True): st.session_state['maestra_actual'] = "Conductores"
                if st.button("🤝 Vendedores", use_container_width=True): st.session_state['maestra_actual'] = "Vendedores"
                if st.button("🐔 Granjas", use_container_width=True): st.session_state['maestra_actual'] = "Granjas"
            with col_centro2:
                if st.button("🚚 Carros", use_container_width=True): st.session_state['maestra_actual'] = "Carros"
                if st.button("🗺️ Rutas", use_container_width=True): st.session_state['maestra_actual'] = "Rutas"
            with col_centro3:
                if st.button("🏢 Clientes", use_container_width=True): st.session_state['maestra_actual'] = "Clientes"
                if st.button("💉 Vacunas", use_container_width=True): st.session_state['maestra_actual'] = "Vacunas"
                
        st.markdown("<br>", unsafe_allow_html=True)
        
        # EDITOR DINÁMICO DE EXCEL (CRUD)
        if st.session_state['maestra_actual']:
            nombre_maestra = st.session_state['maestra_actual']
            nombre_archivo_exacto = ARCHIVOS_EXCEL[nombre_maestra]
            
            st.subheader(f"Editando: {nombre_maestra}")
            
            try:
                df = pd.read_excel(nombre_archivo_exacto)
                df_editado = st.data_editor(
                    df, num_rows="dynamic", use_container_width=True, key=f"editor_{nombre_maestra}" 
                )
                
                if st.button(f"💾 Guardar cambios en {nombre_maestra}"):
                    df_editado.to_excel(nombre_archivo_exacto, index=False)
                    st.success(f"¡Base de datos '{nombre_archivo_exacto}' actualizada!")
                    
            except FileNotFoundError:
                st.error(f"Error: Sube el archivo '{nombre_archivo_exacto}' a GitHub para poder editarlo.")
