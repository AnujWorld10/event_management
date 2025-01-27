from sqlalchemy import create_engine, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:mysql@localhost:3306/event_management"

try:
    engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20)
except exc.SQLAlchemyError as e:
    raise HTTPException(
        status_code=500, detail=f"Error connecting to the database: {e}"
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while interacting with the database session: {e}",
        )
    finally:
        db.close()
