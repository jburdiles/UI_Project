# AuroreUI - Python Automation Runner

## 📋 Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [Usage Guide](#usage-guide)
5. [Development Guide](#development-guide)
6. [API Reference](#api-reference)
7. [Deployment](#deployment)
8. [Troubleshooting](#troubleshooting)

---

## 🎯 Overview

**AuroreUI** is a modern, cross-platform Python automation runner with a beautiful PySide6-based GUI. Built on the PyDracula theme, it provides an intuitive interface for executing Python automation scripts with dynamic input configuration and real-time output monitoring.

### Key Features
- **Dynamic Automation Detection**: Automatically discovers and loads Python automation scripts
- **Modern UI**: Clean, responsive interface with Dracula theme support
- **Input Validation**: Configurable input fields with file/folder selection
- **Real-time Execution**: Live output monitoring with error handling
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Extensible**: Easy to add new automations via JSON configuration

### Technology Stack
- **GUI Framework**: PySide6 (Qt6)
- **Python Version**: 3.9+
- **Theme**: PyDracula (Dark/Light variants)
- **Build Tool**: cx_Freeze (Windows compilation)

---

## 🏗 Architecture

### Project Structure
```
AuroreUI/
├── main.py                          # Application entry point
├── main.ui                          # Qt Designer UI file
├── setup.py                         # Build configuration
├── resources.qrc                    # Qt resources
├── icon.ico                         # Application icon
├── themes/                          # QSS theme files
├── modules/                         # Core application modules
│   ├── __init__.py
│   ├── ui_main.py                   # Generated UI code
│   ├── ui_functions.py              # UI interaction functions
│   ├── app_functions.py             # Application logic
│   ├── app_settings.py              # Global settings
│   ├── automation_manager.py        # Automation discovery & execution
│   ├── automation_widgets.py        # Custom automation UI widgets
│   └── resources_rc.py              # Compiled resources
├── widgets/                         # Custom widget components
│   └── custom_grips/                # Window resize grips
├── Automatizaciones/                # Automation scripts directory
│   ├── automatizacion1/
│   │   ├── ui_config.json          # Automation configuration
│   │   └── run.py                  # Automation script
│   ├── automatizacion2/
│   └── automatizacion3/
└── images/                          # Application images
```

### Core Components

#### 1. MainWindow (`main.py`)
- Application entry point and main window class
- Integrates PyDracula theme with automation functionality
- Manages UI state and automation execution

#### 2. AutomationManager (`modules/automation_manager.py`)
- **Purpose**: Discovers, loads, and executes automation scripts
- **Key Methods**:
  - `load_automations()`: Scans for automation configurations
  - `execute_automation()`: Runs automation with input validation
  - `validate_input_path()`: Validates file/folder inputs

#### 3. AutomationWidgets (`modules/automation_widgets.py`)
- **Purpose**: Custom UI components for automation interface
- **Components**:
  - `AutomationDetailsWidget`: Main automation display
  - `FileInputWidget`: File/folder selection with validation
  - `OutputConsole`: Real-time execution output display

#### 4. UI Functions (`modules/ui_functions.py`)
- **Purpose**: PyDracula theme integration and UI utilities
- **Features**: Menu animations, theme switching, window controls

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.9 or higher
- PySide6
- Operating System: Windows, macOS, or Linux

### Installation Steps

#### 1. Clone/Download Project
```bash
# If using git
git clone <repository-url>
cd AuroreUI

# Or download and extract the project files
```

#### 2. Install Dependencies
```bash
pip install PySide6
```

#### 3. Run the Application
```bash
# Windows
python main.py

# macOS/Linux
python3 main.py
```

### Build for Distribution (Windows)
```bash
python setup.py build
```

---

## 📖 Usage Guide

### Getting Started

#### 1. Launch the Application
```bash
python3 main.py
```

#### 2. Select an Automation
- Automations are automatically detected and displayed in the sidebar
- Click on any automation to view its details and configuration

#### 3. Configure Inputs
- Each automation has configurable inputs defined in `ui_config.json`
- Use file/folder selectors to choose input paths
- Required fields are marked with validation

#### 4. Execute Automation
- Click "Validate" to check all inputs are correct
- Click "Execute" to run the automation
- Monitor real-time output in the console area

### Automation Configuration

#### Creating a New Automation

1. **Create Directory Structure**:
```
Automatizaciones/my_automation/
├── ui_config.json
└── run.py
```

2. **Configure UI** (`ui_config.json`):
```json
{
    "name": "My Automation",
    "description": "Description of what this automation does",
    "inputs": [
        {
            "id": "input_file",
            "label": "Input File",
            "type": "file",
            "required": true,
            "filters": "Text Files (*.txt);;All Files (*)"
        },
        {
            "id": "output_folder",
            "label": "Output Folder",
            "type": "folder",
            "required": true
        }
    ]
}
```

3. **Create Script** (`run.py`):
```python
import sys
import os

def main():
    # Get command line arguments (inputs from UI)
    input_file = sys.argv[1] if len(sys.argv) > 1 else ""
    output_folder = sys.argv[2] if len(sys.argv) > 2 else ""
    
    # Your automation logic here
    print(f"Processing {input_file} to {output_folder}")
    
    # Example processing
    if input_file and os.path.exists(input_file):
        with open(input_file, 'r') as f:
            data = f.read()
        
        output_file = os.path.join(output_folder, "output.txt")
        with open(output_file, 'w') as f:
            f.write(data.upper())
        
        print("✅ Processing completed successfully!")
    else:
        print("❌ Error: Invalid input file")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Input Types

#### File Input
```json
{
    "id": "file_input",
    "label": "Select File",
    "type": "file",
    "required": true,
    "filters": "CSV Files (*.csv);;Excel Files (*.xlsx);;All Files (*)"
}
```

#### Folder Input
```json
{
    "id": "folder_input",
    "label": "Select Folder",
    "type": "folder",
    "required": true
}
```

### Validation Rules
- **Required fields**: Must have a value before execution
- **File validation**: Checks if file exists and matches expected type
- **Folder validation**: Ensures directory exists and is accessible
- **Path validation**: Verifies absolute/relative path correctness

---

## 🛠 Development Guide

### Adding New Features

#### 1. UI Modifications
- Edit `main.ui` in Qt Designer
- Regenerate `modules/ui_main.py`:
```bash
pyside6-uic main.ui -o modules/ui_main.py
```

#### 2. Adding New Input Types
1. Extend `AutomationWidgets` in `modules/automation_widgets.py`
2. Add validation logic in `AutomationManager`
3. Update UI configuration schema

#### 3. Theme Customization
- Modify QSS files in `themes/` directory
- Available themes:
  - `py_dracula_dark.qss`: Dark theme
  - `py_dracula_light.qss`: Light theme

### Code Style Guidelines
- **Python**: Follow PEP 8 standards
- **Qt**: Use PySide6 naming conventions
- **Comments**: Document complex logic and public methods
- **Error Handling**: Use try-catch blocks with meaningful messages

### Testing
```bash
# Run basic functionality test
python3 -c "from modules.automation_manager import AutomationManager; am = AutomationManager(); print(f'Found {len(am.get_automations())} automations')"
```

---

## 📚 API Reference

### AutomationManager Class

#### Methods

##### `__init__(automations_folder: str = "Automatizaciones")`
Initialize the automation manager.

**Parameters:**
- `automations_folder`: Path to automation scripts directory

##### `load_automations() -> List[Dict]`
Scan and load all available automations.

**Returns:**
- List of automation configuration dictionaries

##### `get_automations() -> List[Dict]`
Get all loaded automations.

**Returns:**
- List of automation dictionaries with keys: `id`, `name`, `description`, `inputs`, `folder`, `config_file`, `run_file`

##### `execute_automation(automation_id: str, inputs: Dict[str, str]) -> tuple`
Execute an automation with provided inputs.

**Parameters:**
- `automation_id`: Unique identifier for the automation
- `inputs`: Dictionary mapping input IDs to file/folder paths

**Returns:**
- Tuple `(success: bool, output: str)`

##### `validate_input_path(input_config: Dict, path: str) -> tuple`
Validate an input path against configuration.

**Parameters:**
- `input_config`: Input configuration dictionary
- `path`: File or folder path to validate

**Returns:**
- Tuple `(is_valid: bool, message: str)`

### AutomationDetailsWidget Class

#### Signals
- `executeRequested(inputs: Dict[str, str])`: Emitted when user requests execution

#### Methods

##### `set_automation(automation: Dict)`
Configure widget for a specific automation.

**Parameters:**
- `automation`: Automation configuration dictionary

##### `validate_inputs() -> bool`
Validate all current inputs.

**Returns:**
- True if all required inputs are valid

---

## 🚀 Deployment

### Windows Distribution

#### Using cx_Freeze
```bash
python setup.py build
```

#### Using PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

### Linux Distribution

#### Using PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile main.py
```

#### Creating .deb Package
```bash
# Install build dependencies
sudo apt-get install python3-stdeb

# Create package
python3 setup.py --command-packages=stdeb.command bdist_deb
```

### macOS Distribution

#### Using PyInstaller
```bash
pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

#### Creating .app Bundle
```bash
pyinstaller --onefile --windowed --name="AuroreUI" main.py
```

### Environment Variables
```bash
# Fix High DPI scaling issues
export QT_FONT_DPI=96

# Disable Qt platform plugin warnings
export QT_LOGGING_RULES="qt.qpa.*=false"
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. High DPI Display Issues
**Problem**: UI elements appear blurry or incorrectly sized
**Solution**: The application automatically sets `QT_FONT_DPI=96` to fix scaling issues

#### 2. Automation Not Detected
**Problem**: New automation doesn't appear in the sidebar
**Solution**: 
- Ensure `ui_config.json` and `run.py` exist in automation folder
- Check JSON syntax is valid
- Restart the application

#### 3. Execution Timeout
**Problem**: Automation fails with timeout error
**Solution**: 
- Check automation script for infinite loops
- Verify all required inputs are provided
- Increase timeout in `AutomationManager.execute_automation()`

#### 4. File Permission Errors
**Problem**: Cannot access files or folders
**Solution**:
- Check file/folder permissions
- Ensure paths are absolute or relative to automation directory
- Verify user has read/write access

#### 5. PySide6 Import Errors
**Problem**: Module not found errors
**Solution**:
```bash
pip install --upgrade PySide6
pip install --force-reinstall PySide6
```

### Debug Mode
Enable debug output by modifying `main.py`:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization
- **Large file lists**: Use virtual scrolling for file selectors
- **Memory usage**: Implement cleanup for large automation outputs
- **Startup time**: Cache automation configurations

---

## 📄 License

This project is based on PyDracula theme and is licensed under the same terms. See `LICENSE` file for details.

---

## 🤝 Contributing

### How to Contribute
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd AuroreUI

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
python -m pytest tests/
```

---

## 📞 Support

### Getting Help
- **Documentation**: Check this file and inline code comments
- **Issues**: Report bugs via GitHub issues
- **Discussions**: Use GitHub discussions for questions

### Reporting Bugs
When reporting bugs, please include:
- Operating system and version
- Python version
- PySide6 version
- Steps to reproduce
- Error messages and stack traces
- Screenshots if applicable

---

*Last updated: December 2024*