import customtkinter as ctk
import CustomCTkParts as custom

class HomePage(ctk.CTkFrame):
    def __init__(self, master, controller, app, **kwargs):
        """
        The login window frame.

        Parameters:
            master (ctk.CTk): The parent widget.
            controller (Controller): The controller instance for handling logic.
            app (FinTrackGui): The main application instance for frame switching.
            **kwargs: Additional keyword arguments for the ctk.CTkFrame.
        """
        super().__init__(master, **kwargs)
        self.controller = controller
        self.app = app

        label1 = ctk.CTkLabel(self, font=("Arial", 24), text="Home Page")
        label1.pack(pady = (20, 10))

        self.welcomeLabel = ctk.CTkLabel(self, font=("Arial", 16), text=(f"Welcome, {self.controller.current_user}!"))
        self.welcomeLabel.pack(pady = (10, 10))

        self.addTransactionManualButton = ctk.CTkButton(self, text="Add Transaction Manually", command=lambda: self.app.switch_frame(5))
        self.addTransactionManualButton.pack(pady = (10, 10))

        self.logoutButton = ctk.CTkButton(self, text="Logout", command=lambda: custom.logout(self.app, self.controller))
        self.logoutButton.pack(pady = (10, 10))