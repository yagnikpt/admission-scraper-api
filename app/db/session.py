from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DB_URL = os.environ.get("DB_URL")

# Connection parameters to improve reliability in production
connect_args = {
    "connect_timeout": 30,  # Increase connection timeout
    "sslmode": "require",  # Require SSL connection
    "options": "-c statement_timeout=60000 -c timezone=UTC",  # Set statement timeout and timezone
}

# Create SQLAlchemy engine with connection pooling optimization
url = make_url(DB_URL)
if url.host:
    # Force hostname resolution to IPv4 by setting appropriate options
    connect_args["host"] = url.host
    # PostgreSQL doesn't have a direct IPv4/IPv6 flag, so we rely on hostaddr for IPv4
    # Try to resolve host to IPv4 address when possible

engine = create_engine(
    DB_URL,
    connect_args=connect_args,
    pool_size=5,  # Set a reasonable pool size
    max_overflow=10,  # Allow temporary additional connections
    pool_timeout=30,  # Pool timeout
    pool_recycle=1800,  # Recycle connections after 30 minutes
    pool_pre_ping=True,  # Verify connections before using them
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
