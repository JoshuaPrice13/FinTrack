import customtkinter as ctk

class AddTransactionFrame(ctk.CTkFrame):

    def __init__(self, master, controller, app, **kwargs):
        ctk.CTkFrame.__init__(self, master, **kwargs)
        self.controller = controller
        self.app = app

        label = ctk.CTkLabel(self, text="Enter Transaction Details")
        label.pack(pady=10, padx=10)

        

        addTransactionButton = ctk.CTkButton(self, text="Add Transaction", command=lambda: self.add_transaction)
        addTransactionButton.pack(pady=10, padx=10)

        homeButton = ctk.CTkButton(self, text="Home", command=lambda: self.app.switch_frame(4))
        homeButton.pack()


    def add_transaction(self):
        #get info from fields and submit to controller

        print("Transaction added!")