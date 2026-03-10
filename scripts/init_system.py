#!/usr/bin/env python3
"""
Initialize Manus Agent System - Set up database and tables
"""
import os
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def init_database():
    """Initialize database and create tables"""
    try:
        logger.info("Initializing database...")
        
        from app.db.database import create_tables
        create_tables()
        
        logger.info("✅ Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f"❌ Database initialization error: {e}")
        return False


def create_sample_project():
    """Create a sample project"""
    try:
        logger.info("Creating sample project...")
        
        from app.db.database import SessionLocal
        from app.models.models import Project
        
        db = SessionLocal()
        
        # Check if sample project already exists
        existing = db.query(Project).filter(Project.name == "Sample Project").first()
        
        if not existing:
            project = Project(
                name="Sample Project",
                domain="example.com",
                description="Sample project for testing the Manus Agent System",
                is_active=True,
            )
            db.add(project)
            db.commit()
            logger.info(f"✅ Sample project created (ID: {project.id})")
        else:
            logger.info("ℹ️  Sample project already exists")
        
        db.close()
        return True
    except Exception as e:
        logger.error(f"❌ Sample project creation error: {e}")
        return False


def main():
    """Run initialization"""
    print("🚀 Manus Agent System Initialization")
    print("=" * 50)
    print()
    
    success = True
    
    # Initialize database
    if not init_database():
        success = False
    
    # Create sample project
    if not create_sample_project():
        success = False
    
    print()
    if success:
        print("✅ Initialization completed successfully!")
        print()
        print("📝 Configuration:")
        print("   - Check .env file for API keys")
        print("   - Ensure PostgreSQL is running")
        print("   - Ensure Redis is running")
        print()
        print("🚀 Start the API:")
        print("   uvicorn app.main:app --reload --port 8000")
        print()
        print("📚 View API docs:")
        print("   http://localhost:8000/docs")
        return 0
    else:
        print("❌ Initialization failed!")
        print("   Check error messages above and fix issues")
        return 1


if __name__ == "__main__":
    sys.exit(main())
