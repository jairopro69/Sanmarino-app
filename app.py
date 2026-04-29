import streamlit as st
import pandas as pd

# ==========================================
# CONFIGURACIÓN DE LA PÁGINA
# ==========================================
st.set_page_config(page_title="Motor Logístico Huevo", page_icon="🥚", layout="wide")
st.title("🚚 Panel de Programación Logística - Huevo")
st.markdown("Sistema semi-automático de asignación y validación de flota.")

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
    'Costa Rica': 'XMA049', 
    'La Esmeralda': 'XVV085'
}

CARROS_FLANDES = ['LPM116', 'LWY708']

# ==========================================
# 2. FUNCIONES DEL MOTOR LÓGICO
# ==========================================
def validar_jerarquia_fisica(tipo_vehiculo, permiso_nodo):
    permiso = str(permiso_nodo).strip().upper()
    tipo = str(tipo_vehiculo).strip().upper()
    if permiso in JERARQUIA_ACCESO:
        return tipo in JERARQUIA_ACCESO[permiso]
    return False

def validar_exclusividad(nodo_destino, placa_evaluada):
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
# 3. PANEL LATERAL (CARGA DE MAESTRAS)
# ==========================================
st.sidebar.header("📁 Base de Datos")
st.sidebar.markdown("Sube tu archivo **Maestras sanma.xlsx** para que el motor pueda validar reglas.")
archivo_maestras = st.sidebar.file_uploader("Subir Maestras", type=['xlsx'])

df_vehiculos = None
df_nodos = None

if archivo_maestras is not None:
    try:
        df_vehiculos = pd.read_excel(archivo_maestras, sheet_name='Maestra_Vehiculos')
        df_nodos = pd.read_excel(archivo_maestras, sheet_name='Maestra_Nodos')
        st.sidebar.success("✅ Bases maestras cargadas y listas.")
    except Exception as e:
        st.sidebar.error(f"Error al leer el archivo: Asegúrate de que tenga las pestañas correctas.")

# ==========================================
# 4. INTERFAZ PRINCIPAL: PLANTILLA DE VIAJES
# ==========================================
st.subheader("📋 Plantilla de Viajes Fijos Diarios")
st.write("Marca la casilla **'🚫 Bloquear'** si por alguna situación un viaje NO debe programarse hoy.")

# Datos base (Tu plantilla)
datos_plantilla = {
    'Hora': ['7:00 AM', '2:00 PM', '2:00 PM', '2:00 PM', '2:00 PM'],
    'Conductor_Sugerido': ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA LUIS', 'RINCON RODRIGUEZ SEBASTIAN', 'VARGAS CIRO ALFONSO'],
    'Placa_Sugerida': ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154'],
    'Ruta_Destino': ['Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 'Villa Johana/La Maria San Gil']
}
df_viajes_base = pd.DataFrame(datos_plantilla)

# Editor interactivo
viajes_editados = st.data_editor(
    df_viajes_base,
    column_config={
        "Bloquear": st.column_config.CheckboxColumn(
            "🚫 Bloquear",
            help="Excluir viaje de la programación de hoy",
            default=False,
        )
    },
    disabled=["Hora", "Conductor_Sugerido", "Placa_Sugerida", "Ruta_Destino"],
    hide_index=True,
    use_container_width=True
)

# ==========================================
# 5. EL GATILLO: BOTÓN DE PROGRAMACIÓN
# ==========================================
st.markdown("---")
if st.button("🚀 PROGRAMAR VIAJES DEL DÍA", type="primary", use_container_width=True):
    
    # Filtramos los bloqueados
    if 'Bloquear' in viajes_editados.columns:
        viajes_activos = viajes_editados[viajes_editados['Bloquear'] != True].copy()
    else:
        viajes_activos = viajes_editados.copy()
        
    if viajes_activos.empty:
        st.warning("⚠️ Todos los viajes están bloqueados. No hay nada que programar.")
    else:
        st.success(f"⚙️ Iniciando motor logístico para {len(viajes_activos)} viajes...")
        
        # Simulamos la revisión del motor para mostrar resultados
        resultados_validacion = []
        
        for index, viaje in viajes_activos.iterrows():
            placa = viaje['Placa_Sugerida']
            destino = viaje['Ruta_Destino']
            
            # Si el usuario subió el Excel, hacemos la validación REAL
            if df_vehiculos is not None and df_nodos is not None:
                try:
                    # Regla Exclusividad
                    ok_exclusividad, msj = validar_exclusividad(destino, placa)
                    if ok_exclusividad:
                        estado = "✅ Aprobado"
                    else:
                        estado = f"❌ Rechazado: {msj}"
                except Exception as e:
                    estado = "⚠️ Error al validar"
            else:
                # Si no han subido el Excel, mostramos un aviso
                estado = "⚠️ Pendiente (Falta subir Maestras)"
                
            resultados_validacion.append(estado)
            
        # Añadimos el veredicto del motor a la tabla final
        viajes_activos['Veredicto_Motor'] = resultados_validacion
        
        st.write("### 🏁 Programación Final y Veredicto del Motor:")
        st.dataframe(viajes_activos.drop(columns=['Bloquear'], errors='ignore'), hide_index=True, use_container_width=True)
        
        # Botón para descargar el resultado
        csv = viajes_activos.drop(columns=['Bloquear'], errors='ignore').to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Descargar Programación Final (CSV)",
            data=csv,
            file_name='Programacion_Diaria_Aprobada.csv',
            mime='text/csv',
        )
