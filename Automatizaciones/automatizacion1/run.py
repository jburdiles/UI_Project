#!/usr/bin/env python3
"""
Automatización 1: Procesador de CSV
Procesa archivos CSV y genera reportes
"""

import os
import sys
import csv
import json
from pathlib import Path

def main(input_csv, output_folder, config_file=None):
    """
    Función principal de la automatización
    
    Args:
        input_csv (str): Ruta del archivo CSV de entrada
        output_folder (str): Ruta de la carpeta de salida
        config_file (str, optional): Ruta del archivo de configuración
    """
    try:
        print(f"🚀 Iniciando procesamiento de CSV...")
        print(f"📁 Archivo de entrada: {input_csv}")
        print(f"📂 Carpeta de salida: {output_folder}")
        
        # Verificar que el archivo de entrada existe
        if not os.path.exists(input_csv):
            raise FileNotFoundError(f"El archivo {input_csv} no existe")
            
        # Crear carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)
        
        # Leer configuración si se proporciona
        config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                print(f"⚙️  Configuración cargada desde: {config_file}")
        
        # Procesar CSV
        data = []
        columns = []
        
        with open(input_csv, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            columns = next(reader)  # Primera fila como headers
            for row in reader:
                data.append(row)
        
        print(f"📊 Datos cargados: {len(data)} filas, {len(columns)} columnas")
        print(f"📋 Columnas: {', '.join(columns)}")
        
        # Aplicar filtros básicos (ejemplo)
        filtered_data = data
        if 'filter_column' in config and 'filter_value' in config:
            filter_col = config['filter_column']
            filter_val = config['filter_value']
            
            if filter_col in columns:
                col_index = columns.index(filter_col)
                filtered_data = [row for row in data if len(row) > col_index and row[col_index] == filter_val]
                print(f"🔍 Filtros aplicados: {len(filtered_data)} filas restantes")
            else:
                print(f"⚠️ Columna de filtro '{filter_col}' no encontrada")
        
        # Generar reporte
        output_file = os.path.join(output_folder, "reporte_procesado.csv")
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(columns)  # Headers
            writer.writerows(filtered_data)  # Datos
        
        # Generar estadísticas
        stats_file = os.path.join(output_folder, "estadisticas.json")
        stats = {
            "filas_originales": len(data),
            "filas_procesadas": len(filtered_data),
            "columnas": columns,
            "archivo_salida": output_file
        }
        
        with open(stats_file, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Procesamiento completado exitosamente")
        print(f"📄 Archivo generado: {output_file}")
        print(f"📈 Estadísticas: {stats_file}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {str(e)}")
        return False

if __name__ == "__main__":
    # Esta parte se ejecuta cuando el script se llama directamente
    if len(sys.argv) < 3:
        print("Uso: python run.py <input_csv> <output_folder> [config_file]")
        sys.exit(1)
    
    input_csv = sys.argv[1]
    output_folder = sys.argv[2]
    config_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = main(input_csv, output_folder, config_file)
    sys.exit(0 if success else 1)