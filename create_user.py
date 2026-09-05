import sqlite3
from werkzeug.security import generate_password_hash


# Connect to database
connection = sqlite3.connect("database.db")

cursor = connection.cursor()


# Create users table if it doesn't already exist
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")


# Login details
username = "farmer"
password = "1234"


# Hash the password
hashed_password = generate_password_hash(password)


# Insert user
try:

    cursor.execute(
        """
        INSERT INTO users (username, password)
        VALUES (?, ?)
        """,
        (username, hashed_password)
    )

    connection.commit()

    print("================================")
    print(" User created successfully!")
    print("================================")
    print("Username:", username)
    print("Password:", password)


except sqlite3.IntegrityError:

    print("User already exists!")


connection.close()