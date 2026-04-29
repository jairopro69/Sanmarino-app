import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE PÁGINA Y CONSTANTES
# ==========================================
st.set_page_config(page_title="Motor Logístico Sanma - ROBUSTO", layout="wide")

ARCHIVO_MAESTRA = "Maestras sanma.xlsx"
JERARQUIA = {'MULTIPLE': 5, 'DOBLE': 4, 'SENCILLO': 3, 'TURBO': 2, 'SEMITURBO': 1}

# ==========================================
# 1. CARGA INTELIGENTE Y FILTRADO ESTRICTO (LA IA PENSANDO)
# ==========================================
@st.cache_data 
def cargar_y_limpiar_datos():
    if not os.path.exists(ARCHIVO_MAESTRA):
        st.error(f"❌ [CRÍTICO] No se encontró '{ARCHIVO_MAESTRA}' en el repositorio de GitHub.")
        return None, None, None

    try:
        # 1. Leer las hojas
        df_v = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Vehiculos')
        df_c = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Conductores')
        df_n = pd.read_excel(ARCHIVO_MAESTRA, sheet_name='Maestra_Nodos')

        # 2. Limpieza robusta: Quitar espacios ocultos en los nombres de las columnas
        df_v.columns = df_v.columns.str.strip()
        df_c.columns = df_c.columns.str.strip()
        df_n.columns = df_n.columns.str.strip()

        # 3. EL FILTRO DE ORO: EXCLUSIVO LÍNEA HUEVO
        # Buscamos la columna de linea de operacion, sin importar si está en mayúscula o minúscula
        col_linea_v = [c for c in df_v.columns if 'LINEA' in c.upper() and 'OPERACION' in c.upper()]
        if col_linea_v:
            # Filtramos estrictamente los que digan "Huevo"
            df_v = df_v[df_v[col_linea_v[0]].astype(str).str.upper().str.contains('HUEVO', na=False)]
        else:
            st.warning("⚠️ No se encontró la columna 'Linea_operacion' en Vehículos. Se usará toda la flota.")

        # Hacemos lo mismo con los conductores si tienen línea de operación
        col_linea_c = [c for c in df_c.columns if 'LINEA' in c.upper() and 'OPERACION' in c.upper()]
        if col_linea_c:
            df_c = df_c[df_c[col_linea_c[0]].astype(str).str.upper().str.contains('HUEVO', na=False)]

        return df_v, df_c, df_n

    except Exception as e:
        st.error(f"❌ [ERROR DE LECTURA] El archivo está corrupto o le faltan pestañas. Detalles: {e}")
        return None, None, None

# Ejecutamos la carga segura
df_vehiculos, df_conductores, df_nodos = cargar_y_limpiar_datos()

# ==========================================
# 2. INICIALIZAR LA ESTRUCTURA DE LA SEMANA
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
# 3. MOTOR DE ASIGNACIÓN (ALTO RENDIMIENTO)
# ==========================================
def programar_motor_robusto():
    if df_vehiculos is None or df_vehiculos.empty:
        st.error("❌ No hay vehículos disponibles en la Línea Huevo para programar.")
        return
    
    df = st.session_state.df_semana.copy()
    fechas = df['Fecha'].unique()
    pendientes_mañana = []

    for fecha in fechas:
        # 3.1. REGLA: ROLLOVER (Pasar viajes fallidos a las 7:00 AM del día siguiente)
        for p in pendientes_mañana:
            n = p.copy()
            n['Fecha'] = fecha
            n['Hora'] = '7:00 AM'
            df = pd.concat([df, pd.DataFrame([n])], ignore_index=True)
        pendientes_mañana = []

        mask = (df['Fecha'] == fecha) & (df['Bloquear'] == False) & (df['Conductor'] == '')
        
        for idx, row in df[mask].iterrows():
            # 3.2. REGLA: BLOQUEO DE TURNOS SIMULTÁNEOS
            ocupados = df[(df['Fecha'] == fecha) & (df['Hora'] == row['Hora'])]
            placas_out = ocupados['Placa'].dropna().tolist()
            cond_out = ocupados['Conductor'].dropna().tolist()
            
            asignado = False
            
            # 3.3. REGLA: JERARQUÍA FÍSICA Y NODOS
            permiso_granja = 'SEMITURBO' # Nodo más restrictivo por seguridad
            if df_nodos is not None:
                # Búsqueda flexible de la granja (ignora mayúsculas)
                nodo_match = df_nodos[df_nodos['Nombre_Nodo'].astype(str).str.upper().str.contains(row['Ruta'].upper(), na=False)]
                if not nodo_match.empty:
                    permiso_granja = str(nodo_match.iloc[0]['Vehiculos_Permitidos']).strip().upper()

            jerarquia_n = JERARQUIA.get(permiso_granja, 1)

            # 3.4. RECORRIDO DE FLOTA EXCLUSIVA DE HUEVO
            for i_v, v in df_vehiculos.iterrows():
                p = str(v.get('Placa', '')).strip()
                tipo_v = str(v.get('Tipo_Vehiculo', '')).strip().upper()
                titular = str(v.get('Titular_Vehiculo', '')).strip()

                if p == '' or p in placas_out: 
                    continue # Salta si no hay placa o ya está ocupado en esta hora
                
                # Evaluación Jerarquía
                jerarquia_v = JERARQUIA.get(tipo_v, 1)
                if jerarquia_v > jerarquia_n: 
                    continue # El camión es muy grande
                
                # 3.5. REGLAS DE EXCLUSIVIDAD DE RUTAS
                if 'Dos Hilachas' in row['Ruta'] and p != 'LWY708': continue
                if 'La Esperanza' in row['Ruta'] and p != 'LPK555': continue
                if 'Costa Rica' in row['Ruta'] and p != 'XMA049': continue
                if 'La Esmeralda' in row['Ruta'] and p != 'XVV085': continue

                # 3.6. ASIGNACIÓN EXITOSA
                if titular not in cond_out:
                    df.at[idx, 'Placa'] = p
                    df.at[idx, 'Conductor'] = titular
                    asignado = True
                    break # Salimos del bucle de vehículos, ya encontramos uno
            
            # 3.7. MANEJO DE FALLOS (SIN RECURSOS)
            if not asignado:
                row['Intento'] += 1
                pendientes_mañana.append(row)
                df.at[idx, 'Conductor'] = '⚠️ BAJA A MAÑANA'
                df.at[idx, 'Placa'] = '⚠️ SIN CARRO HUEVO'

    st.session_state.df_semana = df

# ==========================================
# 4. INTERFAZ GRÁFICA ESTRICTA
# ==========================================
st.title("🥚 Motor Logístico Sanma - Enterprise")

# Métricas rápidas para confirmar que el filtro funcionó
if df_vehiculos is not None:
    st.success(f"✅ Inteligencia Activada: Se filtraron {len(df_vehiculos)} vehículos exclusivos de la línea HUEVO.")

dia = st.selectbox("📅 Selecciona el día a visualizar:", st.session_state.df_semana['Fecha'].unique())
df_vista = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia]

# ORDEN ESTRICTO E INMUTABLE
columnas = ['Bloquear', 'Hora', 'Conductor', 'Placa', 'Ruta']

edited = st.data_editor(df_vista[columnas], hide_index=True, use_container_width=True, key="ed_robusto")

if st.button("🚀 INICIAR MOTOR Y CALCULAR RUTAS"):
    with st.spinner("Procesando millones de condicionales..."):
        st.session_state.df_semana.update(edited) 
        programar_motor_robusto()
    st.rerun()
