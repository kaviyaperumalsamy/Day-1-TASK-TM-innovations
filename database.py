# database.py
# ─────────────────────────────────────────────
# This file does ONE job: connect our app to the SQLite database.
# SQLAlchemy is the library that talks to the database for us.
# We create an "engine" (the connection) and a "SessionLocal"
# (a tool to open/close DB sessions inside each API request).
# ─────────────────────────────────────────────

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLite file will be created automatically as "library.db"
# in the same folder where you run the server
DATABASE_URL = "sqlite:///./library.db"

# connect_args is needed only for SQLite (thread safety fix)
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# SessionLocal is a factory — calling it gives you one DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the parent class all our models (tables) will inherit from
Base = declarative_base()


# ── Dependency ──────────────────────────────
# This function is used by FastAPI routes to get a DB session.
# It opens a session, gives it to the route, then closes it automatically.
def get_db():
    db = SessionLocal()
    try:
        yield db          # hand the session to the route
    finally:
        db.close()        # always close, even if an error happens
