import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================
st.set_page_config(page_title="Planificador Logístico Sanma", layout="wide")

# Inicializamos el estado de la aplicación para que los datos persistan
if 'df_semana' not in st.session_state:
    # Definición de rutas base
    rutas_base = [
        'Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 
        'Villa Johana/La Maria San Gil', 'Juan Curi San Gil', 'Miralindo San Gil', 
        'Dos Hilachas San Gil', 'La Esperanza', 'Costa Rica/Costa Rica', 
        'La Esmeralda San gil', 'San German'
    ]
    
    # Placas y Conductores Fijos (Solo los 5 que mandaste)
    placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154', '', '', 'LWY708', 'LPK555', 'XMA049', 'XVV085', '']
    cond_fijos = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS HERNANDO', 'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO', '', '', '', '', '', '', '']
    
    fecha_inicio = pd.to_datetime('2026-05-04')
    filas_totales = []
    
    for i in range(7):
        fecha = (fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y')
        for j, ruta in enumerate(rutas_base):
            filas_totales.append({
                'Bloquear': False,
                'Fecha': fecha,
                'Hora': '7:00 AM' if ruta == 'Girón Mesitas' else '2:00 PM',
                'Ruta/Cliente': ruta,
                'Conductor': cond_fijos[j],
                'Placa': placas_fijas[j],
                'Estado': 'Pendiente'
            })
    st.session_state.df_semana = pd.DataFrame(filas_totales)

st.title("🚚 Sistema de Programación Logística - Sanma")
st.info("Regla: Los viajes no asignados hoy pasan a las 7:00 AM del día siguiente.")

# ==========================================
# MOTOR DE LÓGICA (EL CEREBRO)
# ==========================================
def ejecutar_programacion():
    df = st.session_state.df_semana.copy()
    
    # Listas de recursos (Simulación basada en tus reglas)
    # Aquí es donde el motor decidirá si "alcanzan los carros"
    carros_disponibles = ['UPR329', 'WNN709', 'SXT043', 'TRL154', 'LWY708', 'LPK555', 'XMA049', 'XVV085']
    conductores_disponibles = ['ISAIAS MARTINEZ', 'MENESES SEPULVEDA', 'RINCON RODRIGUEZ', 'VARGAS CIRO']

    # Procesar día por día para el Rollover
    fechas = df['Fecha'].unique()
    viajes_pendientes_manana = []

    for idx_fecha, fecha in enumerate(fechas):
        # 1. Agregar pendientes del día anterior a las 7:00 AM
        for pendiente in viajes_pendientes_manana:
            nuevo_viaje = pendiente.copy()
            nuevo_viaje['Fecha'] = fecha
            nuevo_viaje['Hora'] = '7:00 AM'
            nuevo_viaje['Estado'] = 'Reprogramado (Mañana)'
            df = pd.concat([df, pd.DataFrame([nuevo_viaje])], ignore_index=True)
        
        viajes_pendientes_manana = [] # Limpiar para el día actual

        # 2. Intentar asignar los vacíos de este día
        mask_dia = (df['Fecha'] == fecha) & (df['Bloquear'] == False)
        for index, row in df[mask_dia].iterrows():
            if row['Placa'] == '' or row['Conductor'] == '':
                # LÓGICA: ¿Hay recursos? (Simulación de escasez)
                # Si el índice es par, simulamos que NO hay carro para ver el Rollover
                if index % 5 == 0: 
                    df.at[index, 'Estado'] = 'PASADO A MAÑANA (Falta Recurso)'
                    viajes_pendientes_manana.append(row)
                else:
                    # Asignación según tus reglas de exclusividad
                    if 'Dos Hilachas' in row['Ruta/Cliente']:
                        df.at[index, 'Placa'] = 'LWY708'
                    elif 'La Esperanza' in row['Ruta/Cliente']:
                        df.at[index, 'Placa'] = 'LPK555'
                    
                    df.at[index, 'Conductor'] = 'ASIGNADO POR IA'
                    df.at[index, 'Estado'] = 'Programado'

    st.session_state.df_semana = df

# ==========================================
# INTERFAZ (MISMA TABLA)
# ==========================================
# Filtro por día para no saturar la vista
dia_ver = st.selectbox("Ver día:", st.session_state.df_semana['Fecha'].unique())

df_filtrado = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia_ver]

# EDITOR DE DATOS (AQUÍ APARECERÁ TODO)
edited_df = st.data_editor(
    df_filtrado,
    column_config={
        "Bloquear": st.column_config.CheckboxColumn("Bloquear"),
        "Estado": st.column_config.TextColumn("Estado", disabled=True),
    },
    hide_index=True,
    use_container_width=True,
    key="editor_semanal"
)

# Guardar cambios manuales antes de programar
if st.button("💾 Guardar Cambios Manuales"):
    # Actualizamos el dataframe principal con lo que el usuario editó en pantalla
    st.session_state.df_semana.update(edited_df)
    st.success("Cambios guardados.")

if st.button("🚀 PROGRAMAR Y REUBICAR FALTANTES", type="primary"):
    ejecutar_programacion()
    st.rerun() # Esto hace que la tabla se refresque con los resultados "AHÍ MISMO"

# Botón para descargar el resultado final
if st.button("📥 Descargar Plan de Trabajo"):
    csv = st.session_state.df_semana.to_csv(index=False).encode('utf-8')
    st.download_button("Click para descargar", csv, "logistica_sanma.csv", "text/csv")
