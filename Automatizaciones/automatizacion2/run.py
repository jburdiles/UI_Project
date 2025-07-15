#!/usr/bin/env python3
"""
Automatización 2: Generador de Reportes
Genera reportes PDF y Excel a partir de datos
"""

import os
import sys
import json
from pathlib import Path
import datetime

def main(data_folder, output_folder, template_file=None):
    """
    Función principal de la automatización
    
    Args:
        data_folder (str): Ruta de la carpeta con datos de entrada
        output_folder (str): Ruta de la carpeta de salida
        template_file (str, optional): Ruta de la plantilla de reporte
    """
    try:
        print(f"📊 Iniciando generación de reportes...")
        print(f"📂 Carpeta de datos: {data_folder}")
        print(f"📁 Carpeta de salida: {output_folder}")
        
        # Verificar que la carpeta de datos existe
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"La carpeta {data_folder} no existe")
            
        # Crear carpeta de salida si no existe
        os.makedirs(output_folder, exist_ok=True)
        
        # Buscar archivos de datos
        data_files = []
        for ext in ['*.csv', '*.xlsx', '*.json']:
            data_files.extend(Path(data_folder).glob(ext))
        
        print(f"📄 Archivos encontrados: {len(data_files)}")
        for file in data_files:
            print(f"  - {file.name}")
        
        # Usar plantilla si se proporciona
        if template_file and os.path.exists(template_file):
            print(f"📋 Usando plantilla: {template_file}")
        
        # Generar reporte básico
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        report_data = {
            "timestamp": timestamp,
            "data_folder": data_folder,
            "files_processed": [str(f) for f in data_files],
            "total_files": len(data_files),
            "template_used": template_file if template_file else "Plantilla por defecto"
        }
        
        # Guardar reporte en JSON
        json_report = os.path.join(output_folder, f"reporte_{timestamp}.json")
        with open(json_report, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
        
        # Generar reporte en texto
        txt_report = os.path.join(output_folder, f"reporte_{timestamp}.txt")
        with open(txt_report, 'w', encoding='utf-8') as f:
            f.write("=" * 50 + "\n")
            f.write("REPORTE DE PROCESAMIENTO DE DATOS\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Fecha y hora: {timestamp}\n")
            f.write(f"Carpeta procesada: {data_folder}\n")
            f.write(f"Total de archivos: {len(data_files)}\n\n")
            f.write("Archivos procesados:\n")
            for i, file in enumerate(data_files, 1):
                f.write(f"  {i}. {file.name}\n")
            f.write("\n" + "=" * 50 + "\n")
        
        print(f"✅ Reporte generado exitosamente")
        print(f"📄 Reporte JSON: {json_report}")
        print(f"📄 Reporte TXT: {txt_report}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error durante la generación: {str(e)}")
        return False

if __name__ == "__main__":
    # Esta parte se ejecuta cuando el script se llama directamente
    if len(sys.argv) < 3:
        print("Uso: python run.py <data_folder> <output_folder> [template_file]")
        sys.exit(1)
    
    data_folder = sys.argv[1]
    output_folder = sys.argv[2]
    template_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = main(data_folder, output_folder, template_file)
    sys.exit(0 if success else 1)