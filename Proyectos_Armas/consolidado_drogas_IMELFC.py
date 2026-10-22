import pandas as pd

def consolidar_drogas():
    # Apuntamos a la subcarpeta donde guardaste el archivo
    archivo_entrada = 'excel_drogas_IMELFC/drogas_2025_2026_imelfc.xlsx'
    archivo_salida = 'Base_Drogas_5_Anos.xlsx'
    
    try:
        df = pd.read_excel(archivo_entrada, sheet_name='Hoja1')
        print(f"Archivo '{archivo_entrada}' cargado exitosamente.")
    except Exception as e:
        print(f"Error al cargar el archivo: {e}")
        return

    # Diccionario de coordenadas geográficas de referencia por procedencia
    coordenadas_dict = {
        'Colón': {'Latitud': 9.3592, 'Longitud': -79.9015},
        'Los Santos': {'Latitud': 7.7738, 'Longitud': -80.4182},
        'Panamá Oeste': {'Latitud': 8.8833, 'Longitud': -79.7500},
        'Panamá': {'Latitud': 8.9824, 'Longitud': -79.5199},
        'Veraguas': {'Latitud': 8.1408, 'Longitud': -80.9850},
        'Guna Yala': {'Latitud': 9.4217, 'Longitud': -78.4326},
        'Darién': {'Latitud': 8.3582, 'Longitud': -77.9529},
        'Bocas del Toro': {'Latitud': 9.3407, 'Longitud': -82.2533},
        'Chiriqui': {'Latitud': 8.4333, 'Longitud': -82.4333},
        'Coclé': {'Latitud': 8.5205, 'Longitud': -80.3553},
        'Herrera': {'Latitud': 7.9620, 'Longitud': -80.4286}
    }

    # Limpiar espacios en blanco en la columna PROCEDENCIA
    df['PROCEDENCIA_LIMPIA'] = df['PROCEDENCIA'].astype(str).str.strip()

    # Asignar Latitud y Longitud según la procedencia
    df['Latitud'] = df['PROCEDENCIA_LIMPIA'].map(lambda x: coordenadas_dict.get(x, {}).get('Latitud'))
    df['Longitud'] = df['PROCEDENCIA_LIMPIA'].map(lambda x: coordenadas_dict.get(x, {}).get('Longitud'))

    # Eliminar columna auxiliar
    df = df.drop(columns=['PROCEDENCIA_LIMPIA'])

    # Guardar el resultado en la carpeta principal listo para Streamlit
    df.to_excel(archivo_salida, index=False)
    print(f"¡Consolidado generado y guardado exitosamente como '{archivo_salida}'!")
    print(df.head(10))

if __name__ == '__main__':
    consolidar_drogas()