"""
Automation Manager
Gestiona la detección y ejecución de automatizaciones Python
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import List, Dict, Optional

class AutomationManager:
    def __init__(self, automations_folder: str = "Automatizaciones"):
        """
        Inicializa el gestor de automatizaciones
        
        Args:
            automations_folder: Ruta de la carpeta que contiene las automatizaciones
        """
        self.automations_folder = automations_folder
        self.automations = []
        self.current_automation = None
        self.load_automations()
    
    def load_automations(self) -> List[Dict]:
        """
        Carga dinámicamente todas las automatizaciones disponibles
        
        Returns:
            Lista de diccionarios con información de las automatizaciones
        """
        self.automations = []
        
        if not os.path.exists(self.automations_folder):
            print(f"⚠️  Carpeta de automatizaciones no encontrada: {self.automations_folder}")
            return self.automations
        
        # Buscar subcarpetas que contengan ui_config.json y run.py
        for item in os.listdir(self.automations_folder):
            automation_path = os.path.join(self.automations_folder, item)
            
            if os.path.isdir(automation_path):
                config_file = os.path.join(automation_path, "ui_config.json")
                run_file = os.path.join(automation_path, "run.py")
                
                if os.path.exists(config_file) and os.path.exists(run_file):
                    try:
                        # Cargar configuración
                        with open(config_file, 'r', encoding='utf-8') as f:
                            config = json.load(f)
                        
                        automation_info = {
                            "id": item,
                            "folder": automation_path,
                            "config_file": config_file,
                            "run_file": run_file,
                            "name": config.get("name", item),
                            "description": config.get("description", "Sin descripción"),
                            "inputs": config.get("inputs", [])
                        }
                        
                        self.automations.append(automation_info)
                        print(f"✅ Automatización cargada: {automation_info['name']}")
                        
                    except Exception as e:
                        print(f"❌ Error cargando automatización en {item}: {str(e)}")
        
        print(f"📋 Total de automatizaciones cargadas: {len(self.automations)}")
        return self.automations
    
    def get_automations(self) -> List[Dict]:
        """
        Retorna la lista de automatizaciones disponibles
        """
        return self.automations
    
    def get_automation_by_id(self, automation_id: str) -> Optional[Dict]:
        """
        Obtiene una automatización específica por su ID
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            Diccionario con información de la automatización o None
        """
        for automation in self.automations:
            if automation["id"] == automation_id:
                return automation
        return None
    
    def set_current_automation(self, automation_id: str) -> bool:
        """
        Establece la automatización actual
        
        Args:
            automation_id: ID de la automatización
            
        Returns:
            True si se pudo establecer, False en caso contrario
        """
        automation = self.get_automation_by_id(automation_id)
        if automation:
            self.current_automation = automation
            return True
        return False
    
    def get_current_automation(self) -> Optional[Dict]:
        """
        Retorna la automatización actualmente seleccionada
        """
        return self.current_automation
    
    def execute_automation(self, automation_id: str, inputs: Dict[str, str]) -> tuple:
        """
        Ejecuta una automatización con los inputs proporcionados
        
        Args:
            automation_id: ID de la automatización a ejecutar
            inputs: Diccionario con los valores de entrada {input_id: path}
            
        Returns:
            Tupla (success: bool, output: str)
        """
        automation = self.get_automation_by_id(automation_id)
        if not automation:
            return False, f"Automatización {automation_id} no encontrada"
        
        try:
            # Preparar argumentos para el script
            run_file = automation["run_file"]
            args = [sys.executable, run_file]
            
            # Validar inputs requeridos
            for input_config in automation["inputs"]:
                input_id = input_config["id"]
                is_required = input_config.get("required", False)
                
                if is_required and (input_id not in inputs or not inputs[input_id]):
                    return False, f"Input requerido faltante: {input_config['label']}"
                
                if input_id in inputs and inputs[input_id]:
                    args.append(inputs[input_id])
                else:
                    args.append("")  # Parámetro opcional vacío
            
            print(f"🚀 Ejecutando: {' '.join(args)}")
            
            # Ejecutar el script
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutos de timeout
                cwd=automation["folder"]
            )
            
            output = result.stdout
            if result.stderr:
                output += f"\n--- ERRORES ---\n{result.stderr}"
            
            success = result.returncode == 0
            
            if success:
                print(f"✅ Automatización {automation_id} ejecutada exitosamente")
            else:
                print(f"❌ Error ejecutando automatización {automation_id}")
            
            return success, output
            
        except subprocess.TimeoutExpired:
            return False, "⏰ Timeout: La automatización tardó más de 5 minutos en ejecutarse"
        except Exception as e:
            return False, f"❌ Error inesperado: {str(e)}"
    
    def validate_input_path(self, input_config: Dict, path: str) -> tuple:
        """
        Valida que un path sea válido según la configuración del input
        
        Args:
            input_config: Configuración del input
            path: Ruta a validar
            
        Returns:
            Tupla (is_valid: bool, message: str)
        """
        if not path:
            if input_config.get("required", False):
                return False, f"Campo requerido: {input_config['label']}"
            return True, ""
        
        if not os.path.exists(path):
            return False, f"La ruta no existe: {path}"
        
        input_type = input_config.get("type", "file")
        
        if input_type == "file" and not os.path.isfile(path):
            return False, f"Se esperaba un archivo, pero es una carpeta: {path}"
        
        if input_type == "folder" and not os.path.isdir(path):
            return False, f"Se esperaba una carpeta, pero es un archivo: {path}"
        
        return True, "Ruta válida"
    
    def reload_automations(self):
        """
        Recarga las automatizaciones desde el disco
        """
        print("🔄 Recargando automatizaciones...")
        self.load_automations()