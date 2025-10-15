#Test file
import FinTrackGui as ftg
import FinTrackGuiForTests as ftgft
#import controller here to use instead of DummyController


class DummyController():
     """
     Used to test integration with the controller. Final method will
     use a class in the controller, not a controller object like here,
     but the validateCredentials function is what's really being tested here.
     """

     current_user = None

     usernames = ["gtroast", "gmczalen", "acallist", "bvote"]

     passwords = ["1234", "1029384756", "crushbass4ever", "r0b0ts"]

     categories = ["Food", "Rent", "Utilities", "Entertainment", "Miscellaneous"]

     def __init__(self):
         print("Created controller")

     def get_categories(self):
            """
            Dummy method to simulate getting categories from database
            """
            return self.categories

     def check_username_exists(self, username):
         """
         Dummy method to simulate checking if a username exists
         """
         return username in self.usernames

     def set_current_user(self, username):
         """
         Dummy method to simulate setting the current user
         """
         if username in self.usernames:
             self.current_user = username
             print(f"Current user set to {username}")
             return True
         else:
             print("Username not found")
             return False

     def add_user(self, username, password, sq1, sq1a, sq2, sq2a):
         """
         Dummy method to simulate adding a user
         """
         if username in self.usernames:
             print("Username already exists")
             return False
         else:
             self.usernames.append(username)
             self.passwords.append(password)
             print(f"Added user {username}")
             print("Security Question 1: " + sq1
                   + " Answer: " + sq1a
                   + " Security Question 2: " + sq2
                   + " Answer: " + sq2a)
             return True
         
     def reset_password(self, new_password):
            """
            Dummy method to simulate resetting a password
            """
            index = self.usernames.index(self.current_user)
            self.passwords[index] = new_password
            print(f"Password for user {self.current_user} has been reset")
            return True

     def authenticate_user(self, username, password):
         """
         Takes passed-in username and password, checks them against a
         database (here just arrays) of saved values

         Note: not good with values that just don't exist, but for testing
         purposes, this works.

         Returns
            boolean: True if the values exist and match indexes, false otherwise
         """
         if (username in self.usernames
              and password in self.passwords
              and (self.usernames.index(username) == self.passwords.index(password))):
             return True
         else:
             return False
         
     def add_transaction(self, transaction_type, price, transaction_date, category, description=None, categorized_by_ai=None):
            """
            Dummy method to simulate adding a transaction
            """
            print("Transaction added with the following details:")
            print(f"Type: {transaction_type}, Price: {price}, Date: {transaction_date}, Category: {category}, Description: {description}, AI Categorized: {categorized_by_ai}")
            return True
     
     def process_transaction_file(self, file_path):
            """
            Dummy method to simulate processing a transaction file
            """
            print(f"Processing file: {file_path}")
            return True

if __name__ == "__main__":
    controller = DummyController()
    #app = ftg.FinTrackGui(controller) #Use this for actual gui
    app = ftgft.FinTrackGuiForTests(controller) #Use this for testing purposes

    app.after(0, lambda:app.state('zoomed'))

    app.mainloop()