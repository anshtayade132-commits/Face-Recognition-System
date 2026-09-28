import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

def connect_database():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )

        print("MySQL connected successfully!")
        return connection

    except mysql.connector.Error as error:
        print("Database connection failed:", error)
        return None