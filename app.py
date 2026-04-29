import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Programador Logístico", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Diaria - Huevo")

# ==========================================
# 1. PLANTILLA EXACTA (SEGÚN TU IMAGEN)
# ==========================================
# El orden exacto de las rutas de tu captura
rutas_base = [
    'Girón Mesitas', 
    'Giron Caciquito', 
    'San Roque San Gil', 
    'Rey David San Gil', 
    'Villa Johana/La Maria San Gil',
    'Juan Curi San Gil',
    'Miralindo San Gil',
    'Dos Hilachas San Gil',
    'La Esperanza',
    'Costa Rica/Costa Rica',
    'La Esmeralda San gil',
    'San German'
]

# Las placas ya pre-asignadas por tus reglas (el resto en blanco)
placas_base = [
    'UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154', 
    '', '', 'LWY708', 'LPK555', 'XMA049', 'XVV085', ''
]

# Los conductores pre-asignados solo a los 5 primeros
conductores_base = [
    'ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS HERNANDO', 
    'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO', 
    '', '', '', '', '', '', ''
]

horas_base = [
    '7:00 AM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM',
    '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM'
]

# Configuración de fechas
fecha_inicio = pd.to_datetime('2026-05-04')
dias_semana = [(fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
nombres_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def generar_plantilla_dia():
    """Genera el DataFrame exactamente como la imagen que enviaste"""
    df = pd.DataFrame({
        '🚫 Bloquear': [False] * len(rutas_base),
        'Hora': horas_base,
        'Conductor': conductores_base,
        'Placa': placas_base,
        'Ruta/Cliente': rutas_base
    })
    return df

# ==========================================
# 2. INTERFAZ GRÁFICA (TABS POR DÍA)
# ==========================================
st.markdown("### Selecciona el día a programar:")

tabs = st.tabs([f"{nombres_dias[i].capitalize()}" for i in range(7)])
viajes_por_dia = {}

for i, tab in enumerate(tabs):
    with tab:
        fecha_actual = dias_semana[i]
        
        st.markdown(f"#### Plantilla de rutas para el **{nombres_dias[i]}, {fecha_actual}**")
        st.info("💡 Haz clic en la casilla **'🚫 Bloquear'** para cancelar una ruta hoy. Al darle 'Programar', el motor llenará los espacios vacíos.")
        
        df_dia = generar_plantilla_dia()
        
        # Editor interactivo visualmente idéntico a tu Excel
        viajes_editados = st.data_editor(
            df_dia,
            column_config={
                "🚫 Bloquear": st.column_config.CheckboxColumn("🚫 Bloquear", width="small"),
                "Hora": st.column_config.TextColumn("Hora", disabled=True),
                "Conductor": st.column_config.TextColumn("Conductor"),
                "Placa": st.column_config.TextColumn("Placa"),
                "Ruta/Cliente": st.column_config.TextColumn("Ruta/Cliente", disabled=True)
            },
            hide_index=True,
            use_container_width=True,
            key=f"editor_dia_{i}"
        )
        
        # Guardamos en el diccionario agregándole la fecha por detrás para cuando consolidemos
        viajes_editados['Fecha'] = fecha_actual
        viajes_por_dia[fecha_actual] = viajes_editados

# ==========================================
# 3. BOTÓN DE EJECUCIÓN DEL MOTOR IA
# ==========================================
st.markdown("---")
if st.button("🚀 PROGRAMAR VIAJES (LLENAR VACÍOS)", type="primary", use_container_width=True):
    
    lista_df_activos = []
    
    for fecha, df in viajes_por_dia.items():
        # Quitamos los que marcaste con el chulo de bloquear
        df_activo = df[df['🚫 Bloquear'] != True].copy()
        lista_df_activos.append(df_activo)
        
    df_consolidado = pd.concat(lista_df_activos, ignore_index=True)
    
    st.success("✅ ¡Recibido! Python está buscando los mejores conductores para los carros fijos y asignando carros a las rutas vacías...")
    
    # ---------------------------------------------------------
    # AQUÍ ENTRARÁ EL CÓDIGO DE ASIGNACIÓN AUTOMÁTICA
    # (Donde Python llena los huecos de la columna Conductor y Placa)
    # ---------------------------------------------------------
    
    # Mostramos la tabla limpia para exportar
    df_exportar = df_consolidado.drop(columns=['🚫 Bloquear'])
    
    st.write("### 🏁 Resumen a Programar:")
    st.dataframe(df_exportar, hide_index=True, use_container_width=True)
