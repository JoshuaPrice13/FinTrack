import customtkinter as ctk
import LoginWindow as lw

#Currently using passed-in controller for the login window
#Delete that once Authentication class is ready

class FinTrackGui(ctk.CTk):
    """
    A CustomTkinter class that defines the GUI setup for FinTrack and facilitates
    switching between frames (windows).

    Attributes:
        geometry: The size of the window
        title: The window title
        login_frame: The login window, first to appear when the app is opened
    """
    def __init__(self, controller):
        """
        Initializes the GUI by creating the necessary frames and setting the login frame
        as the frame to display.

        Args:
            (Mandatory)
            controller: A controller object passed to the login_frame for authentication.
                        Will be removed with later updates.
        """
        super().__init__()
        self.geometry("3000x3000")
        #self.minsize(30000, 30000)
        self.title("FinTrack")
        
        self.login_frame = lw.LoginWindow(self, controller)
        self.login_frame.pack()