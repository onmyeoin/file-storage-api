from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg://eoinoreilly:inscribe24@db:5432/pg-db-inscribe-test"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to provide a session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()