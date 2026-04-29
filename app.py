import streamlit as st
import pandas as pd
import itertools

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Motor Logístico Huevo", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Logística Semanal")
st.markdown("Sistema de asignación para la semana del **Lunes 4 de Mayo al Domingo 10 de Mayo**.")

# ==========================================
# 1. DICCIONARIOS DEL MOTOR LÓGICO
# ==========================================
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
    'Costa Rica/Costa Rica': 'XMA049', 
    'La Esmeralda': 'XVV085'
}

CARROS_FLANDES = ['LPM116', 'LWY708']

def validar_exclusividad(nodo_destino, placa_evaluada):
    # Si la placa sugerida es "Por Asignar", dejamos que el motor sepa que falta trabajo
    if placa_evaluada == 'Por Asignar':
        return False, "⚠️ Falta asignar placa"
        
    for granja, placa_fija in RUTAS_EXCLUSIVAS.items():
        if granja.upper() in str(nodo_destino).upper():
            if placa_evaluada == placa_fija:
                return True, f"✅ Fijo para {granja}"
            else:
                return False, f"❌ Exclusivo de {placa_fija}"
                
    if 'FLANDES' in str(nodo_destino).upper():
        if placa_evaluada not in CARROS_FLANDES:
            return False, "❌ No autorizado para Flandes"
            
    return True, "✅ OK"

# ==========================================
# 2. PANEL LATERAL (CARGA DE MAESTRAS)
# ==========================================
st.sidebar.header("📁 Base de Datos")
st.sidebar.markdown("Sube tu archivo **Maestras sanma.xlsx** para validar reglas.")
archivo_maestras = st.sidebar.file_uploader("Subir Maestras", type=['xlsx'])

df_vehiculos = None
df_nodos = None

if archivo_maestras is not None:
    try:
        df_vehiculos = pd.read_excel(archivo_maestras, sheet_name='Maestra_Vehiculos')
        df_nodos = pd.read_excel(archivo_maestras, sheet_name='Maestra_Nodos')
        st.sidebar.success("✅ Bases maestras cargadas y listas.")
    except Exception as e:
        st.sidebar.error("Error al leer el archivo. Verifica las pestañas.")

# ==========================================
# 3. GENERACIÓN AUTOMÁTICA DE LA SEMANA
# ==========================================
# Listas base
dias_semana = [
    '1. Lunes 4 May', '2. Martes 5 May', '3. Miércoles 6 May', 
    '4. Jueves 7 May', '5. Viernes 8 May', '6. Sábado 9 May', '7. Domingo 10 May'
]

granjas = [
    'Girón Mesitas', 'Giron Caciquito', 'San Roque', 'Rey David', 
    'Villa Johana/La Maria', 'Juan Curi', 'Miralindo', 'Dos Hilachas', 
    'La Esperanza', 'Costa Rica/Costa Rica', 'La Esmeralda', 'San German'
]

# Mezclamos todos los días con todas las granjas (Producto Cartesiano)
combinaciones = list(itertools.product(dias_semana, granjas))
df_viajes_base = pd.DataFrame(combinaciones, columns=['Día', 'Ruta_Destino'])

# Aplicamos la regla del horario
df_viajes_base['Hora'] = '2:00 PM' # Por defecto en la tarde
df_viajes_base.loc[df_viajes_base['Ruta_Destino'] == 'Girón Mesitas', 'Hora'] = '7:00 AM' # Excepción Mañana

# Columnas editables para el usuario
df_viajes_base['Conductor_Sugerido'] = 'Por Asignar'
df_viajes_base['Placa_Sugerida'] = 'Por Asignar'
df_viajes_base['Bloquear'] = False

# Ordenamos las columnas para la vista
df_viajes_base = df_viajes_base[['Bloquear', 'Día', 'Hora', 'Ruta_Destino', 'Conductor_Sugerido', 'Placa_Sugerida']]

# ==========================================
# 4. INTERFAZ PRINCIPAL: EDITOR DE DATOS
# ==========================================
st.subheader("📋 Plantilla de Viajes (4 Mayo - 10 Mayo)")
st.write("Marca **'🚫 Bloquear'** para los viajes que NO se harán. Puedes escribir la Placa y Conductor haciendo doble clic en la celda 'Por Asignar'.")

viajes_editados = st.data_editor(
    df_viajes_base,
    column_config={
        "Bloquear": st.column_config.CheckboxColumn("🚫 Bloquear", default=False),
        "Conductor_Sugerido": st.column_config.TextColumn("👤 Conductor"),
        "Placa_Sugerida": st.column_config.TextColumn("🚚 Placa")
    },
    disabled=["Día", "Hora", "Ruta_Destino"], # Estos no se pueden modificar por error
    hide_index=True,
    use_container_width=True,
    height=500 # Altura ampliada para ver bien la semana
)

# ==========================================
# 5. EL GATILLO: BOTÓN DE PROGRAMACIÓN
# ==========================================
st.markdown("---")
if st.button("🚀 PROGRAMAR SEMANA COMPLETA", type="primary", use_container_width=True):
    
    # Filtramos los bloqueados
    viajes_activos = viajes_editados[viajes_editados['Bloquear'] != True].copy()
        
    if viajes_activos.empty:
        st.warning("⚠️ Todos los viajes están bloqueados. No hay nada que programar.")
    else:
        st.success(f"⚙️ Iniciando motor logístico para {len(viajes_activos)} viajes autorizados...")
        
        resultados_validacion = []
        
        for index, viaje in viajes_activos.iterrows():
            placa = viaje['Placa_Sugerida']
            destino = viaje['Ruta_Destino']
            
            if df_vehiculos is not None and df_nodos is not None:
                try:
                    ok_exclusividad, msj = validar_exclusividad(destino, placa)
                    estado = "✅ Aprobado" if ok_exclusividad else f"❌ Rechazado: {msj}"
                except Exception as e:
                    estado = "⚠️ Error al validar"
            else:
                estado = "⚠️ Pendiente (Falta subir Maestras)"
                
            resultados_validacion.append(estado)
            
        viajes_activos['Veredicto_Motor'] = resultados_validacion
        
        st.write("### 🏁 Programación Final y Veredicto del Motor:")
        st.dataframe(viajes_activos.drop(columns=['Bloquear']), hide_index=True, use_container_width=True)
        
        csv = viajes_activos.drop(columns=['Bloquear']).to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Programación Semanal (CSV)",
            data=csv,
            file_name='Programacion_Semana_Mayo_4_al_10.csv',
            mime='text/csv',
        )
