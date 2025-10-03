import tkinter as tk
import customtkinter as ctk
#from GUITESTS import DummyController as dc
#import Authentication as auth
#Currently using passed-in controller; change that once Authentication class is ready

class LoginWindow(ctk.CTkFrame):
    """
    A frame with login fields to authenticate a user. Uses a controller for
    logic functions to preserve MVC architecture.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        usernameField: The entry field for the username.
        passwordField: The entry field for the password.
        login_button: The button to submit the login form.
        newUserButton: The button to navigate to the Add User frame.
        resetButton: The button to navigate to the Reset Password frame.
    Methods:
        authenticate(): Authenticates the user using the controller.
        login(): Handles the login process and frame switching upon success.
    """

    def __init__(self, master, controller, app, **kwargs):
        """
        Initializes the frame by setting controller and creating text fields
        and button.

        Args:
            (Mandatory)
            master: The frame this one belongs to
            control: The controller
            app: The main application instance for frame switching
            (Optional)
            **kwargs: Any extra arguments to be passed to the super function

        """
        super().__init__(master, **kwargs)
        self.configure(height=900, width=1000)
        self.controller = controller
        self.app = app

        label1 = ctk.CTkLabel(self, font=("Helvetica", 40), text="Login")
        label1.pack(pady = (20, 10))

        self.failedLoginLabel = ctk.CTkLabel(self, font=("Arial", 16), text="Login failed; invalid username or password", text_color="red")

        self.usernameField = ctk.CTkEntry(self, width = 300, height = 40, placeholder_text="Username", font=("Arial", 16))
        self.usernameField.pack(padx = 20, pady = 10)

        self.passwordField = ctk.CTkEntry(self, width = 300, height = 40, placeholder_text="Password", font=("Arial", 16), show="*")
        self.passwordField.pack(padx = 20, pady = 10)

        self.loginButton = ctk.CTkButton(self, text="Login", command=self.login)
        self.loginButton.pack(padx = 40, pady = (20, 5))

        self.newUserButton = ctk.CTkButton(self, fg_color = "transparent", text = "Add User", command=lambda: self.app.switch_frame(1))
        self.newUserButton.pack(padx = 40, pady = 5)

        self.resetButton = ctk.CTkButton(self, fg_color = "transparent", text = "Reset Password", command=lambda: self.app.switch_frame(6))
        self.resetButton.pack(padx = 40, pady = 5)


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
            return self.controller.authenticate_user(user, pwd)
        else:
            print("No controller found")
            return False #Error handle here in the future; this return can be confused with failed login

    def login(self):
        """
        Calls authenticate() and deals with the results
        """
        if self.authenticate():
            self.controller.set_current_user(self.usernameField.get())
            self.app.switch_frame(4) #Switch to home page on successful login
        else:
            self.failedLoginLabel.pack(pady = (0, 10)) #Show the failed login label
            print("Login rejected; try again")