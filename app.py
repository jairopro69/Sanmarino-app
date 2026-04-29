import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Programador Logístico", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Diaria - Huevo")

# ==========================================
# 1. GENERACIÓN DEL FORMATO DIARIO (SOLO FIJOS)
# ==========================================
# Estos son los ÚNICOS 5 viajes que salen todos los días sin falta
rutas_fijas = [
    'Girón Mesitas', 
    'Giron Caciquito', 
    'San Roque San Gil', 
    'Rey David San Gil', 
    'Villa Johana/La Maria San Gil'
]

conductores_fijos = [
    'ISAIAS MARTINEZ SOLANO',
    'ISAIAS MARTINEZ SOLANO',
    'MENESES SEPULVEDA LUIS HERNANDO',
    'RINCON RODRIGUEZ SEBASTIAN',
    'VARGAS CIRO ALFONSO'
]

placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154']
horas_fijas = ['7:00 AM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM']

# Configuración de fechas
fecha_inicio = pd.to_datetime('2026-05-04')
dias_semana = [(fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
nombres_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def generar_plantilla_dia(fecha_str):
    """Crea la tabla SOLO con los 5 fijos y deja 10 filas vacías para que Python programe el resto"""
    # Creamos 15 filas en total (5 fijas + 10 vacías)
    total_filas = 15
    df = pd.DataFrame(index=range(total_filas))
    
    df['🚫 Bloquear'] = False # Con un solo clic aquí, el viaje se cancela
    df['Planta/Granja'] = ""
    df['Fecha'] = fecha_str
    
    # Llenamos los 5 fijos
    df['Hora'] = ""
    df.loc[0:4, 'Hora'] = horas_fijas
    
    df['Conductor'] = ""
    df.loc[0:4, 'Conductor'] = conductores_fijos
    
    df['Placa'] = ""
    df.loc[0:4, 'Placa'] = placas_fijas
    
    df['Ruta/Cliente'] = ""
    df.loc[0:4, 'Ruta/Cliente'] = rutas_fijas
    
    df['Granja'] = ""
    df['Cant'] = ""
    
    return df

# ==========================================
# 2. INTERFAZ GRÁFICA (TABS POR DÍA)
# ==========================================
st.markdown("### Selecciona el día a programar:")

tabs = st.tabs([f"{nombres_dias[i].capitalize()}, {dias_semana[i]}" for i in range(7)])
viajes_por_dia = {}

for i, tab in enumerate(tabs):
    with tab:
        fecha_actual = dias_semana[i]
        
        st.markdown(f"#### Programación base para el **{nombres_dias[i]}, {fecha_actual}**")
        st.info("💡 Solo se muestran los 5 viajes fijos diarios. Haz clic en la casilla **'🚫 Bloquear'** si alguno de estos 5 no sale hoy. El resto de las rutas serán asignadas por el motor en los espacios en blanco.")
        
        df_dia = generar_plantilla_dia(fecha_actual)
        
        # Editor de datos
        viajes_editados = st.data_editor(
            df_dia,
            column_config={
                "🚫 Bloquear": st.column_config.CheckboxColumn("🚫 Bloquear", default=False, width="small"),
                "Planta/Granja": st.column_config.TextColumn("Planta/Granja"),
                "Fecha": st.column_config.TextColumn("Fecha", disabled=True),
                "Hora": st.column_config.SelectboxColumn("Hora", options=["7:00 AM", "10:00 AM", "2:00 PM"]),
                "Conductor": st.column_config.TextColumn("Conductor"),
                "Placa": st.column_config.TextColumn("Placa"),
                "Ruta/Cliente": st.column_config.TextColumn("Ruta/Cliente"),
                "Granja": st.column_config.TextColumn("Granja"),
                "Cant": st.column_config.TextColumn("Cant")
            },
            hide_index=True,
            use_container_width=True,
            num_rows="dynamic",
            key=f"editor_dia_{i}"
        )
        
        viajes_por_dia[fecha_actual] = viajes_editados

# ==========================================
# 3. BOTÓN DE CONSOLIDACIÓN Y EJECUCIÓN DEL MOTOR
# ==========================================
st.markdown("---")
if st.button("🚀 PROGRAMAR RESTO DE VIAJES (MOTOR IA)", type="primary", use_container_width=True):
    
    lista_df_activos = []
    
    for fecha, df in viajes_por_dia.items():
        # Filtramos los que el usuario NO bloqueó y los que NO están totalmente vacíos
        df_activo = df[df['🚫 Bloquear'] != True].copy()
        df_activo = df_activo.dropna(subset=['Ruta/Cliente']) # Quitamos filas nulas
        df_activo = df_activo[df_activo['Ruta/Cliente'] != ""] # Quitamos filas vacías
        lista_df_activos.append(df_activo)
        
    df_consolidado = pd.concat(lista_df_activos, ignore_index=True)
    
    st.success("✅ Viajes fijos aprobados. ¡Despertando a Python para calcular las rutas faltantes (Flandes, Dos Hilachas, etc.)!")
    
    # ---------------------------------------------------------
    # AQUÍ ENTRARÁ EL CÓDIGO DE ASIGNACIÓN AUTOMÁTICA DE PYTHON
    # (El cruce con las Maestras, las 112 horas, exclusividad)
    # ---------------------------------------------------------
    
    # Mostramos la tabla para exportar (Por ahora solo los fijos aprobados)
    df_exportar = df_consolidado.drop(columns=['🚫 Bloquear'])
    
    st.write("### 🏁 Resumen Parcial (Fijos):")
    st.dataframe(df_exportar, hide_index=True, use_container_width=True)
    
    csv = df_exportar.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Programación",
        data=csv,
        file_name='Programacion_Semanal.csv',
        mime='text/csv',
    )
