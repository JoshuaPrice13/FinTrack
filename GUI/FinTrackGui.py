import customtkinter as ctk
import LoginWindow as lw
import AddUserWindow as auw
import ResetPasswordWindow as rpw
import HomePage as hp
import AddTransactionFrame as atf

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

        #Setting themes for the app...
        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "dark-blue", "green"

        self.geometry("500x500")
        #self.minsize(30000, 30000)
        self.title("FinTrack")

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
        self.frames = [lw.LoginWindow, auw.AddUserWindow, rpw.ResetPasswordWindow, rpw.SubmitNewPasswordWindow, hp.HomePage,
                       atf.AddTransactionFrame, rpw.EnterUsernameWindow]

        self.controller = controller
        
        self.currentFrame = None
        self.currentFrame = lw.LoginWindow(self, self.controller, app=self)
        self.currentFrame.pack(fill = "both", expand = True)

        #self.switch_frame(0)
        #self.currentFrame = lw.LoginWindow(self, controller)
        #self.currentFrame.pack()

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
            oldFrame.destroy()
        self.currentFrame = self.frames[new_frame](self, self.controller, app = self)
        self.currentFrame.pack(fill = "both", expand = True)

    def switch(self, new_frame):
        """
        Destroys the current frame and replaces it with a new one.

        Args:
            (Mandatory)
            new_frame: The frame to replace the current one.
        """
        self.currentFrame.destroy()
        self.currentFrame = new_frame(self, self.controller)
        self.currentFrame.pack()