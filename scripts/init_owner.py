import os
import sys

# Add project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from models.usuario import Usuario
from config.database import Database

def create_store_owner():
    db = Database()
    conn = None
    try:
        # Get a connection from the pool
        conn = db.get_connection()
        
        # Check if store owner already exists
        owner = Usuario.get_by_username('owner')
        
        if not owner:
            # Create store owner user
            owner = Usuario(
                username='owner',
                password='owner123',  # Initial password that should be changed on first login
                nome='Store Owner',
                nivel_acesso='owner'  # Special access level for store owner
            )
            if owner.save():
                print('Store owner user created successfully!')
                print('Username: owner')
                print('Initial password: owner123')
                print('Please change the password on first login.')
                return True
            else:
                print('Failed to create store owner user!')
                return False
        else:
            print('Store owner user already exists!')
            return True
    except Exception as e:
        print(f'Error creating store owner user: {e}')
        return False
    finally:
        if conn:
            db.return_connection(conn)

if __name__ == '__main__':
    success = create_store_owner()
    sys.exit(0 if success else 1)