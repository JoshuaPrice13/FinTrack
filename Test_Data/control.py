import sqlite3
import bcrypt
import os

DB_NAME = "FinTrack_Database"

class Controller:
    def __init__(self):
        # Get full path of the DB
        self.db_path = os.path.abspath(DB_NAME)
        print(f"Using database at: {self.db_path}")
        self._setup_db()

    def _setup_db(self):
        """Ensure users table exists with correct schema."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        # Check if table exists
        cursor.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='users';
        """)
        table_exists = cursor.fetchone()

        if not table_exists:
            # Table doesn't exist, create it
            cursor.execute("""
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """)
            print("Created 'users' table.")
        else:
            # Table exists, check if password_hash column exists
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            if "password_hash" not in columns:
                cursor.execute("ALTER TABLE users ADD COLUMN password_hash TEXT")
                print("Added 'password_hash' column to 'users' table.")

        connection.commit()
        connection.close()

    def add_user(self, username: str, password: str) -> bool:
        """Add a new user with hashed password."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        try:
            cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", 
                           (username, password_hash.decode("utf-8")))
            connection.commit()
            print(f"User '{username}' added successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
            return False
        finally:
            connection.close()

    def authenticate_user(self, username: str, password: str) -> bool:
        """Check if login credentials are valid."""
        connection = sqlite3.connect(self.db_path)
        cursor = connection.cursor()

        cursor.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        row = cursor.fetchone()
        connection.close()

        if row:
            stored_hash = row[0].encode("utf-8")
            if bcrypt.checkpw(password.encode("utf-8"), stored_hash):
                print(f"Login successful. Welcome, {username}!")
                return True
            else:
                print("Invalid password.")
                return False
        else:
            print("Username not found.")
            return False

        
if __name__ == "__main__":
    controller = Controller()

    # Add users
    controller.add_user("alice", "mypassword123")
    controller.add_user("bob", "securepass456")

    # Authenticate
    controller.authenticate_user("alice", "mypassword123")  #success
    controller.authenticate_user("bob", "wrongpass")        #fail
