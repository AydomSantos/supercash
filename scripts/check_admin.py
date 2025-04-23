import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.usuario import Usuario
from config.database import Database

def check_admin_auth():
    try:
        # Test authentication
        user = Usuario.authenticate('admin', 'admin123')
        if user:
            print('Admin authentication successful!')
            print(f'Username: {user.username}')
            print(f'Access Level: {user.nivel_acesso}')
            print(f'Password Hash: {user.password_hash}')
            return True
        else:
            print('Admin authentication failed!')
            return False
    except Exception as e:
        print(f'Error during authentication check: {e}')
        return False

if __name__ == '__main__':
    success = check_admin_auth()
    sys.exit(0 if success else 1)