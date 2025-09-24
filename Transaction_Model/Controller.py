from datetime import date
from Transaction import Transaction
from TransactionType import TransactionType

from datetime import date
from typing import List, Optional
from transaction import Transaction, TransactionType


class TransactionController:
    """
    Controller class to manage transactions.
    """

    def __init__(self):
        self.transactions: List[Transaction] = []

    def add_transaction(self,
                        transaction_type: TransactionType,
                        price: float,
                        transaction_date: date,
                        category: str,
                        description: Optional[str] = None,
                        categorized_by_ai: Optional[bool] = None) -> Transaction:
        """
        Create and store a new Transaction object.
        """
        transaction = Transaction(
            transaction_type=transaction_type,
            price=price,
            date=transaction_date,
            category=category,
            description=description,
            categorized_by_ai=categorized_by_ai
        )
        self.transactions.append(transaction)
        return transaction

    def get_all_transactions(self) -> List[Transaction]:
        return self.transactions

    def get_total_income(self) -> float:
        return sum(t.price for t in self.transactions if t.is_income)

    def get_total_spending(self) -> float:
        return sum(t.price for t in self.transactions if t.is_spending)

    def get_transactions_by_category(self, category: str) -> List[Transaction]:
        return [t for t in self.transactions if t.category.lower() == category.lower()]

if __name__ == "__main__":
  print("test")
