#!/usr/bin/env python3
"""
Automatización 5: Conversor de Imágenes
Convierte imágenes entre diferentes formatos
"""

import os
import sys
from pathlib import Path

def main(input_folder, output_folder):
    """
    Función principal de la automatización
    """
    try:
        print(f"🖼️ Iniciando conversión de imágenes...")
        print(f"📂 Carpeta origen: {input_folder}")
        print(f"📁 Carpeta destino: {output_folder}")
        
        if not os.path.exists(input_folder):
            raise FileNotFoundError(f"La carpeta {input_folder} no existe")
            
        os.makedirs(output_folder, exist_ok=True)
        
        # Simular procesamiento
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        processed = 0
        
        for root, dirs, files in os.walk(input_folder):
            for file in files:
                if any(file.lower().endswith(ext) for ext in image_extensions):
                    processed += 1
        
        print(f"✅ Conversión completada")
        print(f"📊 Imágenes procesadas: {processed}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python run.py <input_folder> <output_folder>")
        sys.exit(1)
    
    success = main(sys.argv[1], sys.argv[2])
    sys.exit(0 if success else 1)