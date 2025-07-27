import pytest
from sqlalchemy import create_engine, inspect
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/okr_db")


@pytest.fixture(scope="module")
def db_engine():
    """Set up the database engine."""
    engine = create_engine(DATABASE_URL)
    yield engine
    engine.dispose()

def test_schema_tables_exist(db_engine):
    """Check that the required tables exist."""
    inspector = inspect(db_engine)
    tables = inspector.get_table_names()
    assert "objectives" in tables, "Table 'objectives' does not exist"
    assert "key_results" in tables, "Table 'key_results' does not exist"

def test_objectives_columns(db_engine):
    """Check that the 'objectives' table has the correct columns."""
    inspector = inspect(db_engine)
    columns = inspector.get_columns("objectives")
    column_names = [col["name"] for col in columns]
    assert "id" in column_names
    assert "name" in column_names
    assert "description" in column_names
    assert "progress" in column_names
    assert inspector.get_columns("objectives")[3]["type"].python_type == int

def test_key_results_columns(db_engine):
    """Check that the 'key_results' table has the correct columns."""
    inspector = inspect(db_engine)
    columns = inspector.get_columns("key_results")
    column_names = [col["name"] for col in columns]
    assert "id" in column_names
    assert "objective_id" in column_names
    assert "description" in column_names
    assert "progress" in column_names
    assert "metric" in column_names
    assert inspector.get_columns("key_results")[3]["type"].python_type == int
