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

        # LEFT MENUS  
        widgets.btn_widgets.clicked.connect(self.buttonClick)
        widgets.btn_new.clicked.connect(self.buttonClick)
        widgets.btn_save.clicked.connect(self.buttonClick)
        
        # HIDE HOME BUTTON
        widgets.btn_home.hide()

        # SETUP AUTOMATION BUTTONS
        # ///////////////////////////////////////////////////////////////
        self.setup_automation_buttons()

        # HIDE LEFT BOX AND SETTINGS BUTTON
        widgets.toggleLeftBox.hide()
        widgets.settingsTopBtn.hide()

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
        if automations and len(automations) > 0:
            # Show first automation by default
            self.show_automation_details(automations[0]['id'])
            widgets.btn_widgets.setStyleSheet(UIFunctions.selectMenu(widgets.btn_widgets.styleSheet()))
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
            
            print("✅ Widgets de automatización configurados")
            
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
                    btn.deleteLater()
            
            self.automation_buttons = []
            
            # Crear botones para cada automatización
            automations = self.automation_manager.get_automations()
            
            if not automations:
                print("⚠️  No se encontraron automatizaciones")
                return
            
            # Cambiar etiquetas de los botones existentes
            if len(automations) > 0:
                widgets.btn_widgets.setText(automations[0]['name'])
                widgets.btn_widgets.automation_id = automations[0]['id']
                
            if len(automations) > 1:
                widgets.btn_new.setText(automations[1]['name'])
                widgets.btn_new.automation_id = automations[1]['id']
                
            if len(automations) > 2:
                widgets.btn_save.setText(automations[2]['name'])
                widgets.btn_save.automation_id = automations[2]['id']
                
            print(f"✅ Configurados botones para {len(automations)} automatizaciones")
            
        except Exception as e:
            print(f"❌ Error configurando botones de automatización: {str(e)}")

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
        
        print(f"🚀 Ejecutando automatización: {current['name']}")
        print(f"📊 Inputs: {inputs}")
        
        # Ejecutar la automatización
        success, output = self.automation_manager.execute_automation(current['id'], inputs)
        
        # Actualizar la salida en el widget
        if success:
            result_text = f"✅ Automatización ejecutada exitosamente\n\n{output}"
        else:
            result_text = f"❌ Error ejecutando automatización\n\n{output}"
        
        self.automation_details_widget.set_output(result_text)

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
            print(f"📁 Seleccionado: {path}")


    # BUTTONS CLICK
    # Post here your functions for clicked buttons
    # ///////////////////////////////////////////////////////////////
    def buttonClick(self):
        # GET BUTTON CLICKED
        btn = self.sender()
        btnName = btn.objectName()

        # SHOW AUTOMATION PAGES
        if btnName in ["btn_widgets", "btn_new", "btn_save"]:
            # Check if button has automation_id attribute
            if hasattr(btn, 'automation_id'):
                self.show_automation_details(btn.automation_id)
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))
            else:
                # Fallback to original behavior
                if btnName == "btn_widgets":
                    widgets.stackedWidget.setCurrentWidget(widgets.widgets)
                elif btnName == "btn_new":
                    widgets.stackedWidget.setCurrentWidget(widgets.new_page)
                elif btnName == "btn_save":
                    print("Save BTN clicked!")
                    
                UIFunctions.resetStyle(self, btnName)
                btn.setStyleSheet(UIFunctions.selectMenu(btn.styleSheet()))

        # PRINT BTN NAME
        print(f'Button "{btnName}" pressed!')


    # RESIZE EVENTS
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        # Update Size Grips
        UIFunctions.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

        # PRINT MOUSE EVENTS
        if event.buttons() == Qt.LeftButton:
            print('Mouse click: LEFT CLICK')
        if event.buttons() == Qt.RightButton:
            print('Mouse click: RIGHT CLICK')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()
    sys.exit(app.exec_())
