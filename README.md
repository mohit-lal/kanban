# Requirements
1. Python 3.8.2

# Steps to install this app
1. create a virtual environment. `virtualenv -p /usr/bin/python3.8`
2. change directory to root of the project.
3. Install dependency using `pip install -r requirements.txt`

# Configure Database
1. Create Database
2. sudo -u postgres psql
3. CREATE DATABASE <database_name>

# Configure Settings.py
1. Update settings.py and update database configuration
2. python manage.py makemigrations api
3. python manage.py migrate

# Run Server
1. python manage.py runserver