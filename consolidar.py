import os
import glob
import pandas as pd
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

def consolidar_archivos_multianual():
    carpeta_origen = "./excel_por_anos"
    archivo_salida = "Base_Consolidada_5_Anos.xlsx"
    
    patron = os.path.join(carpeta_origen, "*.xlsx")
    
    # FILTRO CLAVE: Ignorar los archivos temporales de Excel que empiezan con ~$
    archivos = [f for f in glob.glob(patron) if not os.path.basename(f).startswith("~$")]
    
    if not archivos:
        print(f"⚠️ No se encontraron archivos Excel válidos en la carpeta '{carpeta_origen}'.")
        return
        
    print(f"📁 Se encontraron {len(archivos)} archivos válidos para consolidar. Procesando...")
    
    lista_dfs = []
    
    for archivo in archivos:
        nombre_archivo = os.path.basename(archivo)
        print(f"    -> Leyendo e integrando: {nombre_archivo}")
        
        try:
            # 1. Leer el archivo sin cabecera fija para detectar la fila correcta de encabezados
            df_raw = pd.read_excel(archivo, header=None)
            header_row = 0
            
            # Buscar en las primeras 10 filas cuál contiene la palabra 'fecha'
            for idx, row in df_raw.head(10).iterrows():
                fila_texto = row.astype(str).str.lower()
                if fila_texto.str.contains('fecha').any():
                    header_row = idx
                    break
            
            # 2. Cargar el archivo usando la fila de cabecera detectada automáticamente
            df = pd.read_excel(archivo, header=header_row)
            
            # Limpiar espacios en los nombres de las columnas
            df.columns = df.columns.str.strip()
            
            # Normalizar el nombre de la columna de fecha
            nombres_fecha_posibles = ['Fecha', 'FECHA', 'fecha', 'Fecha de Incautación', 'Fecha Incautación']
            encontrada = False
            for nombre in nombres_fecha_posibles:
                if nombre in df.columns:
                    if nombre != 'Fecha':
                        df = df.rename(columns={nombre: 'Fecha'})
                    encontrada = True
                    break
                    
            if not encontrada:
                print(f"⚠️ Advertencia: El archivo '{nombre_archivo}' no tiene una columna de fecha reconocida. Columnas disponibles: {list(df.columns)}")
                
            df['Archivo_Origen'] = nombre_archivo
            lista_dfs.append(df)
            
        except Exception as e:
            print(f"❌ Error al leer el archivo {nombre_archivo}: {e}")
            
    if not lista_dfs:
        print("❌ No se pudieron procesar datos válidos.")
        return
        
    # Unir todos los DataFrames en uno solo
    df_final = pd.concat(lista_dfs, ignore_index=True)
    
    # -------------------------------------------------------------
    # TRANSFORMACIÓN Y LIMPIEZA DE DATOS MULTIANUAL
    # -------------------------------------------------------------
    print("⚙️ Procesando fechas, instituciones, corregimientos y filtros operacionales...")
    
    if 'Fecha' in df_final.columns:
        df_final['Fecha_dt'] = pd.to_datetime(df_final['Fecha'], errors='coerce')
        df_final['Año'] = df_final['Fecha_dt'].dt.year
        
        meses_espanol = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }
        df_final['Mes'] = df_final['Fecha_dt'].dt.month.map(meses_espanol)
        df_final = df_final.drop(columns=['Fecha_dt'])
    else:
        print("❌ Error crítico: No se encontró la columna 'Fecha' unificada en los datos.")
        return
    
    # Limpieza de textos en 'Corregimiento' y 'Lugar'
    if 'Corregimiento' in df_final.columns:
        df_final['Corregimiento'] = df_final['Corregimiento'].astype(str).str.strip().replace({'nan': 'No especificado', 'None': 'No especificado'})
        
    if 'Lugar' in df_final.columns:
        df_final['Lugar'] = df_final['Lugar'].astype(str).str.strip().replace({'nan': 'No especificado', 'None': 'No especificado'})
    
    # Clasificación institucional priorizando términos específicos
    def evaluar_institucion(nivel):
        texto = str(nivel).lower()
        if 'aeronaval' in texto:
            return 'Servicio Nacional Aeronaval'
        elif 'brigada' in texto:
            return 'Servicio Nacional de Fronteras'
        elif 'zona' in texto:
            return 'Policía Nacional'
        return 'No especificado'
        
    if 'Nivel Policial 1' in df_final.columns:
        df_final['Instituciones'] = df_final['Nivel Policial 1'].apply(evaluar_institucion)
    else:
        df_final['Instituciones'] = 'No especificado'
    
    # Regla de verificación por estado operativo
    criterios_aplica = ['decomisado', 'decomisada', 'indicios', 'recuperados', 'recuperado', 'requisa']
    
    def evaluar_verificacion(relacion):
        texto = str(relacion).lower()
        for criterio in criterios_aplica:
            if criterio in texto:
                return "Aplica"
        return "No Aplica"
        
    if 'Relación' in df_final.columns:
        df_final['Verificación'] = df_final['Relación'].apply(evaluar_verificacion)
    
    # -------------------------------------------------------------
    # EXPORTACIÓN CON DISEÑO CORPORATIVO
    # -------------------------------------------------------------
    anos_detectados = sorted([int(x) for x in df_final['Año'].dropna().unique()])
    print(f"\n✨ Consolidación exitosa de {len(anos_detectados)} años: {anos_detectados}")
    print(f"📊 Total registros unificados: {len(df_final):,}")
    print(f"💾 Guardando resultado en '{archivo_salida}'...")
    
    with pd.ExcelWriter(archivo_salida, engine='openpyxl') as writer:
        df_final.to_excel(writer, sheet_name='Consolidado', index=False)
        ws = writer.sheets['Consolidado']
        ws.views.sheetView[0].showGridLines = True
        
        header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
        header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        
        for col_num, col_name in enumerate(df_final.columns, 1):
            cell = ws.cell(row=1, column=col_num)
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal="center", vertical="center")
            
            max_len = max(df_final[col_name].fillna('').astype(str).map(len).max(), len(str(col_name))) + 3
            col_letter = get_column_letter(col_num)
            ws.column_dimensions[col_letter].width = max(max_len, 12)
            
    print("🚀 ¡Proceso finalizado con éxito sin errores!")

if __name__ == "__main__":
    consolidar_archivos_multianual()