from datetime import date
from Transaction import Transaction
#from TransactionType import TransactionType

if __name__ == "__main__":
    t1 = Transaction(
        0, 
        25.99, 
        date(2024, 9, 16), 
        "Food"
    )
    t2 = Transaction(
        1,
        1500.00,
        date(2024, 9, 15),
        "Salary",
        description="Monthly salary",
        categorized_by_ai=False
    )
    
    print(t1)
    print(t2)