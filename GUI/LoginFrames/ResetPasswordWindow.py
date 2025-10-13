import customtkinter as ctk
import CustomCTkParts as custom

class EnterUsernameWindow(ctk.CTkFrame):
    """
    A CustomTkinter class that provides a form for users to enter their username.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        usernameField: The entry field for the username.
        userNotExistLabel: A label to indicate that the entered username does not exist.
    Methods:
        submit_username(): Checks if the entered username exists and navigates to the next frame if it does.
    """

    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=300, width=200)
        self.controller = control
        self.app = app

        label1 = ctk.CTkLabel(self, text="Enter Username") #Change text font and size later
        label1.pack()

        self.usernameField = ctk.CTkEntry(self, placeholder_text="Username")
        self.usernameField.pack(padx = 20, pady = 10)

        self.userNotExistLabel = ctk.CTkLabel(self, font=("Arial", 12), text="Username does not exist", text_color="red")

        submitButton = ctk.CTkButton(self, text="Submit Username", command=lambda: self.submit_username())
        submitButton.pack(padx = 40, pady = 20)

        backButton = ctk.CTkButton(self, fg_color = "transparent", text="Back to Login", command=lambda: custom.logout(self.app, self.controller))
        backButton.pack(padx = 40, pady = 5)


    def submit_username(self):
        """
        Checks entered username and navigates to next frame in sequence if username exists.
        Otherwise, shows error message.
        """
        #Get all the data from the fields and submit them to the controller
        user = self.usernameField.get()

        if self.controller.check_username_exists(user):
            self.controller.current_user = user
           #self.controller.set_current_user(user) Changed
            print("Username exists")
            self.app.switch_frame(2)
        else:
            self.userNotExistLabel.pack() #Show the username does not exist label
            print("Username does not exist")


class ResetPasswordWindow(ctk.CTkFrame):
    """
    A CustomTkinter class that provides a form for users to answer their
    security questions.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        sQ1AnswerField: The entry field for the answer to security question 1.
        sQ2AnswerField: The entry field for the answer to security question 2.
    Methods:
        submit_answers(): Submits security question answers to the controller for verification.
    """

    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        #self.frame = ctk.CTk()
        self.configure(height=300, width=200)
        self.controller = control
        self.app = app

        label1 = ctk.CTkLabel(self, text="Security Questions") #Change text, font, and size later
        label1.pack()

        question1 = ctk.CTkLabel(self, text="Get security question 1 from database")
        question1.pack()

        self.sQ1AnswerField = ctk.CTkEntry(self, placeholder_text="Answer")
        self.sQ1AnswerField.pack(padx = 20, pady = 10)

        question2 = ctk.CTkLabel(self, text="Get security question 2 from database")
        question2.pack()

        self.sQ2AnswerField = ctk.CTkEntry(self, placeholder_text="Answer")
        self.sQ2AnswerField.pack(padx = 20, pady = 10)

        resetButton = ctk.CTkButton(self, text="Reset Password", command=lambda: self.submit_answers())
        resetButton.pack(padx = 40, pady = 20)

        backButton = ctk.CTkButton(self, fg_color = "transparent", text="Back to Login", command=lambda: custom.logout(self.app, self.controller))
        backButton.pack(padx = 40, pady = 5)


    def submit_answers(self):
        """
        Submits security question answers to the controller for verification.
        Navigates to next frame in sequence if answers are correct.
        Otherwise, shows error message.
        """
        #Get all the data from the fields and submit them to the controller
        sq1 = self.sQ1AnswerField.get()
        sq2 = self.sQ2AnswerField.get()

        #controller.reset_password(sq1, sq2) !!!!!!!

        self.app.switch_frame(3) #Switch to submit new password window on successful verification
        #Need to add error handling for incorrect answers later

        return True
    

class SubmitNewPasswordWindow(ctk.CTkFrame):
    """
    A CustomTkinter class that provides a form for users to submit a new password.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        newPasswordField: The entry field for the new password.
        repeatNewPasswordField: The entry field for re-entering the new password.
    Methods:
        submit_new_password(): Submits new password to the controller for updating in the database.
    """

    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        #self.frame = ctk.CTk()
        self.configure(height=300, width=200)
        #self.frame.title("FinTrack Submit New Password")
        self.controller = control
        self.app = app

        label1 = ctk.CTkLabel(self, text="Submit New Password") #Change text font and size later
        label1.pack()

        self.newPasswordField = ctk.CTkEntry(self, placeholder_text="Enter new password", show="*")
        self.newPasswordField.pack(padx = 20, pady = 10)

        self.repeatNewPasswordField = ctk.CTkEntry(self, placeholder_text="Re-enter new password", show="*")
        self.repeatNewPasswordField.pack(padx = 20, pady = 10)

        submitButton = ctk.CTkButton(self, text="Submit New Password", command=lambda: self.submit_new_password())
        submitButton.pack(padx = 40, pady = 20)

        #Maybe add back to login button?

    def submit_new_password(self):
        """
        Submits new password to the controller for updating in the database.
        Navigates back to login frame upon success. If failed, shows error message.
        """
        #Get all the data from the fields and submit them to the controller
        newPwd = self.newPasswordField.get()
        repeatNewPwd = self.repeatNewPasswordField.get()

        if newPwd != repeatNewPwd:
            print("Passwords do not match") #Maybe do something with revealing a text label/prompt on the window later
            return False

        #controller.submit_new_password(newPwd) !!!!!!!
        self.controller.reset_password(newPwd)

        custom.logout(self.app, self.controller) #Switch back to login window after submission

        return True