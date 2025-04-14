"""Script to check database schema for tags."""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect, MetaData, Table

# Load environment variables
load_dotenv()

# Get database URL from environment variable
DB_URL = os.environ.get("DB_URL")
if DB_URL is None:
    raise ValueError("DB_URL environment variable is not set")

# Create engine
engine = create_engine(DB_URL)
inspector = inspect(engine)

# Get list of all tables
print("Available tables in the database:")
tables = inspector.get_table_names()
for table in tables:
    print(f"- {table}")

# Look for tag-related tables
tag_tables = [table for table in tables if "tag" in table.lower()]
print("\nTag-related tables found:")
for table in tag_tables:
    print(f"- {table}")
    # Get table columns
    columns = inspector.get_columns(table)
    print("  Columns:")
    for column in columns:
        print(f"    - {column['name']} ({column['type']})")

    # Get primary keys
    pk = inspector.get_pk_constraint(table)
    print(f"  Primary key: {pk['constrained_columns']}")

    # Get foreign keys
    fks = inspector.get_foreign_keys(table)
    if fks:
        print("  Foreign keys:")
        for fk in fks:
            print(
                f"    - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}"
            )

    print()

# Check announcements table for tag relation
if "announcements" in tables:
    print("Checking 'announcements' table:")
    columns = inspector.get_columns("announcements")
    for column in columns:
        if "tag" in column["name"].lower():
            print(f"  Found tag-related column: {column['name']} ({column['type']})")

    fks = inspector.get_foreign_keys("announcements")
    for fk in fks:
        if any("tag" in col.lower() for col in fk["constrained_columns"]):
            print(
                f"  Found tag-related foreign key: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}"
            )
