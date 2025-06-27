import sys
import os
import sqlite3
import logging
from threading import Lock

logger = logging.getLogger(__name__)

class Database:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            if getattr(sys, 'frozen', False):
                # Running in a bundle
                base_dir = os.path.dirname(sys.executable)
                if sys.platform.startswith('darwin'):
                    # On macOS, the database should be in Resources
                    base_dir = os.path.join(base_dir, 'Resources')
            else:
                # Running in development
                base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            self.db_path = os.path.join(base_dir, 'supercash.db')
            logger.info(f'Database path: {self.db_path}')
            self.initialized = True

    def get_connection(self):
        try:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row  # Enable column access by name
            # Enable foreign keys
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            logger.error(f'Error connecting to database: {e}', exc_info=True)
            raise

    def return_connection(self, conn):
        if conn:
            try:
                conn.close()
                logger.debug('Connection closed successfully')
            except Exception as e:
                logger.error(f'Error closing connection: {e}', exc_info=True)

    def close_all(self):
        # SQLite doesn't need connection pooling cleanup
        logger.info('Database connections cleanup completed')

    def __del__(self):
        self.close_all()

    def initialize(self):
        try:
            logger.info('Initializing SQLite database...')
            conn = self.get_connection()

            # Create tables
            with open(os.path.join(os.path.dirname(__file__), '..', 'scripts', 'create_tables.sql'), 'r') as f:
                sql_script = f.read()

            # Execute each statement separately
            for statement in sql_script.split(';'):
                statement = statement.strip()
                if statement:
                    conn.execute(statement)

            conn.commit()
            self.return_connection(conn)
            logger.info('Database initialization completed successfully')

        except Exception as e:
            logger.error(f'Failed to initialize database: {e}', exc_info=True)
            raise