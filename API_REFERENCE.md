# AuroreUI API Reference

## 📋 Table of Contents
1. [Core Classes](#core-classes)
2. [UI Components](#ui-components)
3. [Configuration Schema](#configuration-schema)
4. [Event System](#event-system)
5. [Utility Functions](#utility-functions)

---

## 🏗 Core Classes

### AutomationManager

**Location**: `modules/automation_manager.py`

**Purpose**: Manages automation discovery, loading, validation, and execution.

#### Constructor
```python
def __init__(self, automations_folder: str = "Automatizaciones")
```

**Parameters**:
- `automations_folder` (str): Path to directory containing automation scripts

#### Methods

##### `load_automations() -> List[Dict]`
Scans the automations folder and loads all valid automation configurations.

**Returns**: List of automation dictionaries with structure:
```python
{
    "id": "automation_name",
    "folder": "/path/to/automation",
    "config_file": "/path/to/ui_config.json",
    "run_file": "/path/to/run.py",
    "name": "Display Name",
    "description": "Automation description",
    "inputs": [
        {
            "id": "input_id",
            "label": "Input Label",
            "type": "file|folder",
            "required": bool,
            "filters": "File filters string"
        }
    ]
}
```

##### `get_automations() -> List[Dict]`
Returns all loaded automations.

**Returns**: List of automation dictionaries

##### `get_automation_by_id(automation_id: str) -> Optional[Dict]`
Retrieves a specific automation by its ID.

**Parameters**:
- `automation_id` (str): Unique identifier for the automation

**Returns**: Automation dictionary or None if not found

##### `set_current_automation(automation_id: str) -> bool`
Sets the currently selected automation.

**Parameters**:
- `automation_id` (str): ID of automation to set as current

**Returns**: True if automation was found and set, False otherwise

##### `get_current_automation() -> Optional[Dict]`
Returns the currently selected automation.

**Returns**: Current automation dictionary or None

##### `execute_automation(automation_id: str, inputs: Dict[str, str]) -> tuple`
Executes an automation with provided inputs.

**Parameters**:
- `automation_id` (str): ID of automation to execute
- `inputs` (Dict[str, str]): Dictionary mapping input IDs to file/folder paths

**Returns**: Tuple `(success: bool, output: str)`

**Example**:
```python
success, output = manager.execute_automation(
    "csv_processor",
    {
        "input_file": "/path/to/input.csv",
        "output_folder": "/path/to/output"
    }
)
```

##### `validate_input_path(input_config: Dict, path: str) -> tuple`
Validates a file or folder path against input configuration.

**Parameters**:
- `input_config` (Dict): Input configuration dictionary
- `path` (str): File or folder path to validate

**Returns**: Tuple `(is_valid: bool, message: str)`

##### `reload_automations() -> List[Dict]`
Reloads all automations from disk.

**Returns**: Updated list of automation dictionaries

---

### AutomationDetailsWidget

**Location**: `modules/automation_widgets.py`

**Purpose**: Main UI component for displaying and configuring automation details.

#### Signals
```python
executeRequested = Signal(dict)  # Emitted when user requests execution
```

#### Methods

##### `set_automation(automation: Dict)`
Configures the widget to display a specific automation.

**Parameters**:
- `automation` (Dict): Automation configuration dictionary

**Example**:
```python
widget = AutomationDetailsWidget()
widget.set_automation({
    "name": "CSV Processor",
    "description": "Process CSV files",
    "inputs": [...]
})
```

##### `validate_inputs() -> bool`
Validates all current input values.

**Returns**: True if all required inputs are valid, False otherwise

##### `get_input_values() -> Dict[str, str]`
Returns current input values.

**Returns**: Dictionary mapping input IDs to current values

##### `clear_inputs()`
Clears all input fields.

##### `set_output_text(text: str)`
Sets the output console text.

**Parameters**:
- `text` (str): Text to display in output console

---

### FileInputWidget

**Location**: `modules/automation_widgets.py`

**Purpose**: Custom widget for file and folder selection with validation.

#### Methods

##### `set_config(config: Dict)`
Sets the input configuration.

**Parameters**:
- `config` (Dict): Input configuration dictionary

##### `get_value() -> str`
Returns the current selected path.

**Returns**: Selected file or folder path

##### `set_value(path: str)`
Sets the input value.

**Parameters**:
- `path` (str): File or folder path to set

##### `validate() -> tuple`
Validates the current input value.

**Returns**: Tuple `(is_valid: bool, message: str)`

##### `clear()`
Clears the input field.

---

## 🎨 UI Components

### MainWindow

**Location**: `main.py`

**Purpose**: Main application window and entry point.

#### Key Methods

##### `setup_automation_widgets()`
Initializes automation-specific UI components.

##### `setup_automation_buttons()`
Configures sidebar buttons for available automations.

##### `show_automation_details(automation_id: str)`
Displays details for a specific automation.

**Parameters**:
- `automation_id` (str): ID of automation to display

##### `on_automation_execute_requested(inputs: Dict[str, str])`
Handles automation execution requests.

**Parameters**:
- `inputs` (Dict[str, str]): Input values for automation

##### `open_file_dialog(input_config: Dict) -> str`
Opens file selection dialog.

**Parameters**:
- `input_config` (Dict): Input configuration

**Returns**: Selected file path

---

## ⚙️ Configuration Schema

### Automation Configuration (`ui_config.json`)

#### Root Object
```json
{
    "name": "string",
    "description": "string",
    "inputs": [
        {
            "id": "string",
            "label": "string",
            "type": "file|folder",
            "required": boolean,
            "filters": "string (optional)"
        }
    ]
}
```

#### Field Descriptions

**name** (string, required)
- Display name for the automation
- Used in sidebar and detail views

**description** (string, required)
- Detailed description of what the automation does
- Displayed in the automation details panel

**inputs** (array, required)
- Array of input configuration objects
- Defines what inputs the automation requires

#### Input Configuration

**id** (string, required)
- Unique identifier for the input
- Used internally and passed to automation script

**label** (string, required)
- Human-readable label for the input
- Displayed in the UI

**type** (string, required)
- Input type: `"file"` or `"folder"`
- Determines the type of selector used

**required** (boolean, required)
- Whether the input is mandatory
- Required inputs must have values before execution

**filters** (string, optional)
- File type filters for file inputs
- Format: `"Description (*.ext);;Another (*.ext2)"`
- Example: `"CSV Files (*.csv);;All Files (*)"`

#### Example Configuration
```json
{
    "name": "Data Processor",
    "description": "Process data files and generate reports",
    "inputs": [
        {
            "id": "data_file",
            "label": "Data File",
            "type": "file",
            "required": true,
            "filters": "Data Files (*.csv *.xlsx);;All Files (*)"
        },
        {
            "id": "output_dir",
            "label": "Output Directory",
            "type": "folder",
            "required": true
        },
        {
            "id": "config_file",
            "label": "Configuration (Optional)",
            "type": "file",
            "required": false,
            "filters": "JSON Files (*.json);;All Files (*)"
        }
    ]
}
```

---

## 🔄 Event System

### Signal Connections

#### Automation Execution Flow
```python
# In AutomationDetailsWidget
executeRequested.connect(self.on_automation_execute_requested)

# In MainWindow
def on_automation_execute_requested(self, inputs):
    success, output = self.automation_manager.execute_automation(
        self.automation_manager.get_current_automation()["id"],
        inputs
    )
    # Update UI with results
```

#### File Selection Flow
```python
# FileInputWidget emits signal when file is selected
fileSelected = Signal(str)

# MainWindow connects to handle file selection
def open_file_dialog(self, input_config):
    # Open file dialog and return selected path
```

### Custom Signals

#### AutomationDetailsWidget
```python
executeRequested = Signal(dict)  # Emitted when Execute button is clicked
```

#### FileInputWidget
```python
fileSelected = Signal(str)        # Emitted when file is selected
folderSelected = Signal(str)      # Emitted when folder is selected
validationChanged = Signal(bool)  # Emitted when validation state changes
```

---

## 🛠 Utility Functions

### UI Functions (`modules/ui_functions.py`)

#### Theme Management
```python
def theme(self, file: str, useCustomTheme: bool = True)
```
Applies a QSS theme file to the application.

**Parameters**:
- `file` (str): Path to QSS theme file
- `useCustomTheme` (bool): Whether to use custom theme

#### Menu Management
```python
def toggleMenu(self, enable: bool)
```
Toggles the sidebar menu visibility.

**Parameters**:
- `enable` (bool): Whether to show the menu

#### UI Definitions
```python
def uiDefinitions(self)
```
Applies UI styling and behavior definitions.

### App Functions (`modules/app_functions.py`)

#### Theme Hacks
```python
def setThemeHack(self)
```
Applies theme-specific workarounds and hacks.

---

## 📝 Error Handling

### Common Error Types

#### Validation Errors
```python
# Input validation failed
return False, "Required field 'input_file' is missing"
```

#### Execution Errors
```python
# Script execution failed
return False, "Script returned exit code 1: File not found"
```

#### Timeout Errors
```python
# Execution timed out
return False, "Timeout: Script took longer than 5 minutes"
```

### Error Handling Patterns

#### In AutomationManager
```python
try:
    result = subprocess.run(args, capture_output=True, text=True, timeout=300)
    return result.returncode == 0, result.stdout + result.stderr
except subprocess.TimeoutExpired:
    return False, "Execution timed out"
except Exception as e:
    return False, f"Unexpected error: {str(e)}"
```

#### In UI Components
```python
try:
    # UI operation
    pass
except Exception as e:
    print(f"UI Error: {str(e)}")
    # Show user-friendly error message
```

---

## 🔧 Extension Points

### Adding New Input Types

1. **Extend FileInputWidget**:
```python
class CustomInputWidget(FileInputWidget):
    def __init__(self, config):
        super().__init__(config)
        # Add custom behavior
```

2. **Add Validation Logic**:
```python
def validate_custom_input(self, config, value):
    # Custom validation logic
    return True, "Valid"
```

3. **Update Configuration Schema**:
```json
{
    "id": "custom_input",
    "label": "Custom Input",
    "type": "custom",
    "required": true,
    "custom_property": "value"
}
```

### Adding New Automation Types

1. **Create Automation Script**:
```python
# run.py
import sys

def main():
    # Get arguments from UI
    arg1 = sys.argv[1] if len(sys.argv) > 1 else ""
    arg2 = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Your automation logic
    print("Processing...")
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
```

2. **Create Configuration**:
```json
{
    "name": "My Automation",
    "description": "Description of automation",
    "inputs": [
        {
            "id": "input1",
            "label": "Input 1",
            "type": "file",
            "required": true
        }
    ]
}
```

---

## 📊 Performance Considerations

### Memory Management
- Clear large output text periodically
- Dispose of file dialogs after use
- Limit automation output buffer size

### Execution Optimization
- Use subprocess with timeout to prevent hanging
- Implement progress reporting for long-running tasks
- Cache automation configurations

### UI Responsiveness
- Run automation execution in separate thread
- Update UI asynchronously
- Implement cancellation for long-running tasks

---

*This API reference covers the core functionality of AuroreUI. For additional examples and use cases, see the main documentation.*