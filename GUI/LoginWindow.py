import tkinter as tk
import customtkinter as ctk
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

    def __init__(self, master, control, **kwargs):
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

        self.usernameField = ctk.CTkEntry(self.frame)
        self.usernameField.pack(padx = 20, pady = 10)

        self.passwordField = ctk.CTkEntry(self.frame)
        self.passwordField.pack(padx = 20, pady = 10)

        self.button = ctk.CTkButton(self.frame, text="Login", command=self.login)
        self.button.pack(padx = 40, pady = 20)

        self.controller = control

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
            return self.controller.validateCredentials(user, pwd)

    def login(self):
        """
        Calls authenticate() and deals with the results (currently just prints result)
        """
        if self.authenticate():
            print("Login success!")
        else:
            print("Login rejected; try again")