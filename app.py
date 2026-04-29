import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# ==========================================
# CONFIGURACIÓN ESTRICTA
# ==========================================
st.set_page_config(page_title="Motor Logístico Definitivo", layout="wide")

# ==========================================
# 1. EL CEREBRO: TODAS TUS REGLAS
# ==========================================
JERARQUIA = {'MULTIPLE': 5, 'DOBLE': 4, 'SENCILLO': 3, 'TURBO': 2, 'SEMITURBO': 1}

# Bases de datos maestras simuladas para el motor
VEHICULOS = {
    'UPR329': {'Tipo': 'TURBO', 'Titular': 'ISAIAS MARTINEZ SOLANO'},
    'WNN709': {'Tipo': 'SENCILLO', 'Titular': 'MENESES SEPULVEDA'},
    'SXT043': {'Tipo': 'SENCILLO', 'Titular': 'RINCON RODRIGUEZ'},
    'TRL154': {'Tipo': 'TURBO', 'Titular': 'VARGAS CIRO'},
    'LWY708': {'Tipo': 'SENCILLO', 'Titular': 'PEDRAZA MUÑOZ'},
    'LPK555': {'Tipo': 'TURBO', 'Titular': 'CARDENAS URIBE'},
    'XMA049': {'Tipo': 'SENCILLO', 'Titular': 'GOMEZ OSCAR'},
    'XVV085': {'Tipo': 'TURBO', 'Titular': 'VASQUEZ QUINTERO'},
    'LPM116': {'Tipo': 'DOBLE', 'Titular': 'GOMEZ HERRERA'},
    'ABC999': {'Tipo': 'MULTIPLE', 'Titular': 'CONDUCTOR COMODIN'} # Carro extra
}

CONDUCTORES = {
    'ISAIAS MARTINEZ SOLANO': {'Horas': 100, 'Domingos': 1, 'Descanso_Ok': True},
    'MENESES SEPULVEDA': {'Horas': 110, 'Domingos': 0, 'Descanso_Ok': True}, # A punto de pasarse de las 112 hrs
    'RINCON RODRIGUEZ': {'Horas': 80, 'Domingos': 1, 'Descanso_Ok': True},
    'VARGAS CIRO': {'Horas': 50, 'Domingos': 0, 'Descanso_Ok': False}, # No ha descansado los 2 días
    'PEDRAZA MUÑOZ': {'Horas': 60, 'Domingos': 2, 'Descanso_Ok': True}, # Ya trabajó 2 domingos
    'CARDENAS URIBE': {'Horas': 90, 'Domingos': 1, 'Descanso_Ok': True},
    'GOMEZ OSCAR': {'Horas': 40, 'Domingos': 0, 'Descanso_Ok': True},
    'VASQUEZ QUINTERO': {'Horas': 70, 'Domingos': 1, 'Descanso_Ok': True},
    'GOMEZ HERRERA': {'Horas': 90, 'Domingos': 1, 'Descanso_Ok': True},
    'CONDUCTOR COMODIN': {'Horas': 10, 'Domingos': 0, 'Descanso_Ok': True}
}

NODOS_PERMISOS = {
    'Girón Mesitas': 'MULTIPLE', 'Giron Caciquito': 'MULTIPLE', 'San Roque San Gil': 'SENCILLO', 
    'Rey David San Gil': 'TURBO', 'Villa Johana/La Maria': 'MULTIPLE', 'Juan Curi': 'SENCILLO', 
    'Miralindo': 'DOBLE', 'Dos Hilachas': 'MULTIPLE', 'La Esperanza': 'TURBO', 
    'Costa Rica': 'SENCILLO', 'La Esmeralda': 'TURBO', 'San German': 'MULTIPLE', 'Flandes': 'DOBLE'
}

