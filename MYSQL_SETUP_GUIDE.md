# MySQL Setup Guide for Black T-shirts Project

## Overview

This guide will help you set up MySQL as your database for the Black T-shirts project. The project has been configured to use MySQL instead of SQLite for better performance and scalability.

## Prerequisites

- MySQL Server installed on your system
- Python 3.8 or higher
- Virtual environment with project dependencies installed

## Installation Steps

### 1. Install Required Packages

The project already includes `mysqlclient` in the requirements.txt file. Make sure all dependencies are installed:

```bash
pip install -r requirements.txt
```

### 2. Configure MySQL Database

The project includes a `.env.mysql` file with the following configuration:

```
# MySQL Database Configuration
MYSQL_DATABASE=blacktshirts_db
MYSQL_USER=blacktshirts_user
MYSQL_PASSWORD=your_secure_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
```

Update these values as needed for your environment, especially the password.

### 3. Create MySQL Database and User

You can use the provided `setup_mysql.py` script to create the database and user:

```bash
python setup_mysql.py
```

This script will:
- Create the MySQL database if it doesn't exist
- Create the MySQL user if it doesn't exist
- Grant necessary privileges to the user
- Run migrations to set up the database schema

### 4. Migrate Data (If you have existing data in SQLite)

If you have existing data in SQLite that you want to transfer to MySQL, use the provided `migrate_data.py` script:

```bash
python migrate_data.py
```

This script will transfer all your data from the SQLite database to the MySQL database.

## Verification

To verify that your application is correctly using MySQL:

1. Start your Django development server:
   ```bash
   python manage.py runserver
   ```

2. Access the admin interface or your application and check that all data is available.

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Make sure MySQL server is running
   - Verify the host and port settings in `.env.mysql`

2. **Access Denied**
   - Check that the username and password in `.env.mysql` are correct
   - Ensure the user has proper permissions on the database

3. **Missing Tables**
   - Run migrations again: `python manage.py migrate`

### MySQL Command Line

You can connect to your MySQL database directly using:

```bash
mysql -u blacktshirts_user -p blacktshirts_db
```

When prompted, enter the password you set in the `.env.mysql` file.

## Benefits of Using MySQL

- Better performance for larger datasets
- Improved concurrency handling
- More robust data integrity
- Better scalability for growing applications
- Advanced query capabilities

## Next Steps

Now that you have MySQL configured, you can continue developing your application with a more robust database backend. The settings in `blacktshirts/settings.py` have been updated to use MySQL by default.