import customtkinter as ctk

"""
File used to create custom parts for the GUI that are used in multiple files. Not
declared as an instance of a class, just a collection of functions.
"""


def logout(app, controller):
    """
    Set current user to None and switch to login frame
    Parameters:
        app (FinTrackGui): The main application instance for frame switching.
        controller (Controller): The controller instance for handling logic.
    """
    #controller.current_user(None)
    controller.current_user = None
    # controller.set_current_user(None) original
    app.switch_frame(0)