import glob
import os
import re
import pandas as pd


def estandarizar_institucion_sitigpol(val):
  """Estandariza las instituciones bajo el orden estricto solicitado:

  1. Si contiene 'AERONAVAL' -> Servicio Nacional Aeronaval
  2. Si contiene 'BRIGADA' (o 'BRIGADAS') -> Servicio Nacional de Fronteras
  3. Si contiene 'ZONA' -> Policía Nacional
  """
  if pd.isna(val):
    return 'No Especificado'

  val_str = str(val).upper().strip()

  # 1. Aeronaval primero para evitar choques con la palabra 'Zona'
  if 'AERONAVAL' in val_str:
    return 'Servicio Nacional Aeronaval'
  # 2. Brigada o Brigadas (SENAFRONT)
  elif 'BRIGADA' in val_str:
    return 'Servicio Nacional de Fronteras'
  # 3. Zona de Policía (Policía Nacional)
  elif 'ZONA' in val_str:
    return 'Policía Nacional'
  else:
    if any(k in val_str for k in ['PN', 'POLICIA', 'POLICÍA']):
      return 'Policía Nacional'
    elif any(k in val_str for k in ['SENAFRONT', 'FRONTERAS']):
      return 'Servicio Nacional de Fronteras'
    elif any(k in val_str for k in ['SENAN', 'SNAN']):
      return 'Servicio Nacional Aeronaval'
    return str(val).strip()


def separar_cantidad_y_tipo(val):
  """Separa el valor numérico (Cantidad_Real) de la unidad/descripción (Tipo)"""
  if pd.isna(val):
    return None, ''

  val_str = str(val).strip()
  num_match = re.search(r'[\d\.,]+', val_str)
  if num_match:
    num_str = num_match.group(0).replace(',', '')
    try:
      num_val = float(num_str) if '.' in num_str else int(num_str)
    except ValueError:
      num_val = None
  else:
    num_val = None

  text_val = re.sub(r'[\d\.,]+', '', val_str).strip()
  return num_val, text_val


def consolidar_archivos_drogas(
    nombre_carpeta='excel_drogas_SITIGPOL',
    archivo_salida='consolidado_drogas_SITIGPOL.xlsx',
):
  patron = os.path.join(nombre_carpeta, '*.xls*')
  archivos_excel = glob.glob(patron)

  if not archivos_excel:
    print(
        f"⚠️ No se encontraron archivos Excel en la carpeta '{nombre_carpeta}'."
    )
    return

  print(
      f"📁 Se encontraron {len(archivos_excel)} archivo(s) en"
      f" '{nombre_carpeta}'. Procesando..."
  )
  lista_dfs = []

  for archivo in archivos_excel:
    print(f'📊 Leyendo: {archivo}...')
    try:
      xls = pd.ExcelFile(archivo)
      for hoja in xls.sheet_names:
        df_hoja = pd.read_excel(xls, sheet_name=hoja)
        if not df_hoja.empty:
          lista_dfs.append(df_hoja)
    except Exception as e:
      print(f'❌ Error al leer {archivo}: {e}')

  if not lista_dfs:
    print('⚠️ No hay datos para consolidar.')
    return

  df_consolidado = pd.concat(lista_dfs, ignore_index=True)

  print('📋 Columnas disponibles en los archivos:', df_consolidado.columns.tolist())

  # 1. Asignación directa y segura de la institución usando 'Nivel Policial 1' como referencia
  col_referencia = 'Nivel Policial 1'
  if col_referencia in df_consolidado.columns:
    print(
        "✅ Columna de referencia detectada para institución:"
        f" '{col_referencia}'"
    )
    df_consolidado['Institución'] = df_consolidado[col_referencia].apply(
        estandarizar_institucion_sitigpol
    )
  else:
    # Búsqueda de respaldo en caso de que cambie el nombre de la columna en algún archivo
    candidatos_inst = [
        c
        for c in df_consolidado.columns
        if any(
            k in c.lower()
            for k in ['inst', 'entidad', 'unidad', 'zonal', 'depend', 'org']
        )
    ]
    col_inst = candidatos_inst[0] if candidatos_inst else None
    if col_inst:
      print(f"✅ Columna alternativa de institución detectada: '{col_inst}'")
      df_consolidado['Institución'] = df_consolidado[col_inst].apply(
          estandarizar_institucion_sitigpol
      )
    else:
      print(
          '⚠️ No se encontró la columna de referencia. Se asignará valor por'
          ' defecto.'
      )
      df_consolidado['Institución'] = 'No Especificado'

  # 2. Columnas "Cantidad_Real" y "Tipo"
  col_cant = next(
      (
          c
          for c in df_consolidado.columns
          if 'cant' in c.lower() or 'peso' in c.lower()
      ),
      'Cantidad',
  )
  if col_cant in df_consolidado.columns:
    res_cant = df_consolidado[col_cant].apply(separar_cantidad_y_tipo)
    df_consolidado['Cantidad_Real'] = [r[0] for r in res_cant]
    df_consolidado['Tipo'] = [r[1] for r in res_cant]
  else:
    df_consolidado['Cantidad_Real'] = None
    df_consolidado['Tipo'] = ''

  # 3. Columnas "Año" y "Mes" a partir de Fecha
  col_fecha = next((c for c in df_consolidado.columns if 'fech' in c.lower()), 'Fecha')
  if col_fecha in df_consolidado.columns:
    df_consolidado['Fecha_dt'] = pd.to_datetime(
        df_consolidado[col_fecha], errors='coerce'
    )
    df_consolidado['Año'] = df_consolidado['Fecha_dt'].dt.year

    meses_es = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre',
    }
    df_consolidado['Mes'] = df_consolidado['Fecha_dt'].dt.month.map(meses_es)
    df_consolidado.drop(columns=['Fecha_dt'], inplace=True, errors='ignore')
  else:
    df_consolidado['Año'] = None
    df_consolidado['Mes'] = None

  df_consolidado.to_excel(archivo_salida, index=False)
  print(f"✅ ¡Consolidado guardado exitosamente como '{archivo_salida}'!")
  print('\nMuestra de los primeros registros procesados:')
  print(
      df_consolidado[['Institución', 'Cantidad_Real', 'Tipo', 'Año', 'Mes']].head(
          10
      )
  )


if __name__ == '__main__':
  consolidar_archivos_drogas()