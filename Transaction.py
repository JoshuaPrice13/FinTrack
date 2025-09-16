from datetime import date
from typing import Optional
#Local imports
from TransactionType import TransactionType


class Transaction:
    """
    A transaction object representing a financial transaction.
    
    Attributes:
        transaction_type (TransactionType): Type of transaction (SPENDING or INCOME)
        price (float): Amount of money (should be positive)
        transaction_date (date): Date of the transaction
        year (int): Year extracted from date
        month (int): Month extracted from date  
        day (int): Day extracted from date
        category (str): Category of the transaction
        description (Optional[str]): Merchant or transaction notes
        categorized_by_ai (Optional[bool]): Whether categorized by AI
    """

    def __init__(self, 
                 transaction_type: TransactionType, 
                 price: float, 
                 date: date, 
                 category: str, 
                 description: Optional[str] =None, 
                 categorized_by_ai: Optional[bool] =None):
        """
        Initialization of a transaction object with parameters.
        This function can be 'overloaded' with simply just the mandatory
        args, or with the mandatory and optional args.

        Args:
            (Mandatory)
            transaction_type (TransactionType): SPENDING or INCOME
            price (float): Amount of money 
            date (datetime.date): FORMAT:YYYY-MM-DD
            category (str): Category of the transaction

            (Optional)
            description (str): String of merchant or transaction notes
            categorized_by_ai (boolean): 0=Not categorized by ai | 1=Was categorized by ai

        Returns:
            N/A. Contructor function

        Raises:
            ValueError: If price is negative or category is empty
        """

        #Check for out of bounds price
        if price < 0:
            raise ValueError("Price must be non-negative")
        #Check for empty category
        if not category or not category.strip():
            raise ValueError("Category cannot be empty")

        #Mandatory
        self.transaction_type = transaction_type
        self.price = price
        self.date = date
            # Parse the date into indivdual components for ease of access
        self.year = date.year
        self.month = date.month
        self.day = date.day
        self.category = category.strip()

        #Optional
        self.description = description.strip() if description else None
        self.categorized_by_ai = categorized_by_ai

    def __str__(self) -> str:
        """String representation of the transaction."""
        type_str = "Income" if self.transaction_type == TransactionType.INCOME else "Spending"
        return f"{type_str}: ${self.price:.2f} - {self.category} ({self.date})"
    
    def __repr__(self) -> str:
        """Developer representation of the transaction."""
        return (f"Transaction(type={self.transaction_type}, price={self.price}, "
                f"date={self.date}, category='{self.category}')")
    

    @property
    def is_income(self) -> bool:
        """Check if transaction is income."""
        return self.transaction_type == TransactionType.INCOME
    
    @property  
    def is_spending(self) -> bool:
        """Check if transaction is spending."""
        return self.transaction_type == TransactionType.SPENDING
    


if __name__ == "__main__":
    t1 = Transaction(
        TransactionType.SPENDING, 
        25.99, 
        date(2024, 9, 16), 
        "Food"
    )
    t2 = Transaction(
        TransactionType.INCOME,
        1500.00,
        date(2024, 9, 15),
        "Salary",
        description="Monthly salary",
        categorized_by_ai=False
    )
    
    print(t1)  # Spending: $25.99 - Food (2024-09-16)
    print(repr(t2))  # Income: $1500.00 - Salary (2024-09-15)
    print(f"Is income: {t2.is_income}")

