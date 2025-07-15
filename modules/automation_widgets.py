"""
Automation Widgets
Widgets personalizados para la interfaz de automatizaciones
"""

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QLineEdit, QFrame, QScrollArea, QTextEdit, QSizePolicy,
    QFileDialog, QMessageBox
)
from PySide6.QtGui import QFont

class AutomationInputWidget(QFrame):
    """Widget para un input específico de automatización"""
    
    pathChanged = Signal(str, str)  # input_id, path
    
    def __init__(self, input_config, parent=None):
        super().__init__(parent)
        self.input_config = input_config
        self.current_path = ""
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del widget"""
        self.setFrameStyle(QFrame.Box)
        self.setStyleSheet("""
            QFrame {
                background-color: rgb(44, 49, 58);
                border: 1px solid rgb(60, 65, 75);
                border-radius: 5px;
                padding: 5px;
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        
        # Etiqueta del input
        label_text = self.input_config['label']
        if self.input_config.get('required', False):
            label_text += " *"
        
        self.label = QLabel(label_text)
        self.label.setStyleSheet("""
            QLabel {
                color: rgb(255, 255, 255);
                font-weight: bold;
                font-size: 12px;
                border: none;
                background: transparent;
            }
        """)
        layout.addWidget(self.label)
        
        # Layout horizontal para el campo de texto y botón
        input_layout = QHBoxLayout()
        
        # Campo de texto para mostrar la ruta seleccionada
        self.path_edit = QLineEdit()
        self.path_edit.setReadOnly(True)
        self.path_edit.setPlaceholderText(f"Selecciona un {'archivo' if self.input_config.get('type') == 'file' else 'carpeta'}...")
        self.path_edit.setStyleSheet("""
            QLineEdit {
                background-color: rgb(33, 37, 43);
                border: 1px solid rgb(60, 65, 75);
                border-radius: 3px;
                padding: 8px;
                color: rgb(221, 221, 221);
                font-size: 11px;
            }
            QLineEdit:focus {
                border: 2px solid rgb(255, 121, 198);
            }
        """)
        input_layout.addWidget(self.path_edit)
        
        # Botón para seleccionar archivo/carpeta
        self.browse_btn = QPushButton("Explorar")
        self.browse_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(255, 121, 198);
                border: none;
                border-radius: 3px;
                padding: 8px 12px;
                color: rgb(255, 255, 255);
                font-weight: bold;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: rgb(255, 131, 208);
            }
            QPushButton:pressed {
                background-color: rgb(245, 111, 188);
            }
        """)
        self.browse_btn.clicked.connect(self.browse_path)
        input_layout.addWidget(self.browse_btn)
        
        layout.addLayout(input_layout)
        
        # Información adicional del tipo
        type_info = "Archivo" if self.input_config.get('type') == 'file' else "Carpeta"
        if not self.input_config.get('required', False):
            type_info += " (Opcional)"
        
        info_label = QLabel(type_info)
        info_label.setStyleSheet("""
            QLabel {
                color: rgb(150, 150, 150);
                font-size: 10px;
                border: none;
                background: transparent;
            }
        """)
        layout.addWidget(info_label)
    
    def browse_path(self):
        """Abre el diálogo de selección de archivo/carpeta"""
        input_type = self.input_config.get('type', 'file')
        filters = self.input_config.get('filters', 'All Files (*)')
        
        if input_type == 'folder':
            path = QFileDialog.getExistingDirectory(
                self,
                f"Seleccionar carpeta - {self.input_config['label']}",
                self.current_path
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                f"Seleccionar archivo - {self.input_config['label']}",
                self.current_path,
                filters
            )
        
        if path:
            self.set_path(path)
    
    def set_path(self, path):
        """Establece la ruta seleccionada"""
        self.current_path = path
        self.path_edit.setText(path)
        self.pathChanged.emit(self.input_config['id'], path)
    
    def get_path(self):
        """Retorna la ruta actual"""
        return self.current_path
    
    def is_valid(self):
        """Verifica si el input es válido"""
        if self.input_config.get('required', False):
            return bool(self.current_path.strip())
        return True


class AutomationDetailsWidget(QWidget):
    """Widget principal para mostrar detalles de una automatización"""
    
    executeRequested = Signal(dict)  # inputs dict
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_automation = None
        self.input_widgets = {}
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz principal"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Área de scroll para los contenidos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background-color: rgb(44, 49, 58);
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background-color: rgb(255, 121, 198);
                border-radius: 6px;
                min-height: 20px;
            }
        """)
        
        # Widget contenedor dentro del scroll
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setSpacing(15)
        
        # Título de la automatización
        self.title_label = QLabel("Selecciona una automatización")
        self.title_label.setStyleSheet("""
            QLabel {
                color: rgb(255, 255, 255);
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: rgb(44, 49, 58);
                border-radius: 5px;
            }
        """)
        self.content_layout.addWidget(self.title_label)
        
        # Descripción
        self.description_label = QLabel("Selecciona una automatización del menú lateral para ver sus detalles.")
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet("""
            QLabel {
                color: rgb(200, 200, 200);
                font-size: 12px;
                padding: 10px;
                background-color: rgb(33, 37, 43);
                border-radius: 5px;
                line-height: 1.4;
            }
        """)
        self.content_layout.addWidget(self.description_label)
        
        # Contenedor para inputs
        self.inputs_container = QWidget()
        self.inputs_layout = QVBoxLayout(self.inputs_container)
        self.inputs_layout.setSpacing(10)
        self.content_layout.addWidget(self.inputs_container)
        
        # Botones de acción
        self.create_action_buttons()
        
        # Área de salida/logs
        self.create_output_area()
        
        scroll_area.setWidget(self.content_widget)
        layout.addWidget(scroll_area)
    
    def create_action_buttons(self):
        """Crea los botones de acción"""
        buttons_layout = QHBoxLayout()
        
        # Botón de validar inputs
        self.validate_btn = QPushButton("Validar Inputs")
        self.validate_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(80, 150, 255);
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                color: rgb(255, 255, 255);
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgb(90, 160, 255);
            }
            QPushButton:pressed {
                background-color: rgb(70, 140, 245);
            }
        """)
        self.validate_btn.clicked.connect(self.validate_inputs)
        buttons_layout.addWidget(self.validate_btn)
        
        # Botón de ejecutar
        self.execute_btn = QPushButton("Ejecutar Automatización")
        self.execute_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(80, 250, 123);
                border: none;
                border-radius: 5px;
                padding: 12px 20px;
                color: rgb(0, 0, 0);
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: rgb(90, 255, 133);
            }
            QPushButton:pressed {
                background-color: rgb(70, 240, 113);
            }
            QPushButton:disabled {
                background-color: rgb(60, 65, 75);
                color: rgb(150, 150, 150);
            }
        """)
        self.execute_btn.clicked.connect(self.execute_automation)
        buttons_layout.addWidget(self.execute_btn)
        
        self.content_layout.addLayout(buttons_layout)
        
        # Inicialmente deshabilitar botones
        self.validate_btn.setEnabled(False)
        self.execute_btn.setEnabled(False)
    
    def create_output_area(self):
        """Crea el área de salida para logs"""
        output_label = QLabel("Salida de la automatización:")
        output_label.setStyleSheet("""
            QLabel {
                color: rgb(255, 255, 255);
                font-size: 14px;
                font-weight: bold;
                padding: 5px;
            }
        """)
        self.content_layout.addWidget(output_label)
        
        self.output_text = QTextEdit()
        self.output_text.setMaximumHeight(200)
        self.output_text.setReadOnly(True)
        self.output_text.setStyleSheet("""
            QTextEdit {
                background-color: rgb(20, 22, 26);
                border: 1px solid rgb(60, 65, 75);
                border-radius: 5px;
                padding: 10px;
                color: rgb(255, 255, 255);
                font-family: 'Consolas', 'Monaco', monospace;
                font-size: 11px;
            }
        """)
        self.content_layout.addWidget(self.output_text)
    
    def set_automation(self, automation):
        """Establece la automatización a mostrar"""
        self.current_automation = automation
        self.clear_inputs()
        
        # Actualizar título y descripción
        self.title_label.setText(automation['name'])
        self.description_label.setText(automation['description'])
        
        # Crear inputs
        self.create_input_widgets(automation['inputs'])
        
        # Habilitar botones
        self.validate_btn.setEnabled(True)
        self.execute_btn.setEnabled(True)
        
        # Limpiar salida
        self.output_text.clear()
    
    def create_input_widgets(self, inputs_config):
        """Crea los widgets para los inputs de la automatización"""
        if inputs_config:
            inputs_label = QLabel("Configurar parámetros:")
            inputs_label.setStyleSheet("""
                QLabel {
                    color: rgb(255, 255, 255);
                    font-size: 14px;
                    font-weight: bold;
                    padding: 5px;
                }
            """)
            self.inputs_layout.addWidget(inputs_label)
        
        for input_config in inputs_config:
            input_widget = AutomationInputWidget(input_config)
            input_widget.pathChanged.connect(self.on_input_changed)
            self.input_widgets[input_config['id']] = input_widget
            self.inputs_layout.addWidget(input_widget)
    
    def clear_inputs(self):
        """Limpia todos los inputs existentes"""
        for widget in self.input_widgets.values():
            widget.deleteLater()
        self.input_widgets.clear()
        
        # Limpiar layout
        while self.inputs_layout.count():
            child = self.inputs_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
    
    def on_input_changed(self, input_id, path):
        """Maneja el cambio en un input"""
        print(f"Input {input_id} cambiado a: {path}")
    
    def validate_inputs(self):
        """Valida todos los inputs"""
        if not self.current_automation:
            return
        
        errors = []
        
        for input_widget in self.input_widgets.values():
            if not input_widget.is_valid():
                errors.append(f"- {input_widget.input_config['label']}")
        
        if errors:
            error_msg = "Los siguientes campos son requeridos:\n\n" + "\n".join(errors)
            QMessageBox.warning(self, "Inputs inválidos", error_msg)
            self.output_text.setPlainText("❌ Validación fallida: Hay inputs requeridos sin completar")
        else:
            self.output_text.setPlainText("✅ Todos los inputs son válidos")
    
    def execute_automation(self):
        """Ejecuta la automatización"""
        if not self.current_automation:
            return
        
        # Recolectar inputs
        inputs = {}
        for input_id, input_widget in self.input_widgets.items():
            path = input_widget.get_path()
            if path:
                inputs[input_id] = path
        
        # Validar antes de ejecutar
        valid = True
        for input_widget in self.input_widgets.values():
            if not input_widget.is_valid():
                valid = False
                break
        
        if not valid:
            self.validate_inputs()
            return
        
        self.output_text.setPlainText("🚀 Ejecutando automatización...\n")
        self.executeRequested.emit(inputs)
    
    def append_output(self, text):
        """Agrega texto al área de salida"""
        self.output_text.append(text)
    
    def set_output(self, text):
        """Establece el texto completo del área de salida"""
        self.output_text.setPlainText(text)