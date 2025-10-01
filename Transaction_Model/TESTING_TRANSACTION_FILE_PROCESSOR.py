import unittest
from Transaction_File_Processor import Transaction_File_Processor
from Transaction import Transaction, TransactionType


class TestTransactionFileProcessorWithExternalCSV(unittest.TestCase):
    """Test suite for Transaction_File_Processor using an external CSV file."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        # Path to your external CSV file
        self.csv_file_path = 'Test_Data\BT_Records.csv'  # Change this to your CSV file path
    
    def test_load_external_csv(self):
        """Test loading and processing an external CSV file."""
        # Initialize the processor with the external CSV
        processor = Transaction_File_Processor(self.csv_file_path)
        
        # Print discovered columns
        print("\n=== Discovered Columns ===")
        columns = processor.get_columns()
        for i, col in enumerate(columns):
            print(f"{i}: {col}")
        
        # Print column mappings
        print("\n=== Column Mappings ===")
        mapping = processor.get_column_mapping()
        for field, column in mapping.items():
            print(f"{field} -> {column}")
        
        # Print raw data (first 5 rows)
        print("\n=== Raw Data (First 5 Rows) ===")
        raw_data = processor.get_raw_data()
        for i, row in enumerate(raw_data[:5]):
            print(f"Row {i}: {row}")
        
        # Test assertions
        self.assertIsNotNone(processor)
        self.assertGreater(len(columns), 0, "Should have at least one column")
        self.assertGreater(len(raw_data), 0, "Should have at least one row of data")
    
    def test_column_mapping_completeness(self):
        """Test that all required fields are mapped."""
        processor = Transaction_File_Processor(self.csv_file_path)
        mapping = processor.get_column_mapping()
        
        required_fields = ['transaction_type', 'price', 'date', 'category']
        
        print("\n=== Checking Required Field Mappings ===")
        for field in required_fields:
            if field in mapping:
                print(f"✓ {field} mapped to: {mapping[field]}")
            else:
                print(f"✗ {field} NOT MAPPED")
        
        # Assert all required fields are mapped
        for field in required_fields:
            self.assertIn(field, mapping, f"Required field '{field}' not mapped")
    
    def test_prepare_transaction_data(self):
        """Test preparing transaction data from the external CSV."""
        processor = Transaction_File_Processor(self.csv_file_path)
        
        try:
            prepared_data = processor.prepare_transaction_data()
            
            print(f"\n=== Prepared Transaction Data ===")
            print(f"Total transactions: {len(prepared_data)}")
            
            # Print first 3 transactions
            print("\n=== First 3 Prepared Transactions ===")
            for i, data in enumerate(prepared_data[:3]):
                print(f"\nTransaction {i}:")
                print(f"  Type: {data['transaction_type']}")
                print(f"  Price: ${data['price']:.2f}")
                print(f"  Date: {data['date']}")
                print(f"  Category: {data['category']}")
                print(f"  Description: {data['description']}")
            
            # Assertions
            self.assertGreater(len(prepared_data), 0, "Should have prepared at least one transaction")
            
            # Check structure of first prepared transaction
            if len(prepared_data) > 0:
                first = prepared_data[0]
                self.assertIn('transaction_type', first)
                self.assertIn('price', first)
                self.assertIn('date', first)
                self.assertIn('category', first)
                self.assertIn('description', first)
                self.assertIn('categorized_by_ai', first)
                
        except ValueError as e:
            self.fail(f"Failed to prepare transaction data: {str(e)}")
    
    def test_create_transactions(self):
        """Test creating Transaction objects from the external CSV."""
        processor = Transaction_File_Processor(self.csv_file_path)
        
        try:
            transactions = processor.create_transactions()
            
            print(f"\n=== Created Transactions ===")
            print(f"Total transactions created: {len(transactions)}")
            
            # Print first 3 transactions
            print("\n=== First 3 Transaction Objects ===")
            for i, txn in enumerate(transactions[:3]):
                print(f"\nTransaction {i}:")
                print(f"  Type: {txn.transaction_type}")
                print(f"  Price: ${txn.price:.2f}")
                print(f"  Date: {txn.date}")
                print(f"  Category: {txn.category}")
                print(f"  Description: {txn.description}")
            
            # Assertions
            self.assertGreater(len(transactions), 0, "Should have created at least one transaction")
            
            # Verify all are Transaction objects
            for txn in transactions:
                self.assertIsInstance(txn, Transaction)
                self.assertIsInstance(txn.transaction_type, TransactionType)
                self.assertIsInstance(txn.price, (int, float))
                self.assertGreater(txn.price, 0, "Price should be positive")
                
        except ValueError as e:
            self.fail(f"Failed to create transactions: {str(e)}")
    
    def test_transaction_statistics(self):
        """Test and display statistics about the transactions."""
        processor = Transaction_File_Processor(self.csv_file_path)
        
        try:
            transactions = processor.create_transactions()
            
            # Calculate statistics
            income_count = sum(1 for t in transactions if t.transaction_type == TransactionType.INCOME)
            spending_count = sum(1 for t in transactions if t.transaction_type == TransactionType.SPENDING)
            
            total_income = sum(t.price for t in transactions if t.transaction_type == TransactionType.INCOME)
            total_spending = sum(t.price for t in transactions if t.transaction_type == TransactionType.SPENDING)
            
            categories = set(t.category for t in transactions)
            
            # Print statistics
            print("\n=== Transaction Statistics ===")
            print(f"Total Transactions: {len(transactions)}")
            print(f"Income Transactions: {income_count}")
            print(f"Spending Transactions: {spending_count}")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Spending: ${total_spending:.2f}")
            print(f"Net: ${total_income - total_spending:.2f}")
            print(f"Unique Categories: {len(categories)}")
            print(f"Categories: {', '.join(sorted(categories))}")
            
            # Basic assertions
            self.assertEqual(len(transactions), income_count + spending_count)
            
        except ValueError as e:
            self.fail(f"Failed to analyze transactions: {str(e)}")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)