# ==========================================
# 2. INICIALIZAR LA SEMANA (SOLO COLUMNAS EXACTAS)
# ==========================================
if 'df_semana' not in st.session_state or 'ultimo_flandes' not in st.session_state:
    st.session_state.ultimo_flandes = 'LPM116' # Historial inicial
    
    rutas_fijas = ['Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 'Villa Johana/La Maria']
    rutas_vacias = ['Juan Curi', 'Miralindo', 'Dos Hilachas', 'La Esperanza', 'Costa Rica', 'La Esmeralda', 'San German', 'Flandes']
    
    placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154']
    cond_fijos = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA', 'RINCON RODRIGUEZ', 'VARGAS CIRO']
    
    filas = []
    fecha_inicio = pd.to_datetime('2026-05-04')
    
    for i in range(7):
        fecha = (fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y')
        dia_semana = (fecha_inicio + timedelta(days=i)).weekday() # 0=Lunes, 2=Miercoles, 5=Sabado
        
        # 1. Cargar las 5 rutas que SIEMPRE tienen datos fijos
        for j, ruta in enumerate(rutas_fijas):
            filas.append({'Bloquear': False, 'Fecha': fecha, 'Hora': '7:00 AM' if ruta == 'Girón Mesitas' else '2:00 PM',
                          'Conductor': cond_fijos[j], 'Placa': placas_fijas[j], 'Ruta': ruta, 'Intento': 1})
            
        # 2. Cargar el resto EN BLANCO
        for ruta in rutas_vacias:
            # Regla de Flandes (Solo Miercoles y Sabado)
            if ruta == 'Flandes' and dia_semana not in [2, 5]:
                continue
            
            filas.append({'Bloquear': False, 'Fecha': fecha, 'Hora': '2:00 PM',
                          'Conductor': '', 'Placa': '', 'Ruta': ruta, 'Intento': 1})

    st.session_state.df_semana = pd.DataFrame(filas)

# ==========================================
# 3. FUNCIONES DE VALIDACIÓN (AQUÍ ESTÁ TODO)
# ==========================================
def validar_laboral(conductor, es_domingo):
    """REGLA: 112 horas, 2 días de descanso, max 2 domingos"""
    datos = CONDUCTORES.get(conductor)
    if not datos: return False
    if datos['Horas'] + 8 > 112: return False # Supera 112 hrs quincenales
    if not datos['Descanso_Ok']: return False # No ha descansado 2 días tras ruta larga
    if es_domingo and datos['Domingos'] >= 2: return False # Supera los 2 domingos
    return True

def validar_jerarquia(placa, ruta):
    """REGLA: Si es sencillo entran todos menos doble, etc."""
    if placa not in VEHICULOS: return False
    tipo_vehiculo = VEHICULOS[placa]['Tipo']
    permiso_granja = NODOS_PERMISOS.get(ruta, 'SEMITURBO')
    return JERARQUIA[tipo_vehiculo] <= JERARQUIA[permiso_granja]

def programar_viajes():
    df = st.session_state.df_semana.copy()
    fechas = df['Fecha'].unique()
    viajes_pasados_a_manana = []

    for idx, fecha in enumerate(fechas):
        es_domingo = pd.to_datetime(fecha, format='%d/%m/%Y').weekday() == 6
        
        # INYECTAR REPROGRAMADOS DEL DÍA ANTERIOR A LAS 7:00 AM
        for pendiente in viajes_pasados_a_manana:
            nuevo = pendiente.copy()
            nuevo['Fecha'] = fecha
            nuevo['Hora'] = '7:00 AM' # REGLA: Pasa a la mañana
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        viajes_pasados_a_manana = []

        # FILTRAR VIAJES DE HOY QUE NO ESTÁN BLOQUEADOS
        mask = (df['Fecha'] == fecha) & (df['Bloquear'] == False) & (df['Conductor'] == '')
        
        for index, row in df[mask].iterrows():
            ruta = row['Ruta']
            intento = row['Intento']
            placa_asignada = ""
            cond_asignado = ""
            
            # REGLA: TERCEROS (Si ya falló una vez y pasó a la mañana, a la siguiente va por tercero)
            if intento > 1:
                df.at[index, 'Conductor'] = 'TERCERO (AGENCIA)'
                df.at[index, 'Placa'] = 'EXTERNA'
                continue

            # REGLAS EXCLUSIVAS Y FLANDES
            if ruta == 'Dos Hilachas': placa_asignada = 'LWY708'
            elif ruta == 'La Esperanza': placa_asignada = 'LPK555'
            elif ruta == 'Costa Rica': placa_asignada = 'XMA049'
            elif ruta == 'La Esmeralda': placa_asignada = 'XVV085'
            elif ruta == 'Flandes':
                placa_asignada = 'LWY708' if st.session_state.ultimo_flandes == 'LPM116' else 'LPM116'
                st.session_state.ultimo_flandes = placa_asignada # Actualiza el historial
                
            # BUSCAR RECURSOS SI NO ES EXCLUSIVA
            if not placa_asignada:
                for p in VEHICULOS.keys():
                    if validar_jerarquia(p, ruta):
                        titular = VEHICULOS[p]['Titular']
                        if validar_laboral(titular, es_domingo):
                            placa_asignada = p
                            cond_asignado = titular
                            break
            
            # SI ES EXCLUSIVA, VALIDAR AL TITULAR
            if placa_asignada and not cond_asignado:
                titular = VEHICULOS[placa_asignada]['Titular']
                if validar_laboral(titular, es_domingo):
                    cond_asignado = titular
                else:
                    # REGLA: Prioridad Titular, si no, buscar autorizado (Comodin)
                    cond_asignado = 'CONDUCTOR COMODIN' if validar_laboral('CONDUCTOR COMODIN', es_domingo) else ""

            # REGLA: BAJAR EN LA MAÑANA (Si faltaron carros o conductores)
            if not placa_asignada or not cond_asignado:
                row['Intento'] += 1
                viajes_pasados_a_manana.append(row)
                df.at[index, 'Conductor'] = '⚠️ PASA A MAÑANA'
                df.at[index, 'Placa'] = '⚠️ SIN RECURSO'
            else:
                df.at[index, 'Placa'] = placa_asignada
                df.at[index, 'Conductor'] = cond_asignado

    st.session_state.df_semana = df

# ==========================================
# 4. INTERFAZ: VISUALIZACIÓN EXACTA
# ==========================================
st.title("🚚 Panel de Programación Huevo")
st.write("Columnas exactas: Hora, Conductor, Placa, Ruta. (Más el bloqueo).")

dia_ver = st.selectbox("📅 Selecciona el día a visualizar:", st.session_state.df_semana['Fecha'].unique())

df_mostrar = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia_ver]

# ORDEN ESTRICTO DE COLUMNAS SEGÚN TU PETICIÓN
columnas_estrictas = ['Bloquear', 'Hora', 'Conductor', 'Placa', 'Ruta']

edited_df = st.data_editor(
    df_mostrar[columnas_estrictas],
    column_config={"Bloquear": st.column_config.CheckboxColumn("🚫 Bloq")},
    hide_index=True,
    use_container_width=True,
    key="editor_semanal"
)

# Sincronizar edición manual
if st.button("💾 Guardar Cambios Manuales"):
    st.session_state.df_semana.update(edited_df)
    st.success("Cambios manuales guardados.")

if st.button("🚀 APLICAR MOTOR (REGLAS LOGÍSTICAS)", type="primary"):
    programar_viajes()
    st.rerun() # Refresca ahí mismo la tabla
