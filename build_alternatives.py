
"""
Alternative build methods for creating executables
"""
import os
import sys
import shutil
from pathlib import Path

def build_with_cx_freeze():
    """Build using cx_Freeze"""
    try:
        print("Building with cx_Freeze...")
        
        # Create setup_cx.py
        setup_content = '''
from cx_Freeze import setup, Executable
import sys

# Dependencies
build_exe_options = {
    "packages": ["PySide6", "psycopg2", "dotenv", "qt_material", "pandas", "reportlab"],
    "excludes": ["tkinter"],
    "include_files": [
        ("ui/", "ui/"),
        ("assets/", "assets/"),
        ("config/", "config/"),
        ("models/", "models/"),
        ("controllers/", "controllers/"),
        (".env", ".env")
    ]
}

# Base for GUI applications
base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [
    Executable(
        "main.py",
        base=base,
        target_name="Supercash",
        icon="assets/icon.icns" if sys.platform == "darwin" else "assets/icon.ico"
    )
]

setup(
    name="Supercash",
    version="1.0.0",
    description="Pet Shop Management System",
    options={"build_exe": build_exe_options},
    executables=executables
)
'''
        
        with open('setup_cx.py', 'w') as f:
            f.write(setup_content)
        
        os.system('python setup_cx.py build')
        print("cx_Freeze build completed!")
        
    except Exception as e:
        print(f"cx_Freeze build failed: {e}")

def build_with_nuitka():
    """Build using Nuitka"""
    try:
        print("Building with Nuitka...")
        
        cmd = [
            'python', '-m', 'nuitka',
            '--standalone',
            '--enable-plugin=pyside6',
            '--include-data-dir=ui=ui',
            '--include-data-dir=assets=assets',
            '--include-data-file=.env=.env',
            '--disable-console',
            '--output-filename=Supercash'
        ]
        
        if sys.platform == "darwin":
            cmd.append('--macos-create-app-bundle')
            cmd.append('--macos-app-icon=assets/icon.icns')
        elif sys.platform.startswith('win'):
            cmd.append('--windows-icon-from-ico=assets/icon.ico')
        
        cmd.append('main.py')
        
        os.system(' '.join(cmd))
        print("Nuitka build completed!")
        
    except Exception as e:
        print(f"Nuitka build failed: {e}")

def build_with_briefcase():
    """Build using Briefcase"""
    try:
        print("Building with Briefcase...")
        
        # Create pyproject.toml for Briefcase
        pyproject_content = '''
[build-system]
requires = ["briefcase"]

[tool.briefcase]
project_name = "Supercash"
bundle = "com.supercash"
version = "1.0.0"
url = "https://github.com/your-username/supercash"
license = "MIT"
author = "Your Name"
author_email = "your.email@example.com"

description = "Pet Shop Management System"
long_description = """A complete management system for pet shops."""

[tool.briefcase.app.supercash]
formal_name = "Supercash"
description = "Pet Shop Management System"
icon = "assets/icon"
sources = ["config", "controllers", "models", "ui", "scripts"]
requires = [
    "PySide6>=6.5.0",
    "psycopg2-binary>=2.9.7",
    "python-dotenv>=1.0.0",
    "qt-material>=2.14",
    "pandas>=2.0.0",
    "openpyxl>=3.1.2",
    "reportlab>=4.0.4",
    "qrcode>=7.4.2",
    "pillow>=9.5.0",
    "passlib>=1.7.4",
    "psutil>=5.9.5",
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.2"
]

[tool.briefcase.app.supercash.macOS]
requires = []

[tool.briefcase.app.supercash.linux]
requires = []

[tool.briefcase.app.supercash.windows]
requires = []
'''
        
        with open('pyproject_briefcase.toml', 'w') as f:
            f.write(pyproject_content)
        
        os.system('briefcase create')
        os.system('briefcase build')
        os.system('briefcase package')
        print("Briefcase build completed!")
        
    except Exception as e:
        print(f"Briefcase build failed: {e}")

def main():
    """Main build function with options"""
    print("Choose build method:")
    print("1. PyInstaller (default)")
    print("2. cx_Freeze")
    print("3. Nuitka")
    print("4. Briefcase")
    print("5. All methods")
    
    choice = input("Enter choice (1-5): ").strip()
    
    if choice == "2":
        build_with_cx_freeze()
    elif choice == "3":
        build_with_nuitka()
    elif choice == "4":
        build_with_briefcase()
    elif choice == "5":
        from build import build
        build()  # PyInstaller
        build_with_cx_freeze()
        build_with_nuitka()
        build_with_briefcase()
    else:
        from build import build
        build()  # Default PyInstaller

if __name__ == '__main__':
    main()
