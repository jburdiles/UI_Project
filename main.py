# ///////////////////////////////////////////////////////////////
#
# AuroreUI - Python Automation Runner
# Modern GUI for executing Python automations
#
# ///////////////////////////////////////////////////////////////

import sys
import os
import platform

# IMPORT / GUI AND MODULES AND WIDGETS
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
from PySide6.QtWidgets import QVBoxLayout, QWidget
os.environ["QT_FONT_DPI"] = "96" # FIX Problem for High DPI and Scale above 100%

# SET AS GLOBAL WIDGETS
# ///////////////////////////////////////////////////////////////
widgets = None

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        # SET AS GLOBAL WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        global widgets
        widgets = self.ui

        # INITIALIZE AUTOMATION MANAGER
        # ///////////////////////////////////////////////////////////////
        self.automation_manager = AutomationManager()
        self.current_inputs = {}  # Store current automation inputs
        
        # SETUP AUTOMATION WIDGETS
        # ///////////////////////////////////////////////////////////////
        self.setup_automation_widgets()

        # USE CUSTOM TITLE BAR | USE AS "False" FOR MAC OR LINUX
        # ///////////////////////////////////////////////////////////////
        Settings.ENABLE_CUSTOM_TITLE_BAR = True

        # APP NAME
        # ///////////////////////////////////////////////////////////////
        title = "AuroreUI"
        description = ""
        # APPLY TEXTS
        self.setWindowTitle(title)
        widgets.titleRightInfo.setText(description)

        # TOGGLE MENU
        # ///////////////////////////////////////////////////////////////
        widgets.toggleButton.clicked.connect(lambda: UIFunctions.toggleMenu(self, True))

        # SET UI DEFINITIONS
        # ///////////////////////////////////////////////////////////////
        UIFunctions.uiDefinitions(self)

        # QTableWidget PARAMETERS
        # ///////////////////////////////////////////////////////////////
        widgets.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # BUTTONS CLICK
        # ///////////////////////////////////////////////////////////////

        # HIDE ORIGINAL BUTTONS - We'll create dynamic ones
        widgets.btn_home.hide()
        widgets.btn_widgets.hide()
        widgets.btn_new.hide()
        widgets.btn_save.hide()

        # SETUP AUTOMATION BUTTONS
        # ///////////////////////////////////////////////////////////////
        self.setup_automation_buttons()

        # HIDE LEFT BOX AND SETTINGS BUTTON
        widgets.toggleLeftBox.hide()
        widgets.settingsTopBtn.hide()
        
        # HIDE EXIT BUTTON AND REORGANIZE TOP BUTTONS
        widgets.btn_exit.hide()
        
        # REORGANIZE TOP BUTTONS - Hide first, then close (removing exit)
        # Simply hide the exit button without reorganizing the entire layout
        # This is safer and avoids layout conflicts
        if hasattr(widgets, 'btn_exit'):
            widgets.btn_exit.hide()
        
        # Ensure minimize button is visible and first (if it exists)
        if hasattr(widgets, 'minimizeAppBtn'):
            widgets.minimizeAppBtn.show()
            # Move minimize to front by reparenting if needed
            parent = widgets.minimizeAppBtn.parent()
            if parent and parent.layout():
                parent.layout().removeWidget(widgets.minimizeAppBtn)
                parent.layout().insertWidget(0, widgets.minimizeAppBtn)

        # KEYBOARD SHORTCUTS
        # ///////////////////////////////////////////////////////////////
        # F5 to reload automations
        from PySide6.QtGui import QShortcut, QKeySequence
        reload_shortcut = QShortcut(QKeySequence("F5"), self)
        reload_shortcut.activated.connect(self.reload_automations)

        # SHOW APP
        # ///////////////////////////////////////////////////////////////
        self.show()

        # SET CUSTOM THEME
        # ///////////////////////////////////////////////////////////////
        useCustomTheme = False
        themeFile = "themes/py_dracula_light.qss"

        # SET THEME AND HACKS
        if useCustomTheme:
            # LOAD AND APPLY STYLE
            UIFunctions.theme(self, themeFile, True)

            # SET HACKS
            AppFunctions.setThemeHack(self)

        # SET DEFAULT PAGE - Show first automation if available
        # ///////////////////////////////////////////////////////////////
        automations = self.automation_manager.get_automations()
        if automations and len(automations) > 0 and hasattr(self, 'automation_buttons') and self.automation_buttons:
            # Show first automation by default and select its button
            self.show_automation_details(automations[0]['id'])
            if self.automation_buttons:
                first_btn = self.automation_buttons[0]
                first_btn.setStyleSheet("""
                    QPushButton {
                        background-image: none;
                        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
                        background-color: rgb(40, 44, 52);
                        border: none;
                        background-repeat: none;
                        color: rgb(221, 221, 221);
                        font: 12pt "Segoe UI";
                        padding: 12px 20px;
                        text-align: left;
                    }
                """)
        else:
            # Fallback to widgets page
            widgets.stackedWidget.setCurrentWidget(widgets.widgets)

    def setup_automation_widgets(self):
        """
        Configura los widgets personalizados para automatizaciones
        """
        try:
            # Crear el widget de detalles de automatización
            self.automation_details_widget = AutomationDetailsWidget()
            self.automation_details_widget.executeRequested.connect(self.on_automation_execute_requested)
            self.automation_details_widget.executeAsyncRequested.connect(self.on_automation_execute_async_requested)
            
            # Reemplazar el contenido de la página de widgets
            # Limpiar el layout existente de la página de widgets
            widgets_page = widgets.widgets
            if widgets_page.layout():
                while widgets_page.layout().count():
                    child = widgets_page.layout().takeAt(0)
                    if child.widget():
                        child.widget().hide()
            else:
                # Crear layout si no existe
                from PySide6.QtWidgets import QVBoxLayout
                layout = QVBoxLayout()
                widgets_page.setLayout(layout)
            
            # Agregar el widget de automatización
            widgets_page.layout().addWidget(self.automation_details_widget)
            

            
        except Exception as e:
            print(f"❌ Error configurando widgets de automatización: {str(e)}")

    def setup_automation_buttons(self):
        """
        Configura dinámicamente los botones para las automatizaciones
        """
        try:
            # Limpiar botones de automatización existentes
            if hasattr(self, 'automation_buttons'):
                for btn in self.automation_buttons:
                    btn.setParent(None)  # Remove from parent first
                    btn.deleteLater()
                # Clear the list
                self.automation_buttons.clear()
            else:
                self.automation_buttons = []
            
            # Obtener automatizaciones disponibles
            automations = self.automation_manager.get_automations()
            
            if not automations:
                return
            
            # Obtener el contenedor del menú izquierdo
            left_menu_frame = widgets.leftMenuFrame
            
            # Crear botones dinámicamente para cada automatización
            for i, automation in enumerate(automations):
                btn = QPushButton(automation['name'])
                btn.setObjectName(f"btn_automation_{i}")
                btn.automation_id = automation['id']
                btn.setCheckable(True)
                
                # Aplicar el mismo estilo que los botones originales
                btn.setStyleSheet("""
                    QPushButton {
                        background-image: none;
                        background-color: transparent;
                        border: none;
                        border-left: 22px solid transparent;
                        background-repeat: none;
                        color: rgb(221, 221, 221);
                        font: 12pt "Segoe UI";
                        padding: 12px 20px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: rgb(40, 44, 52);
                    }
                    QPushButton:pressed {
                        background-color: rgb(189, 147, 249);
                    }
                """)
                
                # Conectar el evento click
                btn.clicked.connect(self.automation_button_clicked)
                
                # Agregar al layout del menú izquierdo de forma más segura
                # Buscar el layout correcto en la estructura del menú
                menu_layout = None
                
                # Intentar encontrar el layout del menú navegando por la estructura
                for child in widgets.leftMenuFrame.findChildren(QWidget):
                    if child.layout() and child.layout().count() > 0:
                        # Verificar si este layout contiene botones de menú
                        has_menu_buttons = False
                        for j in range(child.layout().count()):
                            item = child.layout().itemAt(j)
                            if item and item.widget():
                                widget_name = item.widget().objectName()
                                if 'btn_' in widget_name or 'Button' in widget_name:
                                    has_menu_buttons = True
                                    break
                        if has_menu_buttons:
                            menu_layout = child.layout()
                            break
                
                # Si encontramos el layout, agregar el botón al final
                if menu_layout:
                    menu_layout.addWidget(btn)
                else:
                    # Fallback: agregar directamente al frame principal
                    if not hasattr(widgets.leftMenuFrame, '_automation_container'):
                        container = QWidget()
                        layout = QVBoxLayout(container)
                        layout.setContentsMargins(0, 0, 0, 0)
                        layout.setSpacing(0)
                        widgets.leftMenuFrame._automation_container = container
                        # Agregar al final del layout principal si existe
                        if widgets.leftMenuFrame.layout():
                            widgets.leftMenuFrame.layout().addWidget(container)
                    
                    widgets.leftMenuFrame._automation_container.layout().addWidget(btn)
                
                self.automation_buttons.append(btn)
            
        except Exception as e:
            print(f"❌ Error configurando botones de automatización: {str(e)}")
    
    def reload_automations(self):
        """
        Recarga las automatizaciones y actualiza la UI dinámicamente
        """
        # Recargar automatizaciones del manager
        self.automation_manager.reload_automations()
        
        # Reconfigurar botones
        self.setup_automation_buttons()
        
        # Si hay automatizaciones, mostrar la primera por defecto
        automations = self.automation_manager.get_automations()
        if automations and len(automations) > 0 and hasattr(self, 'automation_buttons') and self.automation_buttons:
            self.show_automation_details(automations[0]['id'])
            if self.automation_buttons:
                first_btn = self.automation_buttons[0]
                first_btn.setStyleSheet("""
                    QPushButton {
                        background-image: none;
                        border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
                        background-color: rgb(40, 44, 52);
                        border: none;
                        background-repeat: none;
                        color: rgb(221, 221, 221);
                        font: 12pt "Segoe UI";
                        padding: 12px 20px;
                        text-align: left;
                    }
                """)

    def automation_button_clicked(self):
        """
        Maneja el click de los botones de automatización dinámicos
        """
        btn = self.sender()
        if hasattr(btn, 'automation_id'):
            # Resetear estilo de todos los botones de automatización
            for auto_btn in self.automation_buttons:
                auto_btn.setStyleSheet("""
                    QPushButton {
                        background-image: none;
                        background-color: transparent;
                        border: none;
                        border-left: 22px solid transparent;
                        background-repeat: none;
                        color: rgb(221, 221, 221);
                        font: 12pt "Segoe UI";
                        padding: 12px 20px;
                        text-align: left;
                    }
                    QPushButton:hover {
                        background-color: rgb(40, 44, 52);
                    }
                    QPushButton:pressed {
                        background-color: rgb(189, 147, 249);
                    }
                """)
            
            # Aplicar estilo seleccionado al botón actual
            btn.setStyleSheet("""
                QPushButton {
                    background-image: none;
                    border-left: 22px solid qlineargradient(spread:pad, x1:0.034, y1:0, x2:0.216, y2:0, stop:0.499 rgba(255, 121, 198, 255), stop:0.5 rgba(85, 170, 255, 0));
                    background-color: rgb(40, 44, 52);
                    border: none;
                    background-repeat: none;
                    color: rgb(221, 221, 221);
                    font: 12pt "Segoe UI";
                    padding: 12px 20px;
                    text-align: left;
                }
            """)
            
            # Mostrar detalles de la automatización
            self.show_automation_details(btn.automation_id)

    def show_automation_details(self, automation_id):
        """
        Muestra los detalles de una automatización específica
        """
        automation = self.automation_manager.get_automation_by_id(automation_id)
        if not automation:
            return
            
        self.automation_manager.set_current_automation(automation_id)
        
        # Limpiar inputs anteriores
        self.current_inputs = {}
        
        # Actualizar el widget de automatización
        self.automation_details_widget.set_automation(automation)
        
        # Cambiar a la página de widgets
        widgets.stackedWidget.setCurrentWidget(widgets.widgets)



    def on_automation_execute_requested(self, inputs):
        """
        Maneja la solicitud de ejecución desde el widget de automatización
        """
        current = self.automation_manager.get_current_automation()
        if not current:
            print("⚠️  No hay automatización seleccionada")
            return
        

        
        # Ejecutar la automatización
        success, output = self.automation_manager.execute_automation(current['id'], inputs)
        
        # Actualizar la salida en el widget
        if success:
            result_text = f"✅ Automatización ejecutada exitosamente\n\n{output}"
        else:
            result_text = f"❌ Error ejecutando automatización\n\n{output}"
        
        self.automation_details_widget.set_output(result_text)

    def on_automation_execute_async_requested(self, inputs):
        """
        Maneja la solicitud de ejecución asíncrona desde el widget de automatización
        """
        current = self.automation_manager.get_current_automation()
        if not current:
            print("⚠️  No hay automatización seleccionada")
            return
        

        
        # Callback para cuando termine la ejecución
        def on_execution_complete(success, output, execution_id):
            # Actualizar la salida en el widget
            if success:
                result_text = f"✅ Ejecución {execution_id} completada exitosamente\n\n{output}"
            else:
                result_text = f"❌ Error en ejecución {execution_id}\n\n{output}"
            
            self.automation_details_widget.append_output(f"\n--- Resultado {execution_id} ---")
            self.automation_details_widget.append_output(result_text)
            self.automation_details_widget.remove_execution(execution_id)
        
        # Ejecutar la automatización en paralelo
        execution_id = self.automation_manager.execute_automation_async(
            current['id'], 
            inputs, 
            callback=on_execution_complete
        )
        
        # Agregar al tracking del widget
        execution_info = {
            'automation_name': current['name'],
            'execution_id': execution_id,
            'status': 'running'
        }
        self.automation_details_widget.add_execution(execution_id, execution_info)

    def open_file_dialog(self, input_config):
        """
        Abre el diálogo de selección de archivo/carpeta
        """
        input_type = input_config.get('type', 'file')
        filters = input_config.get('filters', 'All Files (*)')
        
        if input_type == 'folder':
            path = QFileDialog.getExistingDirectory(
                self,
                f"Seleccionar carpeta - {input_config['label']}",
                ""
            )
        else:
            path, _ = QFileDialog.getOpenFileName(
                self,
                f"Seleccionar archivo - {input_config['label']}",
                "",
                filters
            )
        
        if path:
            self.current_inputs[input_config['id']] = path


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # Handle any remaining original buttons (if any)
        # Most functionality is now handled by automation_button_clicked




    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPosition().toPoint()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec())
