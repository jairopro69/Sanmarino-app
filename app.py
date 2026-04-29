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
    'ABC999': {'Tipo': 'MULTIPLE', 'Titular': 'CONDUCTOR COMODIN'}
}

CONDUCTORES = {
    'ISAIAS MARTINEZ SOLANO': {'Horas': 100, 'Domingos': 1, 'Descanso_Ok': True},
    'MENESES SEPULVEDA': {'Horas': 110, 'Domingos': 0, 'Descanso_Ok': True},
    'RINCON RODRIGUEZ': {'Horas': 80, 'Domingos': 1, 'Descanso_Ok': True},
    'VARGAS CIRO': {'Horas': 50, 'Domingos': 0, 'Descanso_Ok': False}, 
    'PEDRAZA MUÑOZ': {'Horas': 60, 'Domingos': 2, 'Descanso_Ok': True},
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
# 2. INICIALIZAR LA SEMANA 
# ==========================================
if 'df_semana' not in st.session_state or 'ultimo_flandes' not in st.session_state:
    st.session_state.ultimo_flandes = 'LPM116' 
    
    rutas_fijas = ['Girón Mesitas', 'Giron Caciquito', 'San Roque San Gil', 'Rey David San Gil', 'Villa Johana/La Maria']
    rutas_vacias = ['Juan Curi', 'Miralindo', 'Dos Hilachas', 'La Esperanza', 'Costa Rica', 'La Esmeralda', 'San German', 'Flandes']
    
    placas_fijas = ['UPR329', 'UPR329', 'WNN709', 'SXT043', 'TRL154']
    cond_fijos = ['ISAIAS MARTINEZ SOLANO', 'ISAIAS MARTINEZ SOLANO', 'MENESES SEPULVEDA', 'RINCON RODRIGUEZ', 'VARGAS CIRO']
    
    filas = []
    fecha_inicio = pd.to_datetime('2026-05-04')
    
    for i in range(7):
        fecha = (fecha_inicio + timedelta(days=i)).strftime('%d/%m/%Y')
        dia_semana = (fecha_inicio + timedelta(days=i)).weekday()
        
        for j, ruta in enumerate(rutas_fijas):
            filas.append({'Bloquear': False, 'Fecha': fecha, 'Hora': '7:00 AM' if ruta == 'Girón Mesitas' else '2:00 PM',
                          'Conductor': cond_fijos[j], 'Placa': placas_fijas[j], 'Ruta': ruta, 'Intento': 1})
            
        for ruta in rutas_vacias:
            if ruta == 'Flandes' and dia_semana not in [2, 5]:
                continue
            filas.append({'Bloquear': False, 'Fecha': fecha, 'Hora': '2:00 PM',
                          'Conductor': '', 'Placa': '', 'Ruta': ruta, 'Intento': 1})

    st.session_state.df_semana = pd.DataFrame(filas)

# ==========================================
# 3. FUNCIONES DE VALIDACIÓN CORREGIDAS
# ==========================================
def validar_laboral(conductor, es_domingo):
    datos = CONDUCTORES.get(conductor)
    if not datos: return False
    if datos['Horas'] + 8 > 112: return False 
    if not datos['Descanso_Ok']: return False 
    if es_domingo and datos['Domingos'] >= 2: return False 
    return True

def validar_jerarquia(placa, ruta):
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
        
        # 1. INYECTAR REPROGRAMADOS A LAS 7:00 AM
        for pendiente in viajes_pasados_a_manana:
            nuevo = pendiente.copy()
            nuevo['Fecha'] = fecha
            nuevo['Hora'] = '7:00 AM'
            df = pd.concat([df, pd.DataFrame([nuevo])], ignore_index=True)
        viajes_pasados_a_manana = []

        mask = (df['Fecha'] == fecha) & (df['Bloquear'] == False) & (df['Conductor'] == '')
        
        for index, row in df[mask].iterrows():
            ruta = row['Ruta']
            intento = row['Intento']
            hora_viaje = row['Hora']
            placa_asignada = ""
            cond_asignado = ""
            
            # EL PARCHE DE ORO: VERIFICAR OCUPADOS EN EL MISMO TURNO EXACTO
            ocupados_turno = df[(df['Fecha'] == fecha) & (df['Hora'] == hora_viaje)]
            placas_ocupadas = ocupados_turno[ocupados_turno['Placa'] != '']['Placa'].tolist()
            cond_ocupados = ocupados_turno[ocupados_turno['Conductor'] != '']['Conductor'].tolist()

            if intento > 1:
                df.at[index, 'Conductor'] = 'TERCERO (AGENCIA)'
                df.at[index, 'Placa'] = 'EXTERNA'
                continue

            candidato_fijo = None
            if ruta == 'Dos Hilachas': candidato_fijo = 'LWY708'
            elif ruta == 'La Esperanza': candidato_fijo = 'LPK555'
            elif ruta == 'Costa Rica': candidato_fijo = 'XMA049'
            elif ruta == 'La Esmeralda': candidato_fijo = 'XVV085'
            elif ruta == 'Flandes':
                candidato_fijo = 'LWY708' if st.session_state.ultimo_flandes == 'LPM116' else 'LPM116'

            # REVISIÓN DE EXCLUSIVIDAD VS DISPONIBILIDAD DE TURNO
            if candidato_fijo:
                if candidato_fijo not in placas_ocupadas:
                    placa_asignada = candidato_fijo
                    if ruta == 'Flandes': st.session_state.ultimo_flandes = placa_asignada

            # BUSCAR RECURSOS LIBRES
            if not placa_asignada and not candidato_fijo:
                for p in VEHICULOS.keys():
                    if p in placas_ocupadas: continue # Salta si el carro ya tiene viaje a esta hora
                    if validar_jerarquia(p, ruta):
                        titular = VEHICULOS[p]['Titular']
                        if titular in cond_ocupados: continue # Salta si el conductor ya tiene viaje a esta hora
                        if validar_laboral(titular, es_domingo):
                            placa_asignada = p
                            cond_asignado = titular
                            break
            
            if placa_asignada and not cond_asignado:
                titular = VEHICULOS[placa_asignada]['Titular']
                if titular not in cond_ocupados and validar_laboral(titular, es_domingo):
                    cond_asignado = titular
                else:
                    if 'CONDUCTOR COMODIN' not in cond_ocupados and validar_laboral('CONDUCTOR COMODIN', es_domingo):
                        cond_asignado = 'CONDUCTOR COMODIN'

            # REGLA: BAJAR EN LA MAÑANA SI FALLA
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

dia_ver = st.selectbox("📅 Selecciona el día a visualizar:", st.session_state.df_semana['Fecha'].unique())

df_mostrar = st.session_state.df_semana[st.session_state.df_semana['Fecha'] == dia_ver]
columnas_estrictas = ['Bloquear', 'Hora', 'Conductor', 'Placa', 'Ruta']

edited_df = st.data_editor(
    df_mostrar[columnas_estrictas],
    column_config={"Bloquear": st.column_config.CheckboxColumn("🚫 Bloq")},
    hide_index=True,
    use_container_width=True,
    key="editor_semanal"
)

if st.button("💾 Guardar Cambios Manuales"):
    st.session_state.df_semana.update(edited_df)
    st.success("Cambios manuales guardados.")

if st.button("🚀 APLICAR MOTOR (REGLAS LOGÍSTICAS)", type="primary"):
    programar_viajes()
    st.rerun()
