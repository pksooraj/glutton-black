import os
import sys
import subprocess
import django
from dotenv import load_dotenv

# Load environment variables from .env.mysql
load_dotenv('.env.mysql')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blacktshirts.settings')
django.setup()

def setup_mysql_database():
    """Set up MySQL database and migrate data"""
    print("Setting up MySQL database...")
    
    # Get database settings from environment variables
    db_name = os.environ.get('MYSQL_DATABASE', 'blacktshirts_db')
    db_user = os.environ.get('MYSQL_USER', 'blacktshirts_user')
    db_password = os.environ.get('MYSQL_PASSWORD', 'your_secure_password')
    db_host = os.environ.get('MYSQL_HOST', 'localhost')
    
    # Create database if it doesn't exist
    try:
        # Command to create database
        create_db_cmd = f"""mysql -u root -e "CREATE DATABASE IF NOT EXISTS {db_name}; 
                          CREATE USER IF NOT EXISTS '{db_user}'@'{db_host}' IDENTIFIED BY '{db_password}'; 
                          GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'{db_host}'; 
                          FLUSH PRIVILEGES;"""
        
        print("Creating MySQL database and user...")
        subprocess.run(create_db_cmd, shell=True, check=True)
        print("Database and user created successfully.")
        
        # Run migrations
        print("Running migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully.")
        
        print("\nMySQL setup completed successfully!")
        print(f"Database: {db_name}")
        print(f"User: {db_user}")
        print("\nYou can now run the server with: python manage.py runserver")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        print("\nManual setup instructions:")
        print(f"1. Create a MySQL database named '{db_name}'")
        print(f"2. Create a MySQL user '{db_user}' with password '{db_password}'")
        print(f"3. Grant all privileges on '{db_name}' to '{db_user}'")
        print("4. Run 'python manage.py migrate' to create the tables")

if __name__ == "__main__":
    setup_mysql_database()