import sqlite3

# Setup database and create users table
connection = sqlite3.connect("FinTrack_Database")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
""")

connection.commit()
connection.close()

def add_user(username, password):
    connection = sqlite3.connect("FinTrack_Database")
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        print(f" User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f" Username '{username}' already exists. Choose another.")
    
    connection.close()

def authenticate_user(username, password):
    connection = sqlite3.connect("FinTrack_Database")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    connection.close()
    
    if user:
        print(f" Login successful. Welcome, {username}!")
        return True
    else:
        print(" Invalid username or password.")
        return False
