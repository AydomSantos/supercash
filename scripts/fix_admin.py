import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.usuario import Usuario
from config.database import Database

def fix_admin_user():
    db = Database()
    conn = None
    try:
        conn = db.get_connection()
        
        # Get admin user
        admin = Usuario.get_by_username('admin')
        
        if admin:
            # Delete existing admin
            admin.delete()
            print('Existing admin user deleted')
        
        # Create new admin user
        new_admin = Usuario(
            username='admin',
            password='admin123',
            nome='Administrator',
            nivel_acesso='admin'
        )
        
        if new_admin.save():
            # Verify the new admin user
            test_admin = Usuario.authenticate('admin', 'admin123')
            if test_admin:
                print('Admin user successfully recreated and verified!')
                print(f'Password hash: {test_admin.password_hash}')
                return True
            else:
                print('Failed to verify new admin user!')
                return False
        else:
            print('Failed to create new admin user!')
            return False
            
    except Exception as e:
        print(f'Error fixing admin user: {e}')
        return False
    finally:
        if conn:
            db.return_connection(conn)

if __name__ == '__main__':
    success = fix_admin_user()
    sys.exit(0 if success else 1)