import sqlite3

def create_database():
    """Create database tables for FinTrack application"""
    connection = sqlite3.connect("FinTrack_Database")
    cursor = connection.cursor()

    # Users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Transactions table - stores bank transactions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        transaction_date DATE NOT NULL,
        description TEXT NOT NULL,
        amount REAL NOT NULL,
        category TEXT,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    )
    """)

    # Create indexes for better performance
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)")

    connection.commit()
    connection.close()
    print("Database and tables created successfully!")

def add_user(username, password):
    """Add a new user to the database"""
    connection = sqlite3.connect("FinTrack_Database")
    cursor = connection.cursor()
    
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        print(f"User '{username}' added successfully.")
    except sqlite3.IntegrityError:
        print(f"Username '{username}' already exists. Choose another.")
    
    connection.close()

def authenticate_user(username, password):
    """Authenticate a user login"""
    connection = sqlite3.connect("FinTrack_Database")
    cursor = connection.cursor()
    
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    
    connection.close()
    
    if user:
        print(f"Login successful. Welcome, {username}!")
        return True
    else:
        print("Invalid username or password.")
        return False

# Initialize the database
if __name__ == "__main__":
    create_database()