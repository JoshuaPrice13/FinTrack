# Transaction Model - Developer Reference

## Quick Overview
`TransactionType.py` (enum), `Transaction.py` (main class)

## TransactionType Enum
```python
class TransactionType(Enum):
    SPENDING = 0
    INCOME = 1
```

## Transaction Class

### Constructor
```python
Transaction(transaction_type, price, date, category, description=None, categorized_by_ai=None)
```

**Required**: `transaction_type` (TransactionType), `price` (float), `date` (datetime.date), `category` (str)  
**Optional**: `description` (str), `categorized_by_ai` (bool)

### Key Attributes
- `transaction_type`, `price`, `date`, `category` - Core data
- `year`, `month`, `day` - Auto-extracted from date
- `description`, `categorized_by_ai` - Optional fields

### Properties
- `is_income` - Returns `transaction_type == TransactionType.INCOME`
- `is_spending` - Returns `transaction_type == TransactionType.SPENDING`

### Validation
- Price must be non-negative (raises ValueError)
- Category cannot be empty/whitespace (raises ValueError)
- Strings are auto-trimmed

### String Output
- `str()`: `"Income: $1500.00 - Salary (2024-09-15)"`
- `repr()`: `"Transaction(type=TransactionType.INCOME, price=1500.0, ...)"`

## Usage
```python
# Basic
t1 = Transaction(TransactionType.SPENDING, 25.99, date(2024, 9, 16), "Food")

# Full
t2 = Transaction(TransactionType.INCOME, 1500.0, date(2024, 9, 15), "Salary", 
                 description="Monthly salary", categorized_by_ai=False)

# Property usage
if t1.is_spending:  # No parentheses - it's a property
    print("Expense transaction")
```