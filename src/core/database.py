from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.core.joi import settings
from sqlalchemy import text
from tenacity import retry, stop_after_delay, wait_fixed

DATABASE_URL = settings.getOrThrow('SQLALCHEMY_DATABASE_URL')

engine = create_async_engine(DATABASE_URL, future=True, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

# Dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# Database connection check
@retry(stop=stop_after_delay(10), wait=wait_fixed(1))
async def check_db_connection():
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT version();"))
            version = result.scalar_one()
            print(f"Database connected. Version: {version}")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False