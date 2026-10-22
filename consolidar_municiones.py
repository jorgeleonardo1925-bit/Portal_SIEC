import os
import pandas as pd

# Carpeta de origen y archivo final
carpeta_origen = "excel_por_anos_municiones"
archivo_salida = "Base_Municiones_5_Anos.xlsx"

print("🔄 Iniciando consolidación y transformación de la base de datos de municiones...")

archivos = [f for f in os.listdir(carpeta_origen) if f.endswith('.xlsx') or f.endswith('.xls')]

def asignar_verificacion(valor):
    if pd.isna(valor):
        return 'No aplica'
    val_clean = str(valor).strip().lower()
    if not val_clean:
        return 'No aplica'
    
    # Palabras clave permitidas para 'Aplica' (incluye variantes y plurales comunes)
    aplica = ['decomisado', 'decomisados', 'indicio', 'indicios', 'recuperado', 'recuperados', 'requisa', 'requisas']
    
    if val_clean in aplica:
        return 'Aplica'
    else:
        return 'No aplica'

def asignar_institucion(valor):
    if pd.isna(valor):
        return None
    val_str = str(valor).strip()
    
    # Jerarquía: Prioridad principal 'Aeronaval', luego 'Brigada', luego 'Zona'
    if 'aeronaval' in val_str.lower():
        return 'Servicio Nacional Aeronaval'
    elif 'brigada' in val_str.lower():
        return 'Servicio Nacional de Fronteras'
    elif 'zona' in val_str.lower():
        return 'Policía Nacional'
    return None

if not archivos:
    print(f"❌ No se encontraron archivos Excel dentro de la carpeta '{carpeta_origen}'.")
else:
    dfs = []
    for archivo in archivos:
        ruta_completa = os.path.join(carpeta_origen, archivo)
        try:
            df_temp = pd.read_excel(ruta_completa)
            
            # 1. Crear columna 'Verificación' a partir de 'Relación' (o 'Relacion')
            if 'Relación' in df_temp.columns:
                df_temp['Verificación'] = df_temp['Relación'].apply(asignar_verificacion)
            elif 'Relacion' in df_temp.columns:
                df_temp['Verificación'] = df_temp['Relacion'].apply(asignar_verificacion)
                
            # 2. Crear columna 'Institucion' a partir de 'Nivel policial 1'
            col_nivel = [c for c in df_temp.columns if 'nivel policial 1' in c.lower()]
            if col_nivel:
                df_temp['Institucion'] = df_temp[col_nivel[0]].apply(asignar_institucion)

            # 3. Crear columnas 'Años' y 'Mes' a partir de la columna 'Fecha'
            col_fecha = [c for c in df_temp.columns if 'fecha' in c.lower()]
            if col_fecha:
                f_col = col_fecha[0]
                # Convertir a datetime de forma segura
                df_temp['Fecha_dt'] = pd.to_datetime(df_temp[f_col], errors='coerce')
                
                # Extraer Año y Mes
                df_temp['Años'] = df_temp['Fecha_dt'].dt.year
                
                # Diccionario para mapear los meses a texto en español (opcional, acorde al estándar del sistema)
                meses_esp = {
                    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 
                    5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 
                    9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
                }
                df_temp['Mes'] = df_temp['Fecha_dt'].dt.month.map(meses_esp)
                
                # Limpiar la columna temporal auxiliar
                df_temp.drop(columns=['Fecha_dt'], inplace=True, errors='ignore')

            print(f"  └─ Procesado y transformado: {archivo} ({len(df_temp)} registros)")
            dfs.append(df_temp)
        except Exception as e:
            print(f"  └─ ⚠️ Error al procesar {archivo}: {e}")

    if dfs:
        df_consolidado = pd.concat(dfs, ignore_index=True)
        df_consolidado.to_excel(archivo_salida, index=False)
        print("--------------------------------------------------")
        print(f"✅ ¡Consolidación y estandarización exitosa!")
        print(f"📁 Archivo generado: '{archivo_salida}'")
        print(f"📊 Total de registros consolidados: {len(df_consolidado):,}")
    else:
        print("❌ No se pudieron procesar los archivos.")