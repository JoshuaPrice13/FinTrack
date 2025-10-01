import customtkinter as ctk


class ResetPasswordWindow(ctk.CTkFrame):
    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        #self.frame = ctk.CTk()
        self.configure(height=300, width=200)
        self.controller = control
        self.app = app

        label1 = ctk.CTkLabel(self, text="Reset Password") #Change text font and size later
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

        #self.frame.mainloop()

    def submit_answers(self):
        #Get all the data from the fields and submit them to the controller
        sq1 = self.sQ1AnswerField.get()
        sq2 = self.sQ2AnswerField.get()

        #controller.reset_password(sq1, sq2) !!!!!!!

        self.app.switch_frame(3) #Switch back to login window after submission

        return True
    

class SubmitNewPasswordWindow(ctk.CTkFrame):
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

    def submit_new_password(self):
        #Get all the data from the fields and submit them to the controller
        newPwd = self.newPasswordField.get()
        repeatNewPwd = self.repeatNewPasswordField.get()

        if newPwd != repeatNewPwd:
            print("Passwords do not match") #Maybe do something with revealing a text label/prompt on the window later
            return False

        #controller.submit_new_password(newPwd) !!!!!!!

        self.app.switch_frame(0) #Switch back to login window after submission

        return True