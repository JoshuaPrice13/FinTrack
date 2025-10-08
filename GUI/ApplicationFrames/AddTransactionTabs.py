import customtkinter as ctk
from tkcalendar import Calendar

class AddTransactionTabs(ctk.CTkTabview):
    """
    A CustomTkinter class that defines a tabbed view for submitting new transaction data
    to the application. Uses two other classes for the contents of each tab.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
    Tabs:
        "Manual": Tab for manually entering transaction details.
        "File Upload": Tab for uploading files to add transactions.
    """

    def __init__(self, master, controller, app, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(height=300, width=200)
        self.controller = controller
        self.app = app

        homeButton = ctk.CTkButton(self, text="Home", command=lambda: self.app.switch_frame(4))

        #Tab for adding transactions manually
        self.add("Manual")

        addTransactionFrame = AddTransactionFrame(self.tab("Manual"), self.controller, self.app)
        addTransactionFrame.pack(fill="both", expand=True, padx=10, pady=10)

        #Tab for uploading files
        self.add("File Upload")

        uploadLabel = ctk.CTkLabel(self.tab("File Upload"), text="Upload a file to add transactions, either CSV or bank statement")
        uploadLabel.pack(pady=10, padx=10)

        #Organizing tag layout
        self.tab("Manual").grid_columnconfigure(0, weight=1)
        self.tab("File Upload").grid_columnconfigure(0, weight=1)
        homeButton.grid(row=0, column=0, sticky="w", padx=10, pady=10)



class AddTransactionFrame(ctk.CTkScrollableFrame):
    """
    A CustomTkinter class that defines the form for manually adding a transaction.

    Attributes:
        controller: The controller instance for handling logic.
        app: The main application instance for frame switching.
    Methods:
        add_transaction(): Gets info from fields and submits to controller to add transaction to database.
    """

    def __init__(self, master, controller, app, **kwargs):
        super().__init__(master, **kwargs)
        self.controller = controller
        self.app = app

        label = ctk.CTkLabel(self, text="Enter Transaction Details")
        label.pack(pady=10, padx=10)

        #Definitely think about grid layout here instead of pack..................._________________________................

        #Transaction type: Spending or Income (0 or 1)
        self.segemented_button_var = ctk.StringVar(value="Spending")
        segemented_button = ctk.CTkSegmentedButton(self, values=["Spending", "Income"],
                                                     variable=self.segemented_button_var)
        segemented_button.pack(pady=10, padx=10)

        dateLabel = ctk.CTkLabel(self, text="Date of Transaction")
        dateLabel.pack(pady=10, padx=10)

        self.calendar = Calendar(self, selectmode='day')
        self.calendar.pack(pady=10, padx=10)

        self.priceField = ctk.CTkEntry(self, placeholder_text="Price")
        self.priceField.pack(pady=10, padx=10)

        #option menu for category
        #there is a master list of categories; user can edit them
        #Also option for AI to categorize

        categoryLabel = ctk.CTkLabel(self, text="Category")
        categoryLabel.pack(pady=10, padx=10)

        self.categoryChoice = ctk.StringVar(value="Select Category")
        optionmenu = ctk.CTkOptionMenu(self,values=controller.get_categories(), variable=self.categoryChoice)
        optionmenu.pack(pady=10, padx=10)


        descriptionLabel = ctk.CTkLabel(self, text="Description")
        descriptionLabel.pack(pady=10, padx=10)

        self.descriptionField = ctk.CTkEntry(self, placeholder_text="(Optional)")
        self.descriptionField.pack(pady=10, padx=10)

        """
        Need for sure:
        - Transaction Type
        - Price
        - Date
        - Category

        Optional:
        - Description
        
        NOTE: no AI categorization for manual, just for file upload. That will have it for sure, no manual option
        """

        addTransactionButton = ctk.CTkButton(self, text="Submit", command=lambda: self.add_transaction())
        addTransactionButton.pack(pady=10, padx=10)


    def add_transaction(self):
        """
        Gets info from fields and submits to controller to add transaction to database.
        """
        #get info from fields and submit to controller
        transaction_type = self.segemented_button_var.get()  # "Spending" or "Income"; 0 or 1 int
        transaction_type = 0 if transaction_type == "Spending" else 1
        price = self.priceField.get() #Convert to float
        date = self.calendar.get_date()  # Format: 'MM/DD/YYYY'
        category = self.categoryChoice.get()
        description = self.descriptionField.get()

        if price == "" or category == "Select Category":
            print("Price and Category are required fields.")
            return
        
        price = float(price)

        print("Type is: " + str(transaction_type))
        print("Price is: " + str(price))
        print("Date is: " + date)
        print("Category is: " + category)
        print("Description is: " + description)

        self.controller.add_transaction(transaction_type, price, date, category, description)
        print("Transaction added!")