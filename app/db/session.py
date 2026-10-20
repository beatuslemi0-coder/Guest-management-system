# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# Kutengeneza SQLAlchemy engine kwa ajili ya PostgreSQL
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency ya kupata Database Session kwenye Endpoints zetu
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()