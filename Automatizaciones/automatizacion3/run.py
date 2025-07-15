#!/usr/bin/env python3
"""
Automatización 3: Backup de Archivos
Realiza copias de seguridad con compresión
"""

import os
import sys
import shutil
import zipfile
import datetime
from pathlib import Path

def main(source_folder, backup_folder, exclude_file=None):
    """
    Función principal de la automatización
    
    Args:
        source_folder (str): Ruta de la carpeta origen
        backup_folder (str): Ruta de la carpeta destino del backup
        exclude_file (str, optional): Archivo con patrones a excluir
    """
    try:
            print(f"Starting file backup...")
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {backup_folder}")
        
        # Verificar que la carpeta origen existe
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"Source folder {source_folder} does not exist")
            
        # Crear carpeta de backup si no existe
        os.makedirs(backup_folder, exist_ok=True)
        
        # Leer patrones de exclusión si se proporciona el archivo
        exclude_patterns = []
        if exclude_file and os.path.exists(exclude_file):
            with open(exclude_file, 'r', encoding='utf-8') as f:
                exclude_patterns = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            print(f"🚫 Patrones de exclusión cargados: {len(exclude_patterns)}")
        
        # Generar nombre del backup con timestamp
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"backup_{Path(source_folder).name}_{timestamp}"
        backup_zip = os.path.join(backup_folder, f"{backup_name}.zip")
        
        # Contar archivos a procesar
        total_files = 0
        for root, dirs, files in os.walk(source_folder):
            total_files += len(files)
        
        print(f"Files to process: {total_files}")
        
        # Crear archivo ZIP
        with zipfile.ZipFile(backup_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
            processed = 0
            for root, dirs, files in os.walk(source_folder):
                # Filtrar directorios y archivos según patrones de exclusión
                if exclude_patterns:
                    dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
                    files = [f for f in files if not any(pattern in f for pattern in exclude_patterns)]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    arc_name = os.path.relpath(file_path, source_folder)
                    
                    try:
                        zipf.write(file_path, arc_name)
                        processed += 1
                        if processed % 100 == 0:
                            print(f"Processed: {processed}/{total_files} files")
                    except Exception as e:
                        print(f"Warning: Error processing {file_path}: {str(e)}")
        
        # Generar información del backup
        backup_info = {
            "timestamp": timestamp,
            "source_folder": source_folder,
            "backup_file": backup_zip,
            "files_processed": processed,
            "backup_size_mb": round(os.path.getsize(backup_zip) / (1024*1024), 2),
            "exclude_patterns": exclude_patterns
        }
        
        # Guardar información del backup
        info_file = os.path.join(backup_folder, f"{backup_name}_info.json")
        import json
        with open(info_file, 'w', encoding='utf-8') as f:
            json.dump(backup_info, f, indent=2, ensure_ascii=False)
        
        print(f"Backup completed successfully")
        print(f"Backup file: {backup_zip}")
        print(f"Information: {info_file}")
        print(f"Files processed: {processed}")
        print(f"Backup size: {backup_info['backup_size_mb']} MB")
        
        return True
        
    except Exception as e:
        print(f"Error during backup: {str(e)}")
        return False

if __name__ == "__main__":
    # Esta parte se ejecuta cuando el script se llama directamente
    if len(sys.argv) < 3:
        print("Uso: python run.py <source_folder> <backup_folder> [exclude_file]")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    backup_folder = sys.argv[2]
    exclude_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = main(source_folder, backup_folder, exclude_file)
    sys.exit(0 if success else 1)