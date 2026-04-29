import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Motor Logístico Sanma - LIVE", layout="wide")

ARCHIVO_MAESTRA = "Maestras sanma.xlsx"

# ==========================================
# 1. CARGA AUTOMÁTICA DE DATOS (LECTURA REAL)
# ==========================================
@st.cache_data 
def cargar_datos_reales():
    if os.path.exists(ARCHIVO_MAESTRA):
        # Usando TUS nombres exactos de pestañas
        df_v = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Vehiculos')
        df_c = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Conductores')
        df_n = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Nodos')
        return df_v, df_c, df_n
    else:
        st.error(f"❌ No encontré '{ARCHIVO_MAESTRA}' en GitHub.")
        return None, None, None

df_vehiculos, df_conductores, df_nodos = cargar_datos_reales()

JERARQUIA = {'MULTIPLE': 5, 'DOBLE': 4, 'SENCILLO': 3, 'TURBO': 2, 'SEMITURBO': 1}

# ==========================================
# 2. INICIALIZAR LA SEMANA
# ==========================================
if 'df_semana' not in st.session_state:
    rutas_fijas = ['Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 'Villa Johana/La Maria San Gil']
    placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154']
    cond_fijos = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS HERNANDO', 'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO']
    
    rutas_vacias = ['Juan Curi San Gil', 'Miralindo San Gil', 'Dos Hilachas San Gil', 'La Esperanza', 'Costa Rica/Costa Rica', 'La Esmeralda San gil', 'San German', 'Flandes']
    
    fecha_inicio = pd.to_datetime('2026-05-04')
    filas = []
    
    for i in range(7):
        fecha = (fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y')
        dia_nombre = (fecha_inicio + timedelta(days=i)).weekday() 

        for j, ruta in enumerate(rutas_fijas):
            filas.append({'Bloquear': False, 'Hora': '7:00 AM' if j==0 else '2:00 PM', 'Conductor': cond_fijos[j], 'Placa': placas_fijas[j], 'Ruta': ruta, 'Fecha': fecha, 'Intento': 1})
        
        for ruta in rutas_vacias:
            if 'Flandes' in ruta and dia_nombre not in [2, 5]: continue 
            filas.append({'Bloquear': False, 'Hora': '2:00 PM', 'Conductor': '', 'Placa': '', 'Ruta': ruta, 'Fecha': fecha, 'Intento': 1})

    st.session_state.df_semana = pd.DataFrame(filas)

# ==========================================
# 3. MOTOR DE ASIGNACIÓN (DATOS REALES)
# ==========================================
def programar_motor():
    if df_vehiculos is None or df_nodos is None: return
    
    df = st.session_state.df_semana.copy()
    fechas = df['Fecha'].unique()
    pendientes_mañana = []

    for fecha in fechas:
        # Rollover a la mañana siguiente
        for p in pendientes_mañana:
            n = p.copy(); n['Fecha'] = fecha; n['Hora'] = '7:00 AM'
            df = pd.concat([df, pd.DataFrame([n])], ignore_index=True)
        pendientes_mañana = []

        mask = (df['Fecha'] == fecha) & (df['Bloquear'] == False) & (df['Conductor'] == '')
        
        for idx, row in df[mask].iterrows():
            ocupados = df[(df['Fecha'] == fecha) & (df['Hora'] == row['Hora'])]
            placas_out = ocupados['Placa'].tolist()
            cond_out = ocupados['Conductor'].tolist()
            
            asignado = False
            
            # Buscar el permiso de la granja (TUS COLUMNAS: Nombre_Nodo y Vehiculos_Permitidos)
            permiso_granja = 'SEMITURBO' # Por defecto si no la encuentra
            nodo_info = df_nodos[df_nodos['Nombre_Nodo'].str.contains(row['Ruta'], case=False, na=False)]
            if not nodo_info.empty:
                permiso_granja = str(nodo_info.iloc[0]['Vehiculos_Permitidos']).strip().upper()

            # Iterar sobre tu tabla de vehículos real
            for i_v, v in df_vehiculos.iterrows():
                # TUS COLUMNAS: Placa, Tipo_Vehiculo, Titular_Vehiculo
                p = str(v['Placa']).strip()
                tipo_v = str(v['Tipo_Vehiculo']).strip().upper()
                titular = str(v['Titular_Vehiculo']).strip()

                if p in placas_out: continue # Bloqueo por mismo turno
                
                # Validar jerarquía física
                jerarquia_v = JERARQUIA.get(tipo_v, 1)
                jerarquia_n = JERARQUIA.get(permiso_granja, 1)
                if jerarquia_v > jerarquia_n: continue 
                
                # Validar exclusivas
                if 'Dos Hilachas' in row['Ruta'] and p != 'LWY708': continue
                if 'La Esperanza' in row['Ruta'] and p != 'LPK555': continue

                # Asignar si el conductor titular no está ocupado en ese mismo turno
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
# 4. INTERFAZ EXACTA
# ==========================================
st.title("🥚 Programador Sanma (Base GitHub)")

dia = st.selectbox("Día:", st.session_state.df_semana['Fecha'].unique())
df_vista = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia]

# ORDEN ESTRICTO FINAL
columnas = ['Bloquear', 'Hora', 'Conductor', 'Placa', 'Ruta']

edited = st.data_editor(df_vista[columnas], hide_index=True, use_container_width=True, key="ed_v1")

if st.button("🚀 PROGRAMAR CON DATOS REALES"):
    st.session_state.df_semana.update(edited) 
    programar_motor()
    st.rerun()
