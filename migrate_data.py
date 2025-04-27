import os
import sys
import sqlite3
import mysql.connector
import django
from dotenv import load_dotenv

# Load environment variables from .env.mysql
load_dotenv('.env.mysql')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blacktshirts.settings')
django.setup()

def migrate_data_from_sqlite_to_mysql():
    """Migrate data from SQLite to MySQL"""
    print("Starting data migration from SQLite to MySQL...")
    
    # Get MySQL database settings from environment variables
    mysql_db_name = os.environ.get('MYSQL_DATABASE', 'blacktshirts_db')
    mysql_user = os.environ.get('MYSQL_USER', 'blacktshirts_user')
    mysql_password = os.environ.get('MYSQL_PASSWORD', 'your_secure_password')
    mysql_host = os.environ.get('MYSQL_HOST', 'localhost')
    mysql_port = os.environ.get('MYSQL_PORT', '3306')
    
    # Connect to SQLite database
    sqlite_conn = sqlite3.connect('db.sqlite3')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Get all tables from SQLite
    sqlite_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
    tables = sqlite_cursor.fetchall()
    
    try:
        # Connect to MySQL database
        mysql_conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db_name,
            port=int(mysql_port)
        )
        mysql_cursor = mysql_conn.cursor()
        
        # For each table in SQLite
        for table in tables:
            table_name = table[0]
            print(f"Migrating table: {table_name}")
            
            # Get all data from SQLite table
            sqlite_cursor.execute(f"SELECT * FROM {table_name};")
            rows = sqlite_cursor.fetchall()
            
            if not rows:
                print(f"  No data in table {table_name}, skipping...")
                continue
            
            # Get column names from SQLite table
            sqlite_cursor.execute(f"PRAGMA table_info({table_name});")
            columns = sqlite_cursor.fetchall()
            column_names = [column[1] for column in columns]
            
            # For each row in SQLite table
            for row in rows:
                # Create INSERT statement for MySQL
                placeholders = ", ".join(["%s"] * len(row))
                columns_str = ", ".join(column_names)
                insert_query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"
                
                try:
                    # Execute INSERT statement
                    mysql_cursor.execute(insert_query, row)
                except Exception as e:
                    print(f"  Error inserting into {table_name}: {e}")
            
            # Commit changes for this table
            mysql_conn.commit()
            print(f"  Migrated {len(rows)} rows from {table_name}")
        
        print("\nData migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {e}")
    finally:
        # Close connections
        sqlite_conn.close()
        if 'mysql_conn' in locals():
            mysql_conn.close()

if __name__ == "__main__":
    migrate_data_from_sqlite_to_mysql()