"""
Database Connection and Session Management
Supports both SQLite (local/development) and PostgreSQL (production/Render)
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Build engine kwargs based on database type
engine_kwargs = {}

if settings.DATABASE_URL.startswith("sqlite"):
    # SQLite: disable same-thread check (needed for FastAPI async)
    engine_kwargs["connect_args"] = {"check_same_thread": False}
elif settings.DATABASE_URL.startswith("postgresql") or settings.DATABASE_URL.startswith("postgres"):
    # PostgreSQL: configure connection pool for production
    engine_kwargs["pool_size"] = 5
    engine_kwargs["max_overflow"] = 10
    engine_kwargs["pool_pre_ping"] = True  # Verify connections before use
    engine_kwargs["pool_recycle"] = 300   # Recycle connections every 5 min

    # Render provides postgres:// URLs, SQLAlchemy needs postgresql://
    database_url = settings.DATABASE_URL
    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
else:
    database_url = settings.DATABASE_URL

# Use the corrected URL for PostgreSQL
database_url = settings.DATABASE_URL
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    database_url,
    **engine_kwargs,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """Create all database tables"""
    try:
        # Import all models so Base knows about them
        from app.models import models  # noqa: F401
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
