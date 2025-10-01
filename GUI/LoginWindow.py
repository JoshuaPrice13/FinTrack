import tkinter as tk
import customtkinter as ctk
#from GUITESTS import DummyController as dc
#import Authentication as auth
#Currently using passed-in controller; change that once Authentication class is ready

class LoginWindow(ctk.CTkFrame):
    """
    A window with login fields to authenticate a user. Uses a controller for
    logic functions to preserve MVC architecture.

    Attributes:
        frame: The frame to hold the login widgets
        usernameField: Text entry box to receive the username
        passwordField: Text entry box to receive the password
        controller: Controller object to perform authentication requests
    """

    def __init__(self, master, controller, app, **kwargs):
        """
        Initializes the frame by setting controller and creating text fields
        and button.

        Args:
            (Mandatory)
            master: The frame this one belongs to
            control: The controller
            **kwargs: Any extra arguments to be passed to the super function

        """
        super().__init__(master, **kwargs)
        self.frame = ctk.CTk()
        self.configure(height=700, width=700)
        self.frame.title("FinTrack Login")
        self.controller = controller
        self.app = app

        #label1 = ctk.CTkLabel(self.frame, text="Username")
        #label1.pack()

        self.usernameField = ctk.CTkEntry(self.frame, placeholder_text="Username")
        self.usernameField.pack(padx = 20, pady = 10)

        #label2 = ctk.CTkLabel(self.frame, text="Password")
        #label2.pack()

        self.passwordField = ctk.CTkEntry(self.frame, placeholder_text="Password", show="*")
        self.passwordField.pack(padx = 20, pady = 10)

        self.login_button = ctk.CTkButton(self.frame, text="Login", command=self.login)
        self.login_button.pack(padx = 40, pady = 20)

        self.reset_button = ctk.CTkButton(self.frame, text = "Forgot Password", command=lambda: self.app.switch_frame(1))
        self.reset_button.pack(padx = 40, pady = 20)

        self.frame.mainloop()

    def authenticate(self):
        """
        Gets the data from the username and password entry fields and checks
        them using an authentication function provided by the controller.

        Returns:
            boolean: A true or false to signify whether the login was successful
        """
        if self.controller:
            user = self.usernameField.get()
            pwd = self.passwordField.get()

            #Replace the below line with the function from the Authenticate class, whenever it is ready
            #Errors if values are not in list or values are empty strings
            return self.controller.authenticate_user(user, pwd)
        else:
            print("No controller found")
            return False

    def login(self):
        """
        Calls authenticate() and deals with the results (currently just prints result)
        """
        if self.authenticate():
            print("Login success!")
        else:
            print("Login rejected; try again")