import customtkinter as ctk
from LoginFrames import LoginWindow as lw
from LoginFrames import AddUserWindow as auw
from LoginFrames import ResetPasswordWindow as rpw
from ApplicationFrames import HomePage as hp
from ApplicationFrames import AddTransactionTabs as att

#Currently using passed-in controller for the login window
#Delete that once Authentication class is ready

class FinTrackGui(ctk.CTk):
    """
    A CustomTkinter class that defines the GUI setup for FinTrack and facilitates
    switching between frames (windows).

    Attributes:
        geometry: The size of the window
        title: The window title
        currentFrame: The current frame being displayed.
        frames: A list of frame classes for easy switching.

    Methods:
        switch_frame(new_frame): Destroys the current frame and replaces it with a new one.
    """

    '''
        * For reference:
        * Login = 0
        * Add User = 1
        * Reset Password = 2
        * Submit New Password = 3
        * Home Page = 4
        * Add Transaction = 5
        * Enter Username for Password Reset = 6
    '''
    frames = [lw.LoginWindow, auw.AddUserWindow, rpw.ResetPasswordWindow, rpw.SubmitNewPasswordWindow, hp.HomePage,
                       att.AddTransactionTabs, rpw.EnterUsernameWindow]

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

        #Setting themes for the app...
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "dark-blue", "green"

        self.geometry("500x500")
        #self.minsize(30000, 30000)
        self.title("FinTrack")

        self.controller = controller
        
        self.currentFrame = None
        self.currentFrame = lw.LoginWindow(self, self.controller, app=self)
        self.currentFrame.pack(fill = "both", expand = True)


    def switch_frame(self, new_frame):
        """
        Destroys the current frame and replaces it with a new one.

        Args:
            (Mandatory)
            c: The index of the frame class to switch to (in self.frames).
        """
        oldFrame = self.currentFrame
        self.currentFrame = None
        if oldFrame is not None:
            oldFrame.pack_forget() # Added to fix issues with CTkScrollableFrame not being fully removed
            oldFrame.destroy()
        self.currentFrame = self.frames[new_frame](self, self.controller, app = self)
        self.currentFrame.pack(fill = "both", expand = True)