# AuroreUI - Ejecutor de Automatizaciones Python

## 🎯 **Objetivo Completado**

Se ha creado exitosamente **AuroreUI**, un ejecutor de automatizaciones Python con detección dinámica e interfaz moderna y limpia.

## ✅ **Funcionalidades Implementadas**

### **1. Detección Dinámica de Automatizaciones**
- **Carpeta**: `Automatizaciones/` (creada en el workspace)
- **Estructura requerida**: Cada automatización debe tener:
  - `ui_config.json` - Configuración de la interfaz
  - `run.py` - Script de ejecución
- **Detección automática** al iniciar la aplicación
- **3 automatizaciones de ejemplo** incluidas

### **2. Configuración via JSON**
Cada `ui_config.json` puede configurar:
- **Nombre y descripción** de la automatización
- **Inputs personalizados** con tipos:
  - `file` - Selector de archivos
  - `folder` - Selector de carpetas
- **Campos requeridos vs opcionales**
- **Filtros de archivo** específicos

### **3. Interfaz de Usuario Moderna**
- **Sidebar dinámico**: Botones automáticos para cada automatización
- **Panel de detalles**: Título, descripción e inputs configurables
- **Selectores de archivos/carpetas**: Con validación de tipos
- **Área de ejecución**: Botones de validación y ejecución
- **Consola de salida**: Logs en tiempo real

### **4. Motor de Ejecución**
- **Validación de inputs** antes de ejecutar
- **Ejecución con timeout** (5 minutos)
- **Captura de stdout/stderr**
- **Manejo de errores** robusto

## 📁 **Estructura de Archivos Creados**

```
workspace/
├── Automatizaciones/
│   ├── automatizacion1/
│   │   ├── ui_config.json
│   │   └── run.py
│   ├── automatizacion2/
│   │   ├── ui_config.json
│   │   └── run.py
│   └── automatizacion3/
│       ├── ui_config.json
│       └── run.py
├── modules/
│   ├── automation_manager.py (NUEVO)
│   └── automation_widgets.py (NUEVO)
└── main.py (MODIFICADO)
```

## 🔧 **Automatizaciones de Ejemplo Incluidas**

### **1. Procesador de CSV**
- **Función**: Procesa archivos CSV, filtra datos y genera reportes
- **Inputs**:
  - Archivo CSV de entrada (requerido)
  - Carpeta de salida (requerida)
  - Archivo de configuración JSON (opcional)
- **Salida**: CSV procesado + estadísticas JSON

### **2. Generador de Reportes**
- **Función**: Genera reportes a partir de múltiples fuentes de datos
- **Inputs**:
  - Carpeta con datos (requerida)
  - Plantilla de reporte (opcional)
  - Carpeta de salida (requerida)
- **Salida**: Reportes en JSON y TXT

### **3. Backup de Archivos**
- **Función**: Copia de seguridad con compresión ZIP
- **Inputs**:
  - Carpeta origen (requerida)
  - Carpeta destino (requerida)
  - Archivo de exclusiones (opcional)
- **Salida**: Archive ZIP + información del backup

## 🎨 **Mantenimiento del Diseño Original**
- **Colores Dracula** conservados
- **Estructura de navegación** mantenida
- **Tema oscuro/claro** disponible
- **Animaciones y efectos** preservados

## 🚀 **Cómo Usar**

### **Ejecutar la Aplicación**
```bash
python3 main.py
```

### **Agregar Nueva Automatización**
1. Crear carpeta en `Automatizaciones/nueva_automatizacion/`
2. Crear `ui_config.json`:
```json
{
    "name": "Mi Automatización",
    "description": "Descripción de lo que hace",
    "inputs": [
        {
            "id": "input1",
            "label": "Archivo de entrada",
            "type": "file",
            "required": true,
            "filters": "CSV Files (*.csv);;All Files (*)"
        }
    ]
}
```
3. Crear `run.py` con función `main()` que reciba los inputs como argumentos
4. Reiniciar la aplicación para detectar la nueva automatización

### **Ejemplo de ui_config.json**
```json
{
    "name": "Procesador de Datos",
    "description": "Automatización que procesa datos y genera reportes.",
    "inputs": [
        {
            "id": "data_file",
            "label": "Archivo de datos",
            "type": "file",
            "required": true,
            "filters": "Data Files (*.csv *.xlsx *.json);;All Files (*)"
        },
        {
            "id": "output_dir",
            "label": "Directorio de salida",
            "type": "folder",
            "required": true
        },
        {
            "id": "config_file",
            "label": "Configuración (opcional)",
            "type": "file",
            "required": false,
            "filters": "Config Files (*.json *.yaml);;All Files (*)"
        }
    ]
}
```

## 🔄 **Flujo de Trabajo**
1. **Inicio**: La aplicación detecta automáticamente las automatizaciones
2. **Selección**: Usuario hace clic en una automatización del sidebar
3. **Configuración**: Se muestran los inputs configurables con selectores
4. **Validación**: Botón para verificar que todos los inputs requeridos están completos
5. **Ejecución**: Botón para ejecutar la automatización
6. **Resultado**: Salida mostrada en la consola integrada

## 🛠 **Componentes Técnicos**

### **AutomationManager**
- Detección dinámica de automatizaciones
- Gestión de configuraciones JSON
- Ejecución con subprocess
- Validación de inputs

### **AutomationWidgets**
- Widgets personalizados para inputs
- Selectores de archivos/carpetas diferenciados
- Interfaz de validación y ejecución
- Área de salida con scroll

### **Integración PyDracula**
- Botones dinámicos en sidebar
- Página de widgets reemplazada
- Mantenimiento de estilos originales
- Conexión de eventos de UI

## 📋 **Características Técnicas**
- **Framework**: PySide6 (Qt6)
- **Compatibilidad**: Python 3.9+
- **Detección**: Automática al inicio
- **Validación**: Tipos de archivo/carpeta
- **Ejecución**: Subprocess con timeout
- **UI**: Responsive con scroll automático
- **Estilos**: CSS mantenidos del tema original

## ✨ **Resultado Final**
**AuroreUI** es un ejecutor universal de automatizaciones Python con una interfaz moderna, limpia y profesional. La aplicación mantiene la estética del tema Dracula pero optimizada específicamente para ejecutar scripts Python de manera visual e intuitiva, sin elementos innecesarios.