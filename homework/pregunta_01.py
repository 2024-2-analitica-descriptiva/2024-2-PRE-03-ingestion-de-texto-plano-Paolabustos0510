import pandas as pd
import re

def pregunta_01():
    # Leer el archivo línea por línea
    with open(r"C:\Users\Olga\Documents\GitHub\2024-2-PRE-03-ingestion-de-texto-plano-Paolabustos0510\files\input\clusters_report.txt", 'r') as file:
        lines = file.readlines()

        # Limpiar y agrupar las líneas para cada fila del DataFrame
    data = []
    current_row = []
    for line in lines[4:]:  # Ignorar las primeras 4 líneas del encabezado
        line = line.strip()
        if re.match(r'^\d+', line):  # Si la línea empieza con un número, es el inicio de un nuevo cluster
            if current_row:  # Agregar la fila acumulada antes de empezar una nueva
                current_row[-1] = re.sub(r'\s+', ' ', current_row[-1]).strip()  # Limpiar espacios adicionales
                data.append(current_row)
            current_row = re.split(r'\s{2,}', line, maxsplit=3)  # Separar en 4 partes máximo
        else:  # Si no empieza con un número, es una continuación de la línea anterior
            current_row[-1] += ' ' + line  # Concatenar la línea al final de la última columna

    # Agregar la última fila
    if current_row:
        current_row[-1] = re.sub(r'\s+', ' ', current_row[-1]).strip()  # Limpiar espacios adicionales
        data.append(current_row)

    # Crear el DataFrame
    df = pd.DataFrame(data, columns=["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"])

    # Limpiar las columnas según las condiciones
    df['principales_palabras_clave'] = (
        df['principales_palabras_clave']
        .str.replace(r'\s*,\s*', ', ')  # Asegurar un solo espacio después de cada coma
        .str.replace(r',\s+', ', ')  # Corregir comas seguidas de múltiples espacios
        .str.replace(r'\.\s*$', '', regex=True)  # Eliminar punto final si existe
        .str.strip()  # Eliminar espacios iniciales y finales
    )

    # Convertir las columnas numéricas
    df['cluster'] = df['cluster'].astype(int)
    df['cantidad_de_palabras_clave'] = df['cantidad_de_palabras_clave'].astype(int)
    df['porcentaje_de_palabras_clave'] = df['porcentaje_de_palabras_clave'].str.replace(',', '.').str.rstrip('%').astype(float)

    # Retornar el DataFrame resultante
    return df