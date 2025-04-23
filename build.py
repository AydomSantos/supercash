import os
import sys
import shutil
from pathlib import Path

def cleanup():
    # Clean previous builds
    build_dir = Path('build')
    dist_dir = Path('dist')
    for dir_path in [build_dir, dist_dir]:
        if dir_path.exists():
            shutil.rmtree(dir_path)

def get_platform_specs():
    if sys.platform.startswith('win'):
        return {
            'icon': 'assets/icon.ico',
            'add_data': ['ui/*.ui', 'assets/*', '.env'],
            'name': 'Supercash.exe'
        }
    elif sys.platform.startswith('darwin'):
        return {
            'icon': 'assets/icon.icns',
            'add_data': ['ui/*.ui', 'assets/*', '.env'],
            'name': 'Supercash',
            'entitlements': 'entitlements.plist',
            'bundle_id': 'com.supercash.app'
        }
    else:  # Linux
        return {
            'icon': 'assets/icon.png',
            'add_data': ['ui/*.ui', 'assets/*', '.env'],
            'name': 'Supercash'
        }

def build():
    try:
        # Install required dependencies
        print('Installing dependencies...')
        os.system('pip install -r requirements.txt')
        
        # Ensure PyInstaller is installed
        os.system('pip install pyinstaller')
        
        # Clean previous builds
        cleanup()
        
        # Get platform-specific settings
        specs = get_platform_specs()
        
        # Build command for PyInstaller
        cmd = []
        cmd.extend([
            'pyinstaller',
            '--clean',
            '--windowed',
            f'--icon={specs["icon"]}',
            '--name', specs['name']
        ])
        
        # Add data files with proper separator
        separator = ';' if sys.platform.startswith('win') else ':'
        for data in specs['add_data']:
            cmd.extend(['--add-data', f'{data}{separator}.'])
            
        cmd.extend([
            '--hidden-import=PySide6.QtXml',
            '--collect-data=qt_material',
            '--collect-data=reportlab',
            '--collect-all=psycopg2-binary'
        ])
        
        # Add macOS specific options
        if sys.platform.startswith('darwin'):
            cmd.extend([
                '--osx-bundle-identifier', specs['bundle_id'],
                '--target-arch', 'x86_64',
                '--codesign-identity', '-'
            ])
        
        cmd.append('main.py')
        
        # Execute PyInstaller
        print('Building application...')
        os.system(' '.join(cmd))
        
        # Additional macOS post-processing
        if sys.platform.startswith('darwin'):
            app_path = Path('dist') / f'{specs["name"]}.app'
            if app_path.exists():
                # Set proper permissions
                os.system(f'chmod -R 755 "{app_path}"')
                # Remove quarantine attribute
                os.system(f'xattr -rd com.apple.quarantine "{app_path}"')
                print('macOS post-processing completed')
        
        print('Build completed successfully!')
        return True
    except Exception as e:
        print(f'Build failed: {e}')
        return False

if __name__ == '__main__':
    build()