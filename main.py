import sys
import os
import logging
from pathlib import Path
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import QFile
from controllers.login_controller import LoginController
from config.database import Database

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('supercash.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def setup_environment():
    try:
        # Add project root to Python path
        project_root = Path(__file__).parent
        sys.path.append(str(project_root))
        
        # Set proper file permissions on macOS
        if sys.platform.startswith('darwin'):
            os.chmod(project_root, 0o755)
            for root, dirs, files in os.walk(project_root):
                for d in dirs:
                    os.chmod(os.path.join(root, d), 0o755)
                for f in files:
                    os.chmod(os.path.join(root, f), 0o644)
        
        logger.info(f'Added {project_root} to Python path')
        logger.info('Environment setup completed')
    except Exception as e:
        logger.error(f'Failed to setup environment: {e}')
        raise

def main():
    try:
        logger.info('Starting Supercash application')
        setup_environment()
        
        # Initialize database
        logger.info('Initializing database connection')
        db = Database()
        db.initialize()
        
        # Create Qt application
        logger.info('Creating Qt application instance')
        app = QApplication(sys.argv)
        
        # Set application style
        app.setStyle('Fusion')
        
        # Initialize and show login window
        logger.info('Initializing login controller')
        login_controller = LoginController()
        login_controller.show_login()
        
        # Start application event loop
        return app.exec()
    except Exception as e:
        logger.error(f'Application error: {e}')
        if 'app' in locals():
            QMessageBox.critical(None, 'Error', f'Application error: {str(e)}')
        return 1

if __name__ == '__main__':
    sys.exit(main())