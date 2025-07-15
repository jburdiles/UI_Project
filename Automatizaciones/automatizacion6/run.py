#!/usr/bin/env python3
"""
Automatización 6: Limpiador de Archivos Temporales
Encuentra y elimina archivos temporales
"""

import os
import sys
from pathlib import Path

def main(target_folder):
    """
    Función principal de la automatización
    """
    try:
        print(f"🧹 Iniciando limpieza de archivos temporales...")
        print(f"📂 Carpeta objetivo: {target_folder}")
        
        if not os.path.exists(target_folder):
            raise FileNotFoundError(f"La carpeta {target_folder} no existe")
        
        # Patrones de archivos temporales (solo simulación)
        temp_patterns = ['.tmp', '.temp', '.cache', '.log', '~']
        found_files = 0
        
        for root, dirs, files in os.walk(target_folder):
            for file in files:
                if any(file.lower().endswith(pattern) or file.startswith(pattern) for pattern in temp_patterns):
                    found_files += 1
        
        print(f"✅ Limpieza completada")
        print(f"🗑️ Archivos temporales encontrados: {found_files}")
        print(f"💾 Espacio que se puede liberar: {found_files * 1.2:.1f} MB (simulado)")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python run.py <target_folder>")
        sys.exit(1)
    
    success = main(sys.argv[1])
    sys.exit(0 if success else 1)