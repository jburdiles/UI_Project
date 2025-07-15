# AuroreUI - Python Automation Runner

> **Modern GUI for executing Python automations with dynamic input configuration and real-time output monitoring.**

> **Warning**: This project requires PySide6 and Python 3.9+, using previous versions can cause compatibility problems.

## 🚀 Quick Start

```bash
# Install dependencies
pip install PySide6

# Run the application
python3 main.py
```

**For detailed documentation, see:**
- 📖 [Full Documentation](DOCUMENTATION.md)
- ⚡ [Quick Start Guide](QUICK_START.md)

# YouTube - Presentation And Tutorial
Presentation and tutorial video with the main functions of the user interface.
> 🔗 https://youtu.be/9DnaHg4M_AM

## 🎯 Key Features

- **Dynamic Automation Detection**: Automatically discovers and loads Python automation scripts
- **Modern UI**: Clean, responsive interface with Dracula theme support
- **Input Validation**: Configurable input fields with file/folder selection
- **Real-time Execution**: Live output monitoring with error handling
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Extensible**: Easy to add new automations via JSON configuration

## 🎨 Multiple Themes
![PyDracula_Default_Dark](https://user-images.githubusercontent.com/60605512/112993874-0b647700-9140-11eb-8670-61322d70dbe3.png)
![PyDracula_Light](https://user-images.githubusercontent.com/60605512/112993918-18816600-9140-11eb-837c-e7a7c3d2b05e.png)

# High DPI
> Qt Widgets is an old technology and does not have a good support for high DPI settings, making these images look distorted when your system has DPI applied above 100%.
You can minimize this problem using a workaround by applying this code below in "main.py" just below the import of the Qt modules.
```python
# ADJUST QT FONT DPI FOR HIGHT SCALE
# ///////////////////////////////////////////////////////////////
from modules import *
from widgets import *
os.environ["QT_FONT_DPI"] = "96"
```

## 🚀 Running

### Prerequisites
- Python 3.9 or higher
- PySide6

### Installation & Execution
```bash
# Install dependencies
pip install PySide6

# Run on Windows
python main.py

# Run on macOS/Linux
python3 main.py
```

## 📦 Compiling

### Windows Distribution
```bash
python setup.py build
```

### Using PyInstaller (All Platforms)
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 📁 Project Structure

### Core Files
- **main.py**: Application entry point and main window
- **main.ui**: Qt Designer UI definition
- **setup.py**: Build configuration for distribution
- **resources.qrc**: Qt resources (icons, images)

### Key Directories
- **modules/**: Core application modules
  - `automation_manager.py`: Automation discovery and execution
  - `automation_widgets.py`: Custom UI components
  - `ui_functions.py`: UI interaction functions
  - `app_settings.py`: Global configuration
- **Automatizaciones/**: Automation scripts directory
  - Each subfolder contains `ui_config.json` and `run.py`
- **themes/**: QSS theme files (Dark/Light variants)
- **widgets/**: Custom widget components

### Automation Structure
Each automation requires:
```
Automatizaciones/my_automation/
├── ui_config.json    # UI configuration
└── run.py           # Automation script
```

## 📚 Documentation

- 📖 **[Full Documentation](DOCUMENTATION.md)**: Complete guide with API reference
- ⚡ **[Quick Start Guide](QUICK_START.md)**: Get running in 5 minutes
- 🎯 **[Usage Examples](AUTOMATIZACION_UI_ADAPTACION.md)**: Detailed usage scenarios

## 🤝 Contributing

We welcome contributions! Please see our contributing guidelines and feel free to submit issues or pull requests.

## 📄 License

This project is based on the PyDracula theme and is licensed under the same terms. See `LICENSE` file for details.

---

*Built with ❤️ using PySide6 and the PyDracula theme*