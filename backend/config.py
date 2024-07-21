import os
import mysql.connector

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False


class Config:
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'  # USE YOUR USER
    MYSQL_PASSWORD = ''  # USE YOUR PASSWORD
    MYSQL_DB = 'kic_db'
    JWT_SECRET_KEY = os.environ.get('SECRET_KEY') or 'supersecretkey'

    try:
        # Connect to the MySQL databaseMYSQL_PASSWORD
        db = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB
        )
        
        # Check if the connection is successful
        if db.is_connected():
            print("Connected to MySQL database!")
            # Perform database operations here
            
        else:
            print("Failed to connect to MySQL database.")
            
    except mysql.connector.Error as error:
        print("Error connecting to MySQL database:", error)
