# AuroreUI - Quick Start Guide

## 🚀 Get Running in 5 Minutes

### 1. Install Dependencies
```bash
pip install PySide6
```

### 2. Run the Application
```bash
python3 main.py
```

### 3. Use the Interface
- **Sidebar**: Click on any automation to select it
- **Inputs**: Use file/folder selectors to configure your automation
- **Execute**: Click "Validate" then "Execute" to run

---

## 📁 Adding Your First Automation

### Step 1: Create Folder Structure
```bash
mkdir -p Automatizaciones/my_first_automation
cd Automatizaciones/my_first_automation
```

### Step 2: Create Configuration
Create `ui_config.json`:
```json
{
    "name": "My First Automation",
    "description": "A simple automation example",
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

### Step 3: Create Script
Create `run.py`:
```python
import sys
import os

def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else ""
    output_folder = sys.argv[2] if len(sys.argv) > 2 else ""
    
    print(f"Processing: {input_file}")
    print(f"Output to: {output_folder}")
    
    if input_file and os.path.exists(input_file):
        with open(input_file, 'r') as f:
            content = f.read()
        
        output_file = os.path.join(output_folder, "processed.txt")
        with open(output_file, 'w') as f:
            f.write(content.upper())
        
        print("✅ Success! Check the output folder.")
    else:
        print("❌ Error: Invalid input file")
        sys.exit(1)

if __name__ == "__main__":
    main()
```

### Step 4: Restart Application
Restart AuroreUI to detect your new automation.

---

## 🎯 Common Use Cases

### File Processing
```json
{
    "inputs": [
        {
            "id": "source_file",
            "label": "Source File",
            "type": "file",
            "required": true,
            "filters": "CSV Files (*.csv);;Excel Files (*.xlsx)"
        }
    ]
}
```

### Batch Operations
```json
{
    "inputs": [
        {
            "id": "input_folder",
            "label": "Input Folder",
            "type": "folder",
            "required": true
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

### Optional Configuration
```json
{
    "inputs": [
        {
            "id": "config_file",
            "label": "Configuration (Optional)",
            "type": "file",
            "required": false,
            "filters": "JSON Files (*.json)"
        }
    ]
}
```

---

## 🔧 Troubleshooting Quick Fixes

### Problem: Application won't start
```bash
pip install --upgrade PySide6
```

### Problem: Automation not detected
- Check that both `ui_config.json` and `run.py` exist
- Verify JSON syntax is valid
- Restart the application

### Problem: File permission errors
- Ensure you have read/write access to selected files/folders
- Try running as administrator (Windows) or with sudo (Linux)

### Problem: High DPI display issues
The application automatically fixes this, but if problems persist:
```bash
export QT_FONT_DPI=96
python3 main.py
```

---

## 📚 Next Steps

- Read the full [Documentation](DOCUMENTATION.md) for advanced features
- Check out the example automations in `Automatizaciones/`
- Explore the [API Reference](DOCUMENTATION.md#api-reference) for development
- Join the community for support and updates

---

*Need help? Check the full documentation or report issues on GitHub.*