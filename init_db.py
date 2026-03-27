#!/usr/bin/env python3
"""
Database Initialization Script for Hospital Queue System
Creates the SQLite database and tables if they do not exist.
"""

import os
import sqlite3
from contextlib import contextmanager

# Database file path
DB_FILE = os.path.join(os.path.dirname(__file__), "backend", "hospital_queue.db")
SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "backend", "init_db.sql")

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    conn = None
    try:
        conn = sqlite3.connect(DB_FILE)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

def initialize_database():
    """Initialize the database with schema if it doesn't exist"""
    print("=" * 60)
    print("🏥 HOSPITAL QUEUE SYSTEM - DATABASE INITIALIZATION")
    print("=" * 60)

    # Check if database already exists
    if os.path.exists(DB_FILE):
        print(f"✅ Database already exists: {DB_FILE}")
        return True

    # Check if schema file exists
    if not os.path.exists(SCHEMA_FILE):
        print(f"❌ ERROR: Schema file not found: {SCHEMA_FILE}")
        return False

    try:
        print(f"📊 Creating database: {DB_FILE}")
        with get_db_connection() as conn:
            cursor = conn.cursor()
            with open(SCHEMA_FILE, 'r') as f:
                schema_sql = f.read()
            cursor.executescript(schema_sql)
            conn.commit()
        print("✅ Database schema created successfully")
        print(f"✅ Database initialized: {DB_FILE}")
        return True
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

if __name__ == "__main__":
    success = initialize_database()
    if success:
        print("=" * 60)
        print("🎉 DATABASE INITIALIZATION COMPLETE")
        print("=" * 60)
    else:
        print("=" * 60)
        print("💥 DATABASE INITIALIZATION FAILED")
        print("=" * 60)
        exit(1)
