import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.usuario import Usuario
from config.database import Database

def create_admin_user():
    db = Database()
    conn = None
    try:
        # Get a connection from the pool
        conn = db.get_connection()
        
        # Check if admin user already exists
        admin = Usuario.get_by_username('admin')
        
        if not admin:
            # Create admin user
            admin = Usuario(
                username='admin',
                password='admin123',  # Initial password that should be changed on first login
                nome='Administrator',
                nivel_acesso='admin'  # Changed to string to match database schema
            )
            if admin.save():
                print('Admin user created successfully!')
                return True
            else:
                print('Failed to create admin user!')
                return False
        else:
            print('Admin user already exists!')
            return True
    except Exception as e:
        print(f'Error creating admin user: {e}')
        return False
    finally:
        if conn:
            db.return_connection(conn)

if __name__ == '__main__':
    success = create_admin_user()
    sys.exit(0 if success else 1)