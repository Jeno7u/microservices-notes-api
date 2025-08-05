import os
from pathlib import Path
from dotenv import load_dotenv

# Load test environment
test_env = Path(__file__).parent / ".env.test"
if test_env.exists():
    load_dotenv(test_env)

# Test database configuration
TEST_DB_CONFIG = {
    "user": os.getenv("TEST_DB_USER", "postgres"),
    "password": os.getenv("TEST_DB_PASSWORD", "password"),
    "database": os.getenv("POSTGRES_TEST_DB", "testdb")
}

TEST_DB_URL = f"postgresql+asyncpg://{TEST_DB_CONFIG['user']}:{TEST_DB_CONFIG['password']}@localhost:5433/{TEST_DB_CONFIG['database']}"