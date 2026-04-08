import streamlit as st
import base64
import pandas as pd
import time
import math

# ==========================================
# 1. CONFIGURACIÓN INICIAL
# ==========================================
st.set_page_config(
    page_title="San Marino Logística", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. SISTEMA DE MEMORIA (ESTADOS)
# ==========================================
if 'logeado' not in st.session_state:
    st.session_state['logeado'] = False
if 'menu_actual' not in st.session_state:
    st.session_state['menu_actual'] = "Despachos" 
if 'maestra_actual' not in st.session_state:
    st.session_state['maestra_actual'] = None
# NUEVO: Memoria para guardar el Excel de ventas y no perderlo al cambiar de menú
if 'df_ventas' not in st.session_state:
    st.session_state['df_ventas'] = None

# ==========================================
# 3. CONSTANTES Y DICCIONARIOS
# ==========================================
ARCHIVOS_EXCEL = {
    "Conductores": "Conductores Sanmarino.xlsx", 
    "Vendedores": "Vendedores sanmarino.xlsx",
    "Carros": "Carros sanmarino.xlsx",
    "Rutas": "Rutas sanmarino.xlsx",
    "Clientes": "Clientes sanmarino.xlsx",
    "Vacunas": "Vacunas sanmarino.xlsx",
    "Granjas": "Granjas sanmarino.xlsx"
}

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

bg_base64 = get_base64_of_bin_file("imagen fondo 1.avif")

# ==========================================
# 4. PANTALLA DE INICIO DE SESIÓN
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
        except: st.warning("⚠️ Recuerda subir 'logo.png' a GitHub.")
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
# 5. PANTALLA INTERNA (PANEL PRINCIPAL)
# ==========================================
else:
    st.markdown("""
    <style>
    .stApp { background-image: none !important; background-color: #353846 !important; }
    html, body { overflow: auto !important; height: auto !important; }
    .block-container { padding-top: 2rem !important; display: block !important; max-width: 95% !important; }
    h1, h2, h3, p, span, label, li { color: #F0F2F6 !important; }
    
    /* Botones del Menú Lateral */
    .btn-cerrar div.stButton > button { background-color: #C01B1B !important; color: white !important; border: none !important; border-radius: 8px !important; width: 100% !important; }
    
    /* Diseño de los botones del menú lateral para que se vean como los tuyos */
    .btn-menu div.stButton > button { background-color: #262730 !important; color: white !important; border: 1px solid #4a4c59 !important; border-radius: 8px !important; width: 100% !important; text-align: left !important; padding-left: 20px !important; margin-bottom: 5px !important; transition: all 0.2s;}
    .btn-menu div.stButton > button:hover { border-color: #C01B1B !important; color: #C01B1B !important; background-color: #1e1f26 !important;}
    
    /* Diseño específico para los sub-botones de productos */
    .btn-sub-menu div.stButton > button { background-color: transparent !important; color: #b0b3c6 !important; border: none !important; border-left: 3px solid transparent !important; border-radius: 0px !important; width: 100% !important; text-align: left !important; padding-left: 40px !important; margin-bottom: 2px !important; font-size: 0.95rem !important;}
    .btn-sub-menu div.stButton > button:hover { color: white !important; border-left: 3px solid #C01B1B !important; background-color: rgba(255,255,255,0.05) !important;}
    
    /* Botones de Maestras */
    div[data-testid="stExpanderDetails"] div.stButton > button { background-color: #262730 !important; border: 1px solid #4a4c59 !important; transition: all 0.2s ease-in-out !important; }
    div[data-testid="stExpanderDetails"] div.stButton > button:hover { border-color: #C01B1B !important; color: #C01B1B !important; }
    
    /* Cargador de archivos */
    [data-testid="stFileUploader"] { background-color: rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 20px; border: 2px dashed #4a4c59; }
    </style>
    """, unsafe_allow_html=True)

    # --- MENÚ LATERAL EXACTAMENTE COMO LO PEDISTE ---
    st.sidebar.title("San Marino")
    st.sidebar.markdown("---")
    
    st.sidebar.markdown('<div class="btn-menu">', unsafe_allow_html=True)
    if st.sidebar.button("📦 Programar Despachos"): st.session_state['menu_actual'] = "Despachos"
    if st.sidebar.button("📁 Bases de Datos (Maestras)"): st.session_state['menu_actual'] = "Maestras"
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Separador sutil para los productos
    st.sidebar.markdown("<hr style='margin: 10px 0; border-color: #4a4c59;'>", unsafe_allow_html=True)
    
    # Los 3 nuevos botones integrados en el menú lateral
    st.sidebar.markdown('<div class="btn-sub-menu">', unsafe_allow_html=True)
    if st.sidebar.button("🥚 Huevo"): st.session_state['menu_actual'] = "Huevo"
    if st.sidebar.button("🌽 Alimento"): st.session_state['menu_actual'] = "Alimento"
    if st.sidebar.button("🐥 Pollito"): st.session_state['menu_actual'] = "Pollito"
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("<br><br><br><br>", unsafe_allow_html=True)
    st.sidebar.markdown('<div class="btn-cerrar">', unsafe_allow_html=True)
    if st.sidebar.button("Cerrar Sesión"):
        st.session_state.clear()
        st.rerun()
    st.sidebar.markdown('</div>', unsafe_allow_html=True)

    # ==========================================
    # SECCIÓN: PROGRAMAR DESPACHOS (SUBIDA DE ARCHIVO)
    # ==========================================
    if st.session_state['menu_actual'] == "Despachos":
        st.title("📦 Carga de Pedidos")
        st.write("1. Sube aquí el archivo de Excel del **Área de Ventas**.")
        st.write("2. Luego selecciona en el menú lateral izquierdo qué línea vas a programar (Huevo, Alimento o Pollito).")
        
        archivo_ventas = st.file_uploader("Arrastra tu Excel de Ventas aquí", type=["xlsx", "xls"], key="up_ventas")
        
        if archivo_ventas is not None:
            # GUARDAMOS EL ARCHIVO EN LA MEMORIA DE PYTHON
            st.session_state['df_ventas'] = pd.read_excel(archivo_ventas)
            st.success("✅ Archivo cargado y guardado en la memoria del sistema.")
            st.info("👉 Ahora haz clic en **Huevo**, **Alimento** o **Pollito** en el menú de la izquierda para generar las rutas.")

    # ==========================================
    # SECCIÓN: CÁLCULO HUEVO
    # ==========================================
    elif st.session_state['menu_actual'] == "Huevo":
        st.title("🥚 Programación de Rutas: HUEVO")
        
        # Verificamos si el usuario ya subió el archivo en "Despachos"
        if st.session_state['df_ventas'] is not None:
            df_ventas = st.session_state['df_ventas']
            
            st.info("Utilizando el archivo de ventas cargado previamente.")
            if st.button("🚀 Calcular Viajes Necesarios", use_container_width=True):
                with st.spinner('Analizando granjas y cruzando con carros tipo Huevo...'):
                    time.sleep(1) 
                    try:
                        df_carros = pd.read_excel(ARCHIVOS_EXCEL["Carros"])
                        carros_huevo = df_carros[df_carros.astype(str).apply(lambda x: x.str.contains('Huevo', case=False, na=False)).any(axis=1)]
                        num_carros_disp = len(carros_huevo)
                    except FileNotFoundError:
                        st.error(f"Falta el archivo maestra '{ARCHIVOS_EXCEL['Carros']}'.")
                        num_carros_disp = 0
                    except Exception:
                        num_carros_disp = 10 
                    
                    try:
                        resumen_granjas = df_ventas.groupby('Granja')['Cantidad'].sum().reset_index()
                        total_viajes_global = 0
                        
                        st.markdown("---")
                        col_info, col_metric = st.columns([2,1])
                        with col_info:
                            st.write("### 📋 Resumen Logístico")
                            for index, fila in resumen_granjas.iterrows():
                                granja = fila['Granja']
                                cantidad = fila['Cantidad']
                                viajes = math.ceil(cantidad / 200) 
                                total_viajes_global += viajes
                                st.write(f"📍 **{granja}**: {cantidad} cajas → Requiere **{viajes}** viajes.")
                        
                        with col_metric:
                            st.metric("Total Camiones Necesitados", total_viajes_global)
                        
                        st.markdown("---")
                        if num_carros_disp > 0:
                            if total_viajes_global > num_carros_disp:
                                st.error(f"⚠️ ¡ALERTA! Necesitas {total_viajes_global} carros pero tu maestra indica que solo tienes {num_carros_disp} tipo Huevo.")
                            else:
                                st.success(f"✅ ¡Flota suficiente! Tienes {num_carros_disp} carros tipo Huevo disponibles.")
                                st.balloons()
                                
                    except KeyError:
                        st.error("❌ El archivo subido no tiene las columnas 'Granja' o 'Cantidad'. Verifica el formato.")
        else:
            # Si no ha subido el archivo, le avisamos
            st.warning("⚠️ Aún no has cargado los pedidos del día.")
            st.info("Por favor, ve a la sección **📦 Programar Despachos** en el menú y sube tu archivo de Excel primero.")

    # ==========================================
    # SECCIÓN: ALIMENTO Y POLLITO
    # ==========================================
    elif st.session_state['menu_actual'] == "Alimento":
        st.title("🌽 Programación de Rutas: ALIMENTO")
        if st.session_state['df_ventas'] is not None:
            st.info("🚧 Módulo de Alimento en construcción. Aquí aplicaremos las reglas de peso para camiones de estacas usando el archivo que ya subiste.")
        else:
            st.warning("⚠️ Primero debes subir el archivo de Excel en la sección **Programar Despachos**.")

    elif st.session_state['menu_actual'] == "Pollito":
        st.title("🐥 Programación de Rutas: POLLITO")
        if st.session_state['df_ventas'] is not None:
            st.info("🚧 Módulo de Pollito en construcción. Aquí aplicaremos las reglas exclusivas para camiones climatizados usando el archivo que ya subiste.")
        else:
            st.warning("⚠️ Primero debes subir el archivo de Excel en la sección **Programar Despachos**.")

    # ==========================================
    # SECCIÓN: BASES DE DATOS (MAESTRAS)
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
        
        if st.session_state['maestra_actual']:
            nombre_maestra = st.session_state['maestra_actual']
            nombre_archivo_exacto = ARCHIVOS_EXCEL[nombre_maestra]
            
            st.subheader(f"Editando: {nombre_maestra}")
            st.write("Doble clic en una celda para editar. Escribe en la última fila (+) para agregar. Selecciona la fila entera y presiona Suprimir para borrar.")
            
            try:
                df = pd.read_excel(nombre_archivo_exacto)
                df_editado = st.data_editor(
                    df, num_rows="dynamic", use_container_width=True, key=f"editor_{nombre_maestra}" 
                )
                
                if st.button(f"💾 Guardar cambios en {nombre_maestra}"):
                    df_editado.to_excel(nombre_archivo_exacto, index=False)
                    st.success(f"¡Base de datos '{nombre_archivo_exacto}' actualizada permanentemente!")
                    
            except FileNotFoundError:
                st.error(f"Error: El archivo '{nombre_archivo_exacto}' no se encontró.")
                st.info("Asegúrate de haber subido el archivo con ese nombre exacto a tu repositorio de GitHub.")
