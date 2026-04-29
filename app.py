import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import random

# ==========================================
# CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="Programador Logístico", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Diaria - Huevo")

# ==========================================
# 1. REGLAS DEL NEGOCIO (EL CEREBRO)
# ==========================================
# Aquí están las reglas que me diste
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

# Flota simulada para rellenar vacíos (mientras subimos tu Excel real)
FLOTA_DISPONIBLE = ['ABC111', 'DEF222', 'GHI333', 'JKL444', 'MNO555']
CONDUCTORES_DISPONIBLES = ['PABLO PEREZ', 'JUAN GOMEZ', 'CARLOS RUIZ', 'ANDRES DIAZ']

# ==========================================
# 2. PLANTILLA BASE
# ==========================================
rutas_base = [
    'Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 
    'Villa Johana/La Maria San Gil', 'Juan Curi San Gil', 'Miralindo San Gil', 
    'Dos Hilachas San Gil', 'La Esperanza', 'Costa Rica/Costa Rica', 
    'La Esmeralda San gil', 'San German'
]
placas_base = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154', '', '', 'LWY708', 'LPK555', 'XMA049', 'XVV085', '']
conductores_base = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS HERNANDO', 'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO', '', '', '', '', '', '', '']
horas_base = ['7:00 AM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM']

dias_semana = [(pd.to_datetime('2026-05-04') + timedelta(days=i)).strftime('%d/%m/%Y') for i in range(7)]
nombres_dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo']

def generar_plantilla_dia():
    return pd.DataFrame({
        '🚫 Bloquear': [False] * len(rutas_base),
        'Hora': horas_base,
        'Conductor': conductores_base,
        'Placa': placas_base,
        'Ruta/Cliente': rutas_base
    })

# ==========================================
# 3. EL MOTOR DE ASIGNACIÓN (TUS CONDICIONALES)
# ==========================================
def asignar_viajes_vacios(df):
    """Aquí Python aplica tus reglas para rellenar los espacios en blanco"""
    for index, fila in df.iterrows():
        destino = str(fila['Ruta/Cliente'])
        placa_actual = fila['Placa']
        conductor_actual = fila['Conductor']

        # 1. REGLA: Asignar placa si está vacía
        if placa_actual == "":
            # Verificamos si es ruta exclusiva
            es_exclusiva = False
            for granja, placa_fija in RUTAS_EXCLUSIVAS.items():
                if granja.upper() in destino.upper():
                    df.at[index, 'Placa'] = placa_fija
                    es_exclusiva = True
                    break
            
            # Verificamos si es Flandes
            if not es_exclusiva and 'FLANDES' in destino.upper():
                df.at[index, 'Placa'] = random.choice(CARROS_FLANDES) # Asigna uno de los dos permitidos
                es_exclusiva = True
                
            # Si no es exclusiva, asignamos un carro general disponible que cumpla el tamaño (Aquí cruzaremos con tu Excel)
            if not es_exclusiva:
                df.at[index, 'Placa'] = random.choice(FLOTA_DISPONIBLE) 

        # 2. REGLA: Asignar conductor si está vacío (Prioridad al Titular)
        if conductor_actual == "":
            placa_asignada = df.at[index, 'Placa']
            # Aquí Python debe buscar quién es el titular de 'placa_asignada'.
            # Simulamos que encuentra al titular disponible:
            df.at[index, 'Conductor'] = f"TITULAR DE {placa_asignada}"

    return df

# ==========================================
# INTERFAZ GRÁFICA
# ==========================================
st.markdown("### Selecciona el día a programar:")
tabs = st.tabs([f"{nombres_dias[i].capitalize()}" for i in range(7)])
viajes_por_dia = {}

for i, tab in enumerate(tabs):
    with tab:
        fecha_actual = dias_semana[i]
        df_dia = generar_plantilla_dia()
        
        viajes_editados = st.data_editor(
            df_dia,
            column_config={
                "🚫 Bloquear": st.column_config.CheckboxColumn("🚫 Bloquear", width="small"),
                "Hora": st.column_config.TextColumn("Hora", disabled=True),
                "Ruta/Cliente": st.column_config.TextColumn("Ruta/Cliente", disabled=True)
            },
            hide_index=True, use_container_width=True, key=f"editor_dia_{i}"
        )
        viajes_editados['Fecha'] = fecha_actual
        viajes_por_dia[fecha_actual] = viajes_editados

# ==========================================
# BOTÓN DE EJECUCIÓN (GATILLO DEL MOTOR)
# ==========================================
st.markdown("---")
if st.button("🚀 PROGRAMAR VIAJES (LLENAR VACÍOS)", type="primary", use_container_width=True):
    
    lista_df_activos = []
    for fecha, df in viajes_por_dia.items():
        df_activo = df[df['🚫 Bloquear'] != True].copy()
        
        # ¡AQUÍ LLAMAMOS A LA FUNCIÓN QUE RELLENA LOS VACÍOS CON TUS REGLAS!
        df_programado = asignar_viajes_vacios(df_activo) 
        
        lista_df_activos.append(df_programado)
        
    df_consolidado = pd.concat(lista_df_activos, ignore_index=True)
    
    st.success("✅ ¡Listo! Python aplicó las reglas exclusivas y rellenó los espacios vacíos.")
    st.dataframe(df_consolidado.drop(columns=['🚫 Bloquear']), hide_index=True, use_container_width=True)
