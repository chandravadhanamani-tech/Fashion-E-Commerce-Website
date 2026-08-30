import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

Base = declarative_base()

# Attempt to create MySQL engine; if connection fails, use SQLite fallback engine
try:
    if settings.DATABASE_URL.startswith("sqlite"):
        engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})
    else:
        engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True, pool_recycle=3600)
        # Test connection
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print("[Database] Successfully connected to MySQL database!")
except Exception as e:
    print(f"[Database Warning] MySQL connection failed ({e}). Falling back to SQLite: {settings.FALLBACK_SQLITE_URL}")
    engine = create_engine(settings.FALLBACK_SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
