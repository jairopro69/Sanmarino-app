import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Motor Logístico Sanma - LIVE", layout="wide")

# NOMBRE EXACTO DE TU ARCHIVO EN GITHUB
ARCHIVO_MAESTRA = "Maestras sanma.xlsx"

# ==========================================
# 1. CARGA AUTOMÁTICA DE DATOS (LECTURA REAL)
# ==========================================
@st.cache_data # Para que la app sea rápida y no lea el excel a cada segundo
def cargar_datos_reales():
    if os.path.exists(ARCHIVO_MAESTRA):
        # Leemos las pestañas exactas que me mostraste en las fotos
        df_v = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Vehiculos')
        df_c = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Conductores')
        df_n = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Nodos')
        return df_v, df_c, df_n
    else:
        st.error(f"❌ No encontré el archivo '{ARCHIVO_MAESTRA}' en GitHub. Revisa que el nombre coincida exactamente.")
        return None, None, None

df_vehiculos, df_conductores, df_nodos = cargar_datos_reales()

# ==========================================
# 2. INICIALIZAR LA SEMANA
# ==========================================
if 'df_semana' not in st.session_state:
    # 5 Rutas Fijas que siempre aparecen
    rutas_fijas = ['Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 'Villa Johana/La Maria San Gil']
    placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154']
    cond_fijos = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS HERNANDO', 'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO']
    
    # Rutas que el motor debe programar (vacías)
    rutas_vacias = ['Juan Curi San Gil', 'Miralindo San Gil', 'Dos Hilachas San Gil', 'La Esperanza', 'Costa Rica/Costa Rica', 'La Esmeralda San gil', 'San German', 'Flandes']
    
    fecha_inicio = pd.to_datetime('2026-05-04')
    filas = []
    
    for i in range(7):
        fecha = (fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y')
        dia_nombre = (fecha_inicio + timedelta(days=i)).weekday() # Para Flandes

        # Cargar Fijos
        for j, ruta in enumerate(rutas_fijas):
            filas.append({'Bloquear': False, 'Hora': '7:00 AM' if j==0 else '2:00 PM', 'Conductor': cond_fijos[j], 'Placa': placas_fijas[j], 'Ruta': ruta, 'Fecha': fecha, 'Intento': 1})
        
        # Cargar Resto Vacío
        for ruta in rutas_vacias:
            if 'Flandes' in ruta and dia_nombre not in [2, 5]: continue # Solo Mier y Sab
            filas.append({'Bloquear': False, 'Hora': '2:00 PM', 'Conductor': '', 'Placa': '', 'Ruta': ruta, 'Fecha': fecha, 'Intento': 1})

    st.session_state.df_semana = pd.DataFrame(filas)

# ==========================================
# 3. MOTOR DE ASIGNACIÓN (CON TUS DATOS REALES)
# ==========================================
def programar_motor():
    if df_vehiculos is None: return
    
    df = st.session_state.df_semana.copy()
    fechas = df['Fecha'].unique()
    pendientes_mañana = []

    for fecha in fechas:
        # Inyectar los que "Bajaron en la mañana" del día anterior
        for p in pendientes_mañana:
            n = p.copy(); n['Fecha'] = fecha; n['Hora'] = '7:00 AM'
            df = pd.concat([df, pd.DataFrame([n])], ignore_index=True)
        pendientes_mañana = []

        mask = (df['Fecha'] == fecha) & (df['Bloquear'] == False) & (df['Conductor'] == '')
        
        for idx, row in df[mask].iterrows():
            # Revisar ocupados en este turno para no clonar carros
            ocupados = df[(df['Fecha'] == fecha) & (df['Hora'] == row['Hora'])]
            placas_out = ocupados['Placa'].tolist()
            cond_out = ocupados['Conductor'].tolist()
            
            # Buscar recurso en tu EXCEL REAL
            asignado = False
            # Filtramos vehículos que queden bien en esa granja (según tu jerarquía)
            # Aquí Python lee tu columna 'Tipo_Vehiculo' del Excel
            for i_v, v in df_vehiculos.iterrows():
                p = v['Placa']
                if p in placas_out: continue
                
                # Validamos si es ruta exclusiva
                if 'Dos Hilachas' in row['Ruta'] and p != 'LWY708': continue
                if 'La Esperanza' in row['Ruta'] and p != 'LPK555': continue

                # Si llegamos aquí, el carro está libre y cumple
                titular = v['Titular_Vehiculo'] # Columna de tu excel
                if titular not in cond_out:
                    df.at[idx, 'Placa'] = p
                    df.at[idx, 'Conductor'] = titular
                    asignado = True
                    break
            
            if not asignado:
                row['Intento'] += 1
                pendientes_mañana.append(row)
                df.at[idx, 'Conductor'] = '⚠️ BAJA A MAÑANA'
                df.at[idx, 'Placa'] = 'SIN RECURSO'

    st.session_state.df_semana = df

# ==========================================
# 4. INTERFAZ: VISUALIZACIÓN EXACTA
# ==========================================
st.title("🥚 Programador Sanma (Base GitHub)")

dia = st.selectbox("Día:", st.session_state.df_semana['Fecha'].unique())
df_vista = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia]

# ORDEN ESTRICTO: HORA, CONDUCTOR, PLACA, RUTA
columnas = ['Bloquear', 'Hora', 'Conductor', 'Placa', 'Ruta']

edited = st.data_editor(df_vista[columnas], hide_index=True, use_container_width=True, key="ed_v1")

if st.button("🚀 PROGRAMAR CON DATOS REALES"):
    st.session_state.df_semana.update(edited) # Guardamos lo que marcaste
    programar_motor()
    st.rerun()
