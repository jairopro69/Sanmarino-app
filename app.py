import streamlit as st
import base64
import pandas as pd
import time
import math

# 1. Configuración de la página
st.set_page_config(page_title="San Marino Logística", layout="wide")

# 2. SISTEMA DE MEMORIA
if 'logeado' not in st.session_state:
    st.session_state['logeado'] = False
if 'menu_actual' not in st.session_state:
    st.session_state['menu_actual'] = "Despachos"

# Nombres de tus archivos según la foto
ARCHIVOS_EXCEL = {
    "Conductores": "Conductores Sanmarino.xlsx", 
    "Carros": "Carros sanmarino.xlsx",
    "Granjas": "Granjas sanmarino.xlsx"
}

# --- FUNCIÓN DE FONDO ---
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f: return base64.b64encode(f.read()).decode()
    except: return ""

bg_base64 = get_base64("imagen fondo 1.avif")

# ==========================================
# LOGIN (Resumido para ahorrar espacio)
# ==========================================
if not st.session_state['logeado']:
    # ... (Tu código de login anterior se mantiene igual aquí) ...
    st.session_state['logeado'] = True # Solo para prueba rápida

# ==========================================
# PANEL INTERNO
# ==========================================
else:
    # --- MENÚ LATERAL ---
    st.sidebar.title("San Marino")
    if st.sidebar.button("📦 Despachos"): st.session_state['menu_actual'] = "Despachos"
    if st.sidebar.button("📁 Maestras"): st.session_state['menu_actual'] = "Maestras"
    if st.sidebar.button("Cerrar Sesión"): st.session_state.clear(); st.rerun()

    if st.session_state['menu_actual'] == "Despachos":
        st.title("📦 Programación de Despachos")
        
        archivo_ventas = st.file_uploader("Sube el Excel de Ventas", type=["xlsx"])
        
        if archivo_ventas:
            # Leemos el archivo que subiste
            df_ventas = pd.read_excel(archivo_ventas)
            st.success("✅ Excel de Ventas cargado.")
            
            # --- EL MOTOR LOGÍSTICO (CÁLCULO REAL) ---
            if st.button("🚀 Calcular Programación (Regla 200 cajas/Carro Huevo)"):
                with st.spinner('Aplicando reglas de San Marino...'):
                    # 1. Filtrar carros que son de Huevo en tu base de datos
                    try:
                        df_carros = pd.read_excel(ARCHIVOS_EXCEL["Carros"])
                        # Suponiendo que la columna se llama 'Tipo'
                        carros_huevo = df_carros[df_carros['Tipo'].str.contains('Huevo', case=False, na=False)]
                        num_carros_disp = len(carros_huevo)
                    except:
                        st.error("Falta el archivo 'Carros sanmarino.xlsx' para validar flota.")
                        num_carros_disp = 10 # Backup por si no está el archivo

                    # 2. Agrupar cajas por granja desde el Excel de ventas
                    # Según tu foto, la columna es 'Granja' y 'Cantidad'
                    resumen_granjas = df_ventas.groupby('Granja')['Cantidad'].sum().reset_index()
                    
                    st.subheader("📋 Resumen de Recolección")
                    
                    total_viajes = 0
                    for index, fila in resumen_granjas.iterrows():
                        granja = fila['Granja']
                        cantidad = fila['Cantidad']
                        # REGLA: Cada carro lleva 200
                        viajes_necesarios = math.ceil(cantidad / 200)
                        total_viajes += viajes_necesarios
                        
                        st.write(f"📍 **{granja}**: {cantidad} cajas total → Requiere **{viajes_necesarios}** viajes de furgón.")
                    
                    st.markdown("---")
                    st.metric("Total Carros Huevo Necesitados", total_viajes)
                    
                    if total_viajes > num_carros_disp:
                        st.error(f"⚠️ ¡ALERTA! Necesitas {total_viajes} carros pero solo tienes {num_carros_disp} de tipo Huevo disponibles.")
                    else:
                        st.success(f"✅ Flota suficiente. Los {total_viajes} despachos pueden ser cubiertos por los carros de huevo.")

    elif st.session_state['menu_actual'] == "Maestras":
        st.title("📁 Bases de Datos")
        # ... (Aquí va tu código de st.data_editor que ya tenemos listo) ...
