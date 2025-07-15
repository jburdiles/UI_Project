#!/usr/bin/env python3
"""
Automatización 4: Organizador de Archivos
Organiza archivos por tipo en carpetas específicas
"""

import os
import sys
import shutil
from pathlib import Path

def main(source_folder, destination_folder):
    """
    Función principal de la automatización
    
    Args:
        source_folder (str): Ruta de la carpeta a organizar
        destination_folder (str): Ruta de la carpeta destino
    """
    try:
            print(f"Starting file organization...")
    print(f"Source folder: {source_folder}")
    print(f"Destination folder: {destination_folder}")
        
        # Verificar que la carpeta origen existe
        if not os.path.exists(source_folder):
            raise FileNotFoundError(f"Source folder {source_folder} does not exist")
            
        # Crear carpeta destino si no existe
        os.makedirs(destination_folder, exist_ok=True)
        
        # Definir categorías de archivos
        file_categories = {
            'Imágenes': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
            'Documentos': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt'],
            'Hojas de Cálculo': ['.xls', '.xlsx', '.csv', '.ods'],
            'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
            'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma'],
            'Archivos': ['.zip', '.rar', '.7z', '.tar', '.gz'],
            'Código': ['.py', '.js', '.html', '.css', '.php', '.cpp', '.java'],
            'Ejecutables': ['.exe', '.msi', '.deb', '.rpm', '.dmg']
        }
        
        # Contadores
        organized_files = 0
        total_files = 0
        
        # Contar archivos totales
        for root, dirs, files in os.walk(source_folder):
            total_files += len(files)
        
        print(f"Total files to process: {total_files}")
        
        # Procesar archivos
        for root, dirs, files in os.walk(source_folder):
            for file in files:
                file_path = os.path.join(root, file)
                file_ext = Path(file).suffix.lower()
                
                # Determinar categoría
                category = 'Otros'
                for cat_name, extensions in file_categories.items():
                    if file_ext in extensions:
                        category = cat_name
                        break
                
                # Crear carpeta de categoría
                category_folder = os.path.join(destination_folder, category)
                os.makedirs(category_folder, exist_ok=True)
                
                # Mover archivo
                try:
                    dest_path = os.path.join(category_folder, file)
                    
                    # Si ya existe, agregar número
                    counter = 1
                    original_dest = dest_path
                    while os.path.exists(dest_path):
                        name, ext = os.path.splitext(original_dest)
                        dest_path = f"{name}_{counter}{ext}"
                        counter += 1
                    
                    shutil.move(file_path, dest_path)
                    organized_files += 1
                    
                    if organized_files % 10 == 0:
                        print(f"Organized: {organized_files}/{total_files} files")
                        
                except Exception as e:
                    print(f"Warning: Error moving {file}: {str(e)}")
        
        # Generar resumen
        print(f"Organization completed successfully")
        print(f"Files organized: {organized_files}")
        print(f"Folders created by category:")
        
        for category in file_categories.keys():
            category_path = os.path.join(destination_folder, category)
            if os.path.exists(category_path):
                file_count = len(os.listdir(category_path))
                if file_count > 0:
                    print(f"  - {category}: {file_count} archivos")
        
        return True
        
    except Exception as e:
        print(f"Error during organization: {str(e)}")
        return False

if __name__ == "__main__":
    # Esta parte se ejecuta cuando el script se llama directamente
    if len(sys.argv) < 3:
        print("Uso: python run.py <source_folder> <destination_folder>")
        sys.exit(1)
    
    source_folder = sys.argv[1]
    destination_folder = sys.argv[2]
    
    success = main(source_folder, destination_folder)
    sys.exit(0 if success else 1)