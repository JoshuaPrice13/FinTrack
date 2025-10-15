import sqlite3
from datetime import datetime
import FinTrackGui as ftg
from LoginFrames.LoginWindow import LoginWindow
from cryptography.fernet import Fernet
from ApplicationFrames.HomePage import HomePage

class Controller:

    _encryption_key = b'mQ_B2m7F4RqqBQ74df4xPz6Qy4VeKVpBjhZYlvi6iF0='
    _cipher = Fernet(_encryption_key)

    def __init__(self, db_path="FinTrack_Database"):
        self.db_path = db_path
        self.current_user = None

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def encrypt_text(self, plain_text):
        return self._cipher.encrypt(plain_text.encode()).decode()

    def decrypt_text(self, encrypted_text):
        return self._cipher.decrypt(encrypted_text.encode()).decode()

    def add_user(self, username, password, sq1, sa1, sq2, sa2):
        conn = self._connect()
        cursor = conn.cursor()
        try:
            encrypted_password = self.encrypt_text(password)
            encrypted_sa1 = self.encrypt_text(sa1)
            encrypted_sa2 = self.encrypt_text(sa2)

            cursor.execute(
                "INSERT INTO users (username, password, security_question_1, security_answer_1, security_question_2, security_answer_2) VALUES (?, ?, ?, ?, ?, ?)",
                (username, encrypted_password, sq1, encrypted_sa1, sq2, encrypted_sa2)
            )
            conn.commit()
            print(f"User '{username}' added successfully.")
            return True
        except sqlite3.IntegrityError:
            print(f"Username '{username}' already exists.")
            return False
        finally:
            conn.close()
            
            
    def get_security_questions(self, username):
        """Get security questions for a specific user"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT security_question_1, security_question_2 FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
    
        if result:
            return {"question1": result[0], "question2": result[1]}
        return None

    def verify_security_answers(self, username, answer1, answer2):
        """Verify both security answers for password recovery"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT security_answer_1, security_answer_2 FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
    
        if result:
            # Decrypt the stored answers
            stored_answer1 = self.decrypt_text(result[0])
            stored_answer2 = self.decrypt_text(result[1])
        
            # Compare case-insensitive
            if stored_answer1.lower() == answer1.lower() and stored_answer2.lower() == answer2.lower():
                return True
        return False

    def create_database(self):
        """Create database tables if they don't exist"""
        connection = self._connect()
        cursor = connection.cursor()

        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            security_question_1 TEXT NOT NULL,
            security_answer_1 TEXT NOT NULL,
            security_question_2 TEXT NOT NULL,
            security_answer_2 TEXT NOT NULL
        )
        """)

        # Transactions table
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

        # Stocks table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            stock_id TEXT NOT NULL,
            amount INTEGER NOT NULL,
            paid_value REAL NOT NULL,
            purchase_date DATE DEFAULT CURRENT_DATE,
            current_value REAL,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        )
        """)

        # Indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_user_id ON transactions(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions(transaction_date)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stocks_user_id ON stocks(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_stocks_stock_id ON stocks(stock_id)")

        connection.commit()
        connection.close()
        print("Database and tables created successfully!")

    def authenticate_user(self, username, password):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()

        if result:
            stored_encrypted_password = result[0]
            try:
                decrypted_password = self.decrypt_text(stored_encrypted_password)
                if decrypted_password == password:
                    self.current_user = username
                    print(f"Login successful. Welcome, {username}!")
                    return True
            except Exception as e:
                print(f"Decryption error: {e}")

        print("Invalid username or password.")
        return False

    def get_security_questions(self, username):
        """Get security questions for a specific user"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT security_question_1, security_question_2 FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {"question1": result[0], "question2": result[1]}
        return None

    def verify_security_answers(self, username, answer1, answer2):
        """Verify both security answers for password recovery"""
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT security_answer_1, security_answer_2 FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        
        if result:
            try:
                # Decrypt the stored answers
                stored_answer1 = self.decrypt_text(result[0])
                stored_answer2 = self.decrypt_text(result[1])
                
                # Compare case-insensitive
                if stored_answer1.lower() == answer1.lower() and stored_answer2.lower() == answer2.lower():
                    return True
            except Exception as e:
                print(f"Decryption error: {e}")
        return False

    def reset_password(self, username, new_password):
        conn = self._connect()
        cursor = conn.cursor()
        encrypted_password = self.encrypt_text(new_password)
        cursor.execute("UPDATE users SET password=? WHERE username=?", (encrypted_password, username))
        conn.commit()
        conn.close()
        print(f"Password updated for user {username}.")
        return True

    def get_user_id(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        if result:
            return result[0]
        return None

    def add_transaction(self, user_id, transaction_date, description, amount, category=None):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO transactions (user_id, transaction_date, description, amount, category) VALUES (?, ?, ?, ?, ?)",
            (user_id, transaction_date, description, amount, category)
        )
        conn.commit()
        conn.close()
        print("Transaction added.")
        return True

    def get_categories(self):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT category FROM transactions WHERE category IS NOT NULL")
        categories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return categories

    def get_transactions_for_user(self, user_id):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT transaction_date, description, amount, category FROM transactions WHERE user_id=?", (user_id,))
        transactions = cursor.fetchall()
        conn.close()
        return transactions

    def check_username_exists(self, username):
        conn = self._connect()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM users WHERE username=?", (username,))
        result = cursor.fetchone()
        conn.close()
        return result is not None

if __name__ == "__main__":
    ctrl = Controller()

    # Create tables if they don't exist
    ctrl.create_database()

    # Add a test user
    username = "admin"
    password = "password"
    sq1 = "Your first pet's name?"
    sa1 = "Fluffy"
    sq2 = "Favorite color?"
    sa2 = "Blue"
    ctrl.add_user(username, password, sq1, sa1, sq2, sa2)

    # Authenticate test user
    if ctrl.authenticate_user(username, password):
        user_id = ctrl.get_user_id(username)

        # Add a transaction for the user
        ctrl.add_transaction(
            user_id=user_id,
            transaction_date=datetime.now().strftime("%Y-%m-%d"),
            description="Grocery shopping",
            amount=45.60,
            category="Food"
        )

        # Get and print categories
        categories = ctrl.get_categories()
        print("Categories in DB:", categories)

        # Get and print transactions for the user
        transactions = ctrl.get_transactions_for_user(user_id)
        print("Transactions for user:")
        for t in transactions:
            print(t)

    controller = Controller()
    controller.create_database()

    app = ftg.FinTrackGui(controller)
    app.after(0, lambda: app.state('zoomed'))
    app.mainloop()