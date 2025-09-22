#Test file
import FinTrackGui as ftg
import LoginWindow as lw

class DummyController():
     """
     Used to test integration with the controller. Final method will
     use a class in the controller, not a controller object like here,
     but the validateCredentials function is what's really being tested here.
     """

     usernames = ["gtroast", "gmczalen", "acallist", "bvote"]

     passwords = ["1234", "1029384756", "crushbass4ever", "r0b0ts"]

     def __init__(self):
         print("Created controller")

     def validateCredentials(self, username, password):
         """
         Takes passed-in username and password, checks them against a
         database (here just arrays) of saved values

         Note: not good with values that just don't exist, but for testing
         purposes, this works.

         Returns
            boolean: True if the values exist and match indexes, false otherwise
         """
         ui = self.usernames.index(username)
         pi = self.passwords.index(password)
         if ui == pi:
             return True
         else:
             return False

if __name__ == "__main__":
    controller = DummyController()
    app = ftg.FinTrackGui(controller)
    app.mainloop()