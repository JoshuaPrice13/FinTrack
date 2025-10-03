import customtkinter as ctk
import CustomCTkParts as custom


class AddUserWindow(ctk.CTkFrame):
    """
    A CustomTkinter class that provides a form for adding a new user.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        newUsernameField: The entry field for the new username.
        newPasswordField: The entry field for the new password.
        securityQuestion1Field: The entry field for security question 1.
        sQ1AnswerField: The entry field for the answer to security question 1.
        securityQuestion2Field: The entry field for security question 2.
        sQ2AnswerField: The entry field for the answer to security question 2.
    Methods:
        submit_new_user(): Submits information in fields to controller to add new user.
    """


    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=300, width=200)
        self.controller = control
        self.app = app

        #label1 = ctk.CTkLabel(self.frame, text="New Username")
        #label1.pack()

        self.newUsernameField = ctk.CTkEntry(self, placeholder_text="Enter new username")
        self.newUsernameField.pack(padx = 20, pady = 10)

        #label2 = ctk.CTkLabel(self.frame, text="New Password")
        #label2.pack()

        self.newPasswordField = ctk.CTkEntry(self, placeholder_text="Enter new password", show="*")
        self.newPasswordField.pack(padx = 20, pady = 10)

        label3 = ctk.CTkLabel(self, text="Security Question 1")
        label3.pack()

        self.securityQuestion1Field = ctk.CTkEntry(self)
        self.securityQuestion1Field.pack(padx = 20, pady = 10)

        label4 = ctk.CTkLabel(self, text="Answer 1")
        label4.pack(padx = 20, pady = (10, 5))

        self.sQ1AnswerField = ctk.CTkEntry(self)
        self.sQ1AnswerField.pack(padx = 20, pady = (5, 10))

        label5 = ctk.CTkLabel(self, text="Security Question 2")
        label5.pack(padx = 20, pady = (10, 5))

        self.securityQuestion2Field = ctk.CTkEntry(self)
        self.securityQuestion2Field.pack(padx = 20, pady = (5, 10))

        label6 = ctk.CTkLabel(self, text="Answer 2")
        label6.pack(padx = 20, pady = (10, 5))

        self.sQ2AnswerField = ctk.CTkEntry(self)
        self.sQ2AnswerField.pack(padx = 20, pady = (5, 10))

        self.addButton = ctk.CTkButton(self, text="Add User", command=lambda: self.submit_new_user())
        self.addButton.pack(padx = 40, pady = 20)

        self.backButton = ctk.CTkButton(self, fg_color = "transparent", text="Back to Login", command=lambda: custom.logout(self.app, self.controller))

    def submit_new_user(self):
        """
        Gathers new user information from fields and submits to controller to add
        to database. Navigates back to login frame upon success.
        
        Currently no error handling, could do this later. (example: username already exists,
        password requirements not met, security questions not filled out, etc.)
        """
        #Get all the data from the fields and submit them to the controller
        newUser = self.newUsernameField.get()
        newPwd = self.newPasswordField.get()
        sq1 = self.securityQuestion1Field.get()
        sq1a = self.sQ1AnswerField.get()
        sq2 = self.securityQuestion2Field.get()
        sq2a = self.sQ2AnswerField.get()

        self.controller.add_user(newUser, newPwd, sq1, sq1a, sq2, sq2a)

        custom.logout(self.app, self.controller)