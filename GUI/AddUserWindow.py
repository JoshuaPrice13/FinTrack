import customtkinter as ctk


#So everything but the class name was AI added... not sure if it's good or not
class AddUserWindow(ctk.CTkFrame):


    def __init__(self, master, control, app, **kwargs):
        super().__init__(master, **kwargs)
        self.frame = ctk.CTk()
        self.configure(height=300, width=200)
        #self.title("Add User")
        #self.geometry("300x200")
        self.frame.title("FinTrack Add User")
        self.controller = control
        self.app = app

        label1 = ctk.CTkLabel(self.frame, text="New Username")
        label1.pack()

        self.newUsernameField = ctk.CTkEntry(self.frame)
        self.newUsernameField.pack(padx = 20, pady = 10)

        label2 = ctk.CTkLabel(self.frame, text="New Password")
        label2.pack()

        self.newPasswordField = ctk.CTkEntry(self.frame)
        self.newPasswordField.pack(padx = 20, pady = 10)

        label3 = ctk.CTkLabel(self.frame, text="Security Question 1")
        label3.pack()

        self.securityQuestion1Field = ctk.CTkEntry(self.frame)
        self.securityQuestion1Field.pack(padx = 20, pady = 10)

        label4 = ctk.CTkLabel(self.frame, text="Answer 1")
        label4.pack()

        self.sQ1AnswerField = ctk.CTkEntry(self.frame)
        self.sQ1AnswerField.pack(padx = 20, pady = 10)

        label5 = ctk.CTkLabel(self.frame, text="Security Question 2")
        label5.pack()

        self.securityQuestion2Field = ctk.CTkEntry(self.frame)
        self.securityQuestion2Field.pack(padx = 20, pady = 10)

        label6 = ctk.CTkLabel(self.frame, text="Answer 2")
        label6.pack()

        self.sQ2AnswerField = ctk.CTkEntry(self.frame)
        self.sQ2AnswerField.pack(padx = 20, pady = 10)

        self.addButton = ctk.CTkButton(self.frame, text="Add User", command=lambda: self.submit_new_user())
        self.addButton.pack(padx = 40, pady = 20)

        self.frame.mainloop()

    def submit_new_user(self):
        print("Submitted new user")
        #Get all the data from the fields and submit them to the controller
        newUser = self.newUsernameField.get()
        newPwd = self.newPasswordField.get()
        sq1 = self.securityQuestion1Field.get()
        sq1a = self.sQ1AnswerField.get()
        sq2 = self.securityQuestion2Field.get()
        sq2a = self.sQ2AnswerField.get()
        #Submit to controller here
        print("New user: " + newUser
              + "\nNew password: " + newPwd
              + "\nSecurity Question 1: " + sq1
              + "\nAnswer 1: " + sq1a
              + "\nSecurity Question 2: " + sq2
              + "\nAnswer 2: " + sq2a)
        self.app.switch_frame(0)
        return True