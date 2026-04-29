import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Programador Logístico", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Diaria - Huevo")

# ==========================================
# 1. DICCIONARIOS Y FUNCIONES
# ==========================================
# (Aquí mantendremos las reglas base que creamos antes para futuras validaciones)
JERARQUIA_ACCESO = {
    'MULTIPLE':  ['DOBLE', 'SENCILLO', 'TURBO', 'SEMITURBO'],
    'DOBLE':     ['DOBLE', 'SENCILLO', 'TURBO', 'SEMITURBO'],
    'SENCILLO':  ['SENCILLO', 'TURBO', 'SEMITURBO'],
    'TURBO':     ['TURBO', 'SEMITURBO'],
    'SEMITURBO': ['SEMITURBO']
}

RUTAS_EXCLUSIVAS = {
    'La Esperanza': 'LPK555',
    'Dos Hilachas': 'LWY708',
    'Costa Rica': 'XMA049', 
    'La Esmeralda': 'XVV085'
}

CARROS_FLANDES = ['LPM116', 'LWY708']

# ==========================================
# 2. GENERACIÓN DEL FORMATO DIARIO
# ==========================================
# Granjas base (delimitadas por tu imagen)
granjas_base = [
    'Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 
    'Villa Johana/La Maria San Gil', 'Juan Curi San Gil', 'Miralindo San Gil', 
    'Dos Hilachas San Gil', 'La Esperanza', 'Costa Rica/Costa Rica', 
    'La Esmeralda San gil', 'San German', 'SALIDA FLANDES HUEVO', 
    'Miralindo San Gil', 'San German'
]

# Configuración inicial de fechas (Desde hoy)
fecha_inicio = pd.to_datetime('2026-05-04') # Lunes 4 de Mayo de 2026
dias_semana = [(fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
nombres_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def generar_plantilla_dia(fecha_str):
    """Crea un DataFrame vacío con la estructura exacta de tu Excel"""
    df = pd.DataFrame(index=range(len(granjas_base)))
    df['Bloquear'] = False # Checkbox para uso en Streamlit
    df['Planta/Granja'] = ""
    df['Fecha'] = fecha_str
    
    # Asignación de horas por defecto (basado en tu imagen)
    horas = ['2:00 PM'] * len(granjas_base)
    horas[0] = '7:00 AM' # Girón Mesitas
    horas[12] = '10:00 AM' # Flandes (Aproximación según tu imagen)
    horas[13] = '7:00 AM' # Miralindo mañana
    horas[14] = '7:00 AM' # San German mañana
    df['Hora'] = horas
    
    # Valores sugeridos fijos (basado en tu imagen)
    df['Conductor'] = ""
    df['Placa'] = ""
    df['Ruta/Cliente'] = granjas_base
    df['Granja'] = ""
    df['Cant'] = ""
    
    # Asignaciones fijas sugeridas
    df.loc[0, ['Conductor', 'Placa']] = ['ISAIAS MARTINEZ SOLANO', 'UPR329']
    df.loc[1, ['Conductor', 'Placa']] = ['ISAIAS MARTINEZ SOLANO', 'UPR329']
    df.loc[2, ['Conductor', 'Placa']] = ['MENESES SEPULVEDA LUIS HERNANDO', 'WNN709']
    df.loc[3, ['Conductor', 'Placa']] = ['RINCON RODRIGUEZ SEBASTIAN', 'SXT043']
    df.loc[4, ['Conductor', 'Placa']] = ['VARGAS CIRO ALFONSO', 'TRL154']
    df.loc[7, ['Conductor', 'Placa']] = ['PEDRAZA MUÑOZ JORGE ELIECER', 'LWY708']
    df.loc[8, ['Conductor', 'Placa']] = ['CARDENAS URIBE SERGIO', 'LPK555']
    df.loc[9, ['Conductor', 'Placa']] = ['GOMEZ OSCAR', 'XMA049']
    df.loc[10, ['Conductor', 'Placa']] = ['VASQUEZ QUINTERO DAWIS', 'XVV085']
    df.loc[12, ['Conductor', 'Placa']] = ['GOMEZ HERRERA FERNANDO', 'LWY708']
    df.loc[13, ['Conductor', 'Placa']] = ['CARDENAS URIBE SERGIO', 'LPK555']
    df.loc[14, ['Conductor', 'Placa']] = ['VASQUEZ QUINTERO DAWIS', 'XVV085']
    
    return df

# ==========================================
# 3. INTERFAZ GRÁFICA (TABS POR DÍA)
# ==========================================
st.markdown("### Selecciona el día a programar:")

# Creamos pestañas (Tabs) para cada día de la semana
tabs = st.tabs([f"{nombres_dias[i].capitalize()}, {dias_semana[i]}" for i in range(7)])

# Diccionario para guardar las tablas editadas de cada día
viajes_por_dia = {}

for i, tab in enumerate(tabs):
    with tab:
        fecha_actual = dias_semana[i]
        nombre_dia = nombres_dias[i]
        
        st.markdown(f"#### Programación para el **{nombre_dia}, {fecha_actual}**")
        st.write("Marca **'🚫 Bloquear'** para los viajes que NO se enviarán. Edita Placa y Conductor haciendo doble clic.")
        
        # Generamos la plantilla para este día
        df_dia = generar_plantilla_dia(fecha_actual)
        
        # Editor interactivo
        viajes_editados = st.data_editor(
            df_dia,
            column_config={
                "Bloquear": st.column_config.CheckboxColumn("🚫 Bloquear", default=False, width="small"),
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
            num_rows="dynamic", # Permite agregar filas si es necesario
            key=f"editor_dia_{i}"
        )
        
        # Guardamos la tabla editada de este día
        viajes_por_dia[fecha_actual] = viajes_editados

# ==========================================
# 4. BOTÓN DE CONSOLIDACIÓN Y EXPORTACIÓN
# ==========================================
st.markdown("---")
if st.button("🚀 CONSOLIDAR Y VALIDAR SEMANA", type="primary", use_container_width=True):
    
    # 1. Unimos todos los días en una sola tabla, filtrando los bloqueados
    lista_df_activos = []
    for fecha, df in viajes_por_dia.items():
        df_activo = df[df['Bloquear'] != True].copy()
        lista_df_activos.append(df_activo)
        
    df_consolidado = pd.concat(lista_df_activos, ignore_index=True)
    
    if df_consolidado.empty:
        st.warning("⚠️ Todos los viajes de la semana están bloqueados.")
    else:
        st.success(f"✅ Semana consolidada: {len(df_consolidado)} viajes a programar.")
        
        # (Aquí iría la lógica del motor para validar exclusividades)
        # Por ahora, mostramos la tabla final limpia para exportar
        df_exportar = df_consolidado.drop(columns=['Bloquear'])
        
        st.write("### 🏁 Resumen Semanal:")
        st.dataframe(df_exportar, hide_index=True, use_container_width=True)
        
        # Exportación
        csv = df_exportar.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Programación Formato Excel (CSV)",
            data=csv,
            file_name='Programacion_Semanal_Consolidada.csv',
            mime='text/csv',
        )
