from enum import Enum

""""

For Controller:
    When creating Transaction object, use this class for the proper argument expected.
    Example passed argument from controller side:
        TransactionType(SPENDING)

"""
class TransactionType(Enum):
    SPENDING = 0
    INCOME = 1