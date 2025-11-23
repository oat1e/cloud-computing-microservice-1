"""
Database configuration and connection setup for CloudSQL.
Supports both Cloud Run (Unix socket) and local development.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

Base = declarative_base()


def get_database_url() -> str:
    """
    Construct database URL for CloudSQL or local MySQL.
    
    Environment variables:
    - DB_HOST: Database host (default: localhost)
    - DB_PORT: Database port (default: 3306)
    - DB_USER: Database user (default: root)
    - DB_PASSWORD: Database password (required)
    - DB_NAME: Database name (default: matcha_db)
    - CLOUD_SQL_CONNECTION_NAME: CloudSQL connection name (e.g., project:region:instance)
    - DB_SOCKET_DIR: Unix socket directory (default: /cloudsql)
    
    For Cloud Run with CloudSQL, use Unix socket connection.
    For local development, use TCP connection.
    """
    # CloudSQL connection via Unix socket (Cloud Run)
    cloud_sql_connection_name = os.environ.get("CLOUD_SQL_CONNECTION_NAME")
    db_socket_dir = os.environ.get("DB_SOCKET_DIR", "/cloudsql")
    
    if cloud_sql_connection_name:
        # Use Unix socket for Cloud Run
        db_user = os.environ.get("DB_USER", "root")
        db_password = os.environ.get("DB_PASSWORD", "")
        db_name = os.environ.get("DB_NAME", "matcha_db")
        
        unix_socket_path = f"{db_socket_dir}/{cloud_sql_connection_name}"
        return (
            f"mysql+pymysql://{db_user}:{db_password}@/{db_name}"
            f"?unix_socket={unix_socket_path}"
        )
    else:
        # Use TCP connection for local development
        db_host = os.environ.get("DB_HOST", "localhost")
        db_port = os.environ.get("DB_PORT", "3306")
        db_user = os.environ.get("DB_USER", "root")
        db_password = os.environ.get("DB_PASSWORD", "")
        db_name = os.environ.get("DB_NAME", "matcha_db")
        
        if not db_password:
            raise ValueError("DB_PASSWORD environment variable is required")
        
        return (
            f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        )


# Create engine with appropriate pool settings
database_url = get_database_url()
engine = create_engine(
    database_url,
    poolclass=NullPool,  # Cloud Run doesn't need connection pooling
    pool_pre_ping=True,  # Verify connections before using
    echo=False,  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """Dependency for FastAPI to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables."""
    Base.metadata.create_all(bind=engine)

