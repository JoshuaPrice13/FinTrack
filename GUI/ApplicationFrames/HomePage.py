import customtkinter as ctk
import CustomCTkParts as custom

class HomePage(ctk.CTkFrame):
    """
    A CustomTkinter class that defines the home page frame of the application.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
        welcomeLabel: A label to display a welcome message to the user.
        addTransactionManualButton: A button to navigate to the add transaction frame.
        logoutButton: A button to log out the current user and return to the login frame.
    Methods:
        __init__(): Initializes the HomePage frame with necessary widgets and layout.
    """
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

        self.addTransactionManualButton = ctk.CTkButton(self, text="Add Transactions", command=lambda: self.app.switch_frame(5))
        self.addTransactionManualButton.pack(pady = (10, 10))

        self.logoutButton = ctk.CTkButton(self, text="Logout", command=lambda: custom.logout(self.app, self.controller))
        self.logoutButton.pack(pady = (10, 10))