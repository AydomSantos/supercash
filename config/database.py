import sys
import os
from dotenv import load_dotenv
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import psycopg2
import logging

logger = logging.getLogger(__name__)

class Database:
    _pool = None
    def __init__(self):
        if getattr(sys, 'frozen', False):
            # Running in a bundle
            base_dir = os.path.dirname(sys.executable)
            if sys.platform.startswith('darwin'):
                # On macOS, the .env should be in Resources
                base_dir = os.path.join(base_dir, 'Resources')
        else:
            # Running in development
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Load environment variables from the correct location
        env_path = os.path.join(base_dir, '.env')
        load_dotenv(env_path)
        
        self.host = os.getenv('DB_HOST', 'localhost')
        self.port = os.getenv('DB_PORT', '5432')
        self.user = os.getenv('DB_USER', 'postgres')
        self.password = os.getenv('DB_PASSWORD', '')
        self.dbname = os.getenv('DB_NAME', 'petshop_db')
        
        logger.info(f'Database configuration loaded: host={self.host}, port={self.port}, user={self.user}, dbname={self.dbname}')
        
        if self._pool is None:
            self._pool = SimpleConnectionPool(
                minconn=1,
                maxconn=20,
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname
            )
            logger.info('Database connection pool initialized successfully')
    def close_all(self):
        if self._pool:
            try:
                self._pool.closeall()
                logger.info('All database connections closed successfully')
                self._pool = None
            except Exception as e:
                logger.error(f'Error closing database connections: {e}', exc_info=True)
                raise

    def __del__(self):
        self.close_all()

    def get_connection(self):
        if not self._pool:
            logger.error('Database connection pool not initialized')
            raise Exception('Database connection pool not initialized')
        try:
            conn = self._pool.getconn()
            if conn:
                conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
                return conn
            logger.error('Could not get connection from pool')
            raise Exception('Could not get connection from pool')
        except psycopg2.Error as e:
            logger.error(f'Error getting connection from pool: {e}', exc_info=True)
            raise

    def return_connection(self, conn):
        if conn and self._pool:
            try:
                if not conn.closed:
                    self._pool.putconn(conn)
                    logger.debug('Connection returned to pool successfully')
            except Exception as e:
                logger.error(f'Error returning connection to pool: {e}', exc_info=True)
                try:
                    conn.close()
                except:
                    pass

    def initialize(self):
        try:
            logger.info('Initializing database...')
            temp_conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname='postgres'
            )
            temp_conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            logger.info('Connected to postgres database for initialization')

            cur = temp_conn.cursor()
            
            # Check if database exists
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (self.dbname,))
            exists = cur.fetchone()
            
            if not exists:
                logger.info(f'Creating database {self.dbname}')
                cur.execute(f'CREATE DATABASE {self.dbname}')
                logger.info(f'Database {self.dbname} created successfully')
            else:
                logger.info(f'Database {self.dbname} already exists')

            cur.close()
            temp_conn.close()
            logger.info('Database initialization completed successfully')
            
        except Exception as e:
            logger.error(f'Failed to initialize database: {e}', exc_info=True)
            raise