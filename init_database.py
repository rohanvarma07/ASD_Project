#!/usr/bin/env python3
"""
Database Initialization Script
Clears and recreates the database with proper schema
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import Database

def clear_and_init_database():
    """Clear existing database and initialize fresh"""
    
    print("\n" + "="*60)
    print("DATABASE INITIALIZATION")
    print("="*60)
    
    # Remove old database file
    db_file = 'asd_database.db'
    if os.path.exists(db_file):
        os.remove(db_file)
        print(f"\n✅ Removed old database: {db_file}")
    
    # Remove WAL files
    for ext in ['-shm', '-wal']:
        wal_file = db_file + ext
        if os.path.exists(wal_file):
            os.remove(wal_file)
            print(f"✅ Removed WAL file: {wal_file}")
    
    # Initialize new database
    print("\n🔨 Creating new database...")
    db = Database(db_file)
    
    # Create sample admin user
    print("\n👤 Creating sample admin user...")
    success, message = db.register_user(
        email='admin@example.com',
        mobile='1234567890',
        password='Admin@123',
        username='Admin User'
    )
    
    if success:
        print(f"✅ {message}")
        print("\n📝 Sample Login Credentials:")
        print("   Email: admin@example.com")
        print("   Password: Admin@123")
    else:
        print(f"⚠️ {message}")
    
    # Verify database
    print("\n🔍 Verifying database structure...")
    conn = db.get_connection()
    cursor = conn.cursor()
    
    # Check tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    
    print(f"\n✅ Tables created: {len(tables)}")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   • {table}: {count} records")
    
    # Check WAL mode
    cursor.execute("PRAGMA journal_mode")
    journal_mode = cursor.fetchone()[0]
    print(f"\n✅ Journal mode: {journal_mode}")
    
    conn.close()
    
    print("\n" + "="*60)
    print("✅ DATABASE READY FOR DEPLOYMENT!")
    print("="*60)
    print("\nDatabase file: asd_database.db")
    print(f"Size: {os.path.getsize(db_file) / 1024:.1f} KB")
    print("\n🚀 You can now deploy to Render")
    print("\n")

if __name__ == "__main__":
    try:
        clear_and_init_database()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
