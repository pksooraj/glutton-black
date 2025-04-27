# Manual MySQL Setup Guide

Since the automated setup script couldn't find the MySQL command, follow these manual steps to set up your MySQL database for the Black T-shirts project.

## Prerequisites

- MySQL Server installed on your system
- MySQL command-line tools or MySQL Workbench

## Step 1: Access MySQL

### Using MySQL Command Line

Open a command prompt or terminal and log in to MySQL as root:

```bash
mysql -u root -p
```

When prompted, enter your MySQL root password.

### Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your local MySQL instance

## Step 2: Create Database and User

Execute the following SQL commands:

```sql
-- Create the database
CREATE DATABASE IF NOT EXISTS blacktshirts_db;

-- Create the user with the password from your .env.mysql file
CREATE USER IF NOT EXISTS 'blacktshirts_user'@'localhost' IDENTIFIED BY 'Sooraj@Codered@';

-- Grant privileges
GRANT ALL PRIVILEGES ON blacktshirts_db.* TO 'blacktshirts_user'@'localhost';

-- Apply changes
FLUSH PRIVILEGES;
```

## Step 3: Verify Connection

Test that you can connect with the new user:

```bash
mysql -u blacktshirts_user -p blacktshirts_db
```

When prompted, enter the password: `Sooraj@Codered@`

## Step 4: Run Django Migrations

Now that your database is set up, run the Django migrations to create the necessary tables:

```bash
python manage.py migrate
```

## Step 5: Start the Development Server

Start your Django development server:

```bash
python manage.py runserver
```

## Troubleshooting

### MySQL Path Issues

If you get "mysql is not recognized as an internal or external command", you need to add MySQL to your system PATH:

1. Find your MySQL installation directory (typically `C:\Program Files\MySQL\MySQL Server 8.0\bin` on Windows)
2. Add this directory to your system PATH:
   - Right-click on 'This PC' or 'My Computer'
   - Select 'Properties'
   - Click on 'Advanced system settings'
   - Click on 'Environment Variables'
   - Under 'System variables', find and select 'Path'
   - Click 'Edit'
   - Click 'New' and add the MySQL bin directory path
   - Click 'OK' on all dialogs

### Connection Issues

If you have trouble connecting to MySQL, verify:

1. MySQL service is running
2. The credentials in your `.env.mysql` file match what you created
3. The host and port settings are correct

### Django Database Configuration

Your Django settings are already configured to use MySQL as shown in `blacktshirts/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('MYSQL_DATABASE', 'blacktshirts_db'),
        'USER': os.environ.get('MYSQL_USER', 'blacktshirts_user'),
        'PASSWORD': os.environ.get('MYSQL_PASSWORD', 'Sooraj@Codered@'),
        'HOST': os.environ.get('MYSQL_HOST', 'localhost'),
        'PORT': os.environ.get('MYSQL_PORT', '3306'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

## Next Steps

After completing the database setup:

1. Create a superuser to access the admin panel: `python manage.py createsuperuser`
2. Load any initial data if needed
3. Continue developing your Black T-shirts project