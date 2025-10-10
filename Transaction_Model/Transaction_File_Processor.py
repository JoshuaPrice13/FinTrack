import csv
from datetime import datetime, date
from typing import List, Dict, Optional, Any
from pathlib import Path
from Transaction import Transaction


class Transaction_File_Processor:
    """
    A class to read transaction data from various CSV formats and prepare
    Transaction objects using intelligent column mapping.
    """

    def __init__(self, file_path: str):
        """
        Initialize the CSV reader with a file path.
        
        Args:
            file_path (str): Path to the CSV file
            
        Raises:
            FileNotFoundError: If the specified file doesn't exist
            ValueError: If the file is not a CSV file
        """
        self.file_path = Path(file_path)
        
        
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        if not self.file_path.suffix.lower() == '.csv':
            raise ValueError(f"File must be a CSV file, got: {self.file_path.suffix}")
        
        self.raw_data: List[Dict[str, Any]] = []
        self.column_mapping: Dict[str, str] = {}
        self.columns: List[str] = []
        self.ALL_TRANSACTIONS: List['Transaction'] = []
        
        # Define possible column name variations for mapping
        self.column_patterns = {
            'date': [
                # Date/Time variations (150+ from the synonym list)
                'day', 'date', 'transaction_date', 'trans_date', 'txn_date', 'posting_date', 
                'post_date', 'processed_date', 'process_date', 'settlement_date', 
                'settle_date', 'value_date', 'effective_date', 'entry_date', 'booking_date', 
                'cleared_date', 'completion_date', 'execution_date', 'activity_date', 
                'occurrence_date', 'event_date', 'action_date', 'timestamp', 'datetime', 
                'time_stamp', 'posted_on', 'processed_on', 'settled_on', 'cleared_on', 
                'completed_on', 'executed_on', 'occurred_on', 'happened_on', 'made_on', 
                'created_on', 'initiated_on', 'authorized_on', 'approved_on', 'confirmed_on', 
                'recorded_on', 'logged_on', 'registered_on', 'entered_on', 'booked_on', 
                'filed_on', 'submitted_on', 'requested_on', 'ordered_on', 'scheduled_on', 
                'performed_on', 'conducted_on', 'transacted_on', 'debited_on', 
                'charged_on', 'paid_on', 'received_on', 'sent_on', 'transferred_on', 
                'withdrawn_on', 'deposited_on', 'issued_on', 'generated_on', 'produced_on', 
                'published_on', 'released_on', 'delivered_on', 'dispatched_on', 'forwarded_on', 
                'transmitted_on', 'communicated_on', 'reported_on', 'notified_on', 'alerted_on', 
                'updated_on', 'modified_on', 'changed_on', 'edited_on', 'revised_on', 
                'amended_on', 'adjusted_on', 'corrected_on', 'fixed_on', 'repaired_on', 
                'restored_on', 'renewed_on', 'refreshed_on', 'synchronized_on', 'synced_on', 
                'backed_up_on', 'archived_on', 'stored_on', 'saved_on', 'preserved_on', 
                'maintained_on', 'kept_on', 'held_on', 'retained_on', 'secured_on', 
                'protected_on', 'validated_on', 'verified_on', 'authenticated_on', 
                'authorized_on', 'approved_on', 'accepted_on', 'rejected_on', 'declined_on', 
                'denied_on', 'refused_on', 'cancelled_on', 'voided_on', 'reversed_on', 
                'refunded_on', 'returned_on', 'recalled_on', 'retracted_on', 'undone_on', 
                'rolled_back_on', 'backed_out_on', 'aborted_on', 'terminated_on', 'ended_on', 
                'finished_on', 'closed_on', 'finalized_on', 'concluded_on', 'wrapped_up_on', 
                'sealed_on', 'signed_on', 'endorsed_on', 'ratified_on', 'sanctioned_on', 
                'permitted_on', 'allowed_on', 'enabled_on', 'activated_on', 'triggered_on', 
                'started_on', 'begun_on', 'commenced_on', 'launched_on', 'opened_on', 
                'create_date', 'creation_date', 'made_date', 'generated_date', 'issued_date', 
                'posted_date', 'entered_date', 'recorded_date', 'logged_date', 'filed_date', 
                'submitted_date', 'sent_date', 'received_date', 'processed_date', 'completed_date', 
                'finished_date', 'closed_date', 'transaction_timestamp', 'txn_timestamp', 
                'trans_timestamp', 'posting_timestamp', 'settlement_timestamp', 'clearing_timestamp', 
                'completion_timestamp', 'purchase_date', 'sale_date', 'order_date', 'invoice_date'
            ],

            'transaction_type': [
                'transaction_type', 'type', 'transaction type', 'trans_type', 'txn_type',
                'debit_credit', 'debit/credit', 'debit credit', 'dr_cr', 'dr/cr',
                'income_expense', 'income/expense', 'income expense', 'in_out',
                'credit_debit', 'credit/debit', 'direction', 'transaction_direction',
                'flow', 'money_flow', 'cash_flow', 'fund_flow', 'payment_type',
                'payment_direction', 'account_movement', 'movement_type', 'entry_type',
                'posting_type', 'ledger_type', 'journal_type', 'book_type'
            ],
        
            'price': [
                # Amount/Value variations (150+ from the synonym list)
                'Withdrawls','amount', 'amt', 'value', 'sum', 'total', 'price', 'cost', 
                'expense', 'charge', 'fee', 'payment', 'receipt', 'debit', 'credit', 
                'withdrawal', 'deposit', 'transfer', 'transaction_amount', 'trans_amount', 
                'txn_amount', 'transaction_value', 'trans_value', 'txn_value', 
                'dollar_amount', 'currency_amount', 'monetary_amount', 'financial_amount', 
                'cash_amount', 'money_amount', 'fund_amount', 'capital_amount', 
                'principal_amount', 'gross_amount', 'net_amount', 'base_amount', 
                'original_amount', 'initial_amount', 'final_amount', 'settled_amount', 
                'cleared_amount', 'posted_amount', 'processed_amount', 'authorized_amount', 
                'approved_amount', 'confirmed_amount', 'verified_amount', 'validated_amount', 
                'certified_amount', 'authenticated_amount', 'recorded_amount', 'logged_amount', 
                'registered_amount', 'entered_amount', 'booked_amount', 'filed_amount', 
                'submitted_amount', 'requested_amount', 'ordered_amount', 'charged_amount', 
                'billed_amount', 'invoiced_amount', 'quoted_amount', 'estimated_amount', 
                'calculated_amount', 'computed_amount', 'determined_amount', 'assessed_amount', 
                'evaluated_amount', 'appraised_amount', 'valued_amount', 'priced_amount', 
                'costed_amount', 'figured_amount', 'totaled_amount', 'summed_amount', 
                'aggregated_amount', 'accumulated_amount', 'collected_amount', 'gathered_amount', 
                'assembled_amount', 'compiled_amount', 'consolidated_amount', 'combined_amount', 
                'merged_amount', 'united_amount', 'joined_amount', 'linked_amount', 
                'connected_amount', 'associated_amount', 'related_amount', 'corresponding_amount', 
                'matching_amount', 'equivalent_amount', 'equal_amount', 'same_amount', 
                'identical_amount', 'similar_amount', 'comparable_amount', 'analogous_amount', 
                'parallel_amount', 'tied_amount', 'bound_amount', 'attached_amount', 
                'fixed_amount', 'set_amount', 'established_amount', 'decided_amount', 
                'resolved_amount', 'agreed_amount', 'negotiated_amount', 'bargained_amount', 
                'contracted_amount', 'committed_amount', 'promised_amount', 'pledged_amount', 
                'guaranteed_amount', 'assured_amount', 'secured_amount', 'protected_amount', 
                'insured_amount', 'covered_amount', 'included_amount', 'contained_amount', 
                'comprised_amount', 'encompassed_amount', 'embraced_amount', 'incorporated_amount', 
                'integrated_amount', 'embedded_amount', 'implanted_amount', 'inserted_amount', 
                'injected_amount', 'infused_amount', 'instilled_amount', 'introduced_amount', 
                'imported_amount', 'brought_amount', 'carried_amount', 'transported_amount', 
                'transferred_amount', 'moved_amount', 'shifted_amount', 'displaced_amount', 
                'relocated_amount', 'repositioned_amount', 'rearranged_amount', 'reorganized_amount', 
                'restructured_amount', 'reformed_amount', 'revised_amount', 'modified_amount', 
                'changed_amount', 'altered_amount', 'adjusted_amount', 'adapted_amount', 
                'amended_amount', 'updated_amount', 'upgraded_amount', 'improved_amount', 
                'enhanced_amount', 'optimized_amount', 'refined_amount', 'perfected_amount'
            ],
            
            'category': [
                'category', 'cat', 'type', 'classification', 'group', 'class', 'kind', 
                'sort', 'variety', 'style', 'genre', 'nature', 'species', 'family', 
                'division', 'section', 'department', 'unit', 'branch', 'segment', 
                'part', 'portion', 'piece', 'component', 'element', 'factor', 'aspect', 
                'feature', 'characteristic', 'attribute', 'property', 'quality', 'trait', 
                'transaction_category', 'transaction category', 'trans_category', 
                'txn_category', 'merchant_category', 'business_category', 'expense_category', 
                'income_category', 'payment_category', 'spending_category', 'purchase_category', 
                'transaction_class', 'trans_class', 'txn_class', 'expense_class', 
                'income_class', 'payment_class', 'spending_class', 'purchase_class', 
                'transaction_type_category', 'expense_type', 'income_type', 'payment_type', 
                'spending_type', 'purchase_type', 'merchant_type', 'business_type', 
                'vendor_type', 'payee_type', 'recipient_type', 'beneficiary_type', 
                'counterparty_type', 'transaction_group', 'expense_group', 'income_group', 
                'payment_group', 'spending_group', 'purchase_group', 'merchant_group', 
                'business_group', 'vendor_group', 'payee_group', 'recipient_group', 
                'beneficiary_group', 'counterparty_group', 'account_category', 'ledger_category', 
                'journal_category', 'book_category', 'financial_category', 'monetary_category', 
                'cash_category', 'fund_category', 'capital_category', 'asset_category', 
                'liability_category', 'equity_category', 'revenue_category', 'cost_category', 
                'budget_category', 'allocation_category', 'assignment_category', 'designation_category'
            ],
            
            'description': [
                # Description variations (150+ from the synonym list)
                'description', 'desc', 'details', 'memo', 'note', 'notes', 'reference', 
                'ref', 'comment', 'comments', 'remarks', 'narrative', 'summary', 
                'explanation', 'info', 'information', 'particulars', 'specifics', 
                'transaction_description', 'trans_description', 'txn_description', 
                'transaction_details', 'trans_details', 'txn_details', 'transaction_memo', 
                'trans_memo', 'txn_memo', 'transaction_note', 'trans_note', 'txn_note', 
                'transaction_reference', 'trans_reference', 'txn_reference', 'transaction_comment', 
                'trans_comment', 'txn_comment', 'merchant', 'merchant_name', 'vendor', 
                'vendor_name', 'payee', 'payee_name', 'payer', 'payer_name', 'recipient', 
                'recipient_name', 'beneficiary', 'beneficiary_name', 'counterparty', 
                'counterparty_name', 'business_name', 'company_name', 'organization', 
                'store_name', 'shop_name', 'retailer', 'supplier', 'provider', 
                'service_provider', 'institution', 'establishment', 'entity', 'party', 
                'third_party', 'other_party', 'transaction_party', 'trans_party', 'txn_party', 
                'purpose', 'reason', 'cause', 'basis', 'justification', 'rationale', 
                'motive', 'intent', 'objective', 'goal', 'target', 'subject', 'topic', 
                'theme', 'location', 'place', 'venue', 'site', 'address', 'city', 
                'state', 'country', 'region', 'area', 'zone', 'territory', 'district', 
                'locality', 'neighborhood', 'suburb', 'town', 'village', 'municipality', 
                'county', 'province', 'jurisdiction', 'domain', 'realm', 'sphere', 
                'field', 'sector', 'industry', 'market', 'segment', 'niche', 'specialty', 
                'focus', 'concentration', 'emphasis', 'highlight', 'feature', 'aspect', 
                'element', 'component', 'part', 'piece', 'item', 'product', 'service', 
                'offering', 'package', 'bundle', 'deal', 'offer', 'promotion', 'discount', 
                'sale', 'purchase', 'buy', 'acquisition', 'procurement', 'order', 
                'request', 'booking', 'reservation', 'appointment', 'schedule', 'arrangement', 
                'agreement', 'contract', 'treaty', 'pact', 'bargain', 'negotiation', 
                'settlement', 'resolution', 'solution', 'answer', 'response', 'reply', 
                'feedback', 'input', 'output', 'result', 'outcome', 'consequence', 
                'effect', 'impact', 'influence', 'change', 'modification', 'adjustment', 
                'correction', 'fix', 'repair', 'update', 'upgrade', 'improvement', 
                'enhancement', 'optimization', 'refinement', 'revision', 'amendment', 
                'alteration', 'variation', 'difference', 'deviation', 'exception', 
                'anomaly', 'irregularity', 'discrepancy', 'error', 'mistake', 'fault', 
                'flaw', 'defect', 'issue', 'problem', 'concern', 'matter', 'affair', 
                'business', 'case', 'instance', 'example', 'sample', 'specimen', 
                'model', 'template', 'pattern', 'format', 'structure', 'layout', 
                'design', 'plan', 'blueprint', 'scheme', 'system', 'method', 'approach', 
                'technique', 'procedure', 'process', 'workflow', 'protocol', 'standard', 
                'guideline', 'rule', 'regulation', 'policy', 'practice', 'custom', 
                'tradition', 'convention', 'norm', 'habit', 'routine', 'ritual', 
                'ceremony', 'event', 'occasion', 'happening', 'incident', 'occurrence', 
                'episode', 'experience', 'encounter', 'meeting', 'session', 'conference', 
                'discussion', 'conversation', 'dialogue', 'exchange', 'interaction', 
                'communication', 'correspondence', 'message', 'transmission', 'broadcast', 
                'announcement', 'notification', 'alert', 'warning', 'reminder', 'notice', 
                'bulletin', 'report', 'statement', 'declaration', 'proclamation', 
                'publication', 'release', 'disclosure', 'revelation', 'exposure', 
                'presentation', 'demonstration', 'exhibition', 'display', 'show', 
                'performance', 'act', 'action', 'activity', 'operation', 'function'
            ],
            
            'account': [
                # Account variations (150+ from the synonym list)
                'account', 'account_number', 'account_num', 'acct', 'acct_number', 
                'acct_num', 'account_id', 'acct_id', 'account_identifier', 'account_code', 
                'account_reference', 'account_ref', 'account_name', 'acct_name', 
                'account_title', 'acct_title', 'account_description', 'acct_description', 
                'account_type', 'acct_type', 'account_category', 'acct_category', 
                'account_classification', 'acct_classification', 'account_group', 'acct_group', 
                'account_class', 'acct_class', 'account_kind', 'acct_kind', 'account_sort', 
                'acct_sort', 'account_style', 'acct_style', 'account_variety', 'acct_variety', 
                'account_branch', 'acct_branch', 'account_office', 'acct_office', 
                'account_location', 'acct_location', 'account_address', 'acct_address', 
                'account_region', 'acct_region', 'account_area', 'acct_area', 'account_zone', 
                'acct_zone', 'account_territory', 'acct_territory', 'account_district', 
                'acct_district', 'account_division', 'acct_division', 'account_department', 
                'acct_department', 'account_unit', 'acct_unit', 'account_section', 'acct_section', 
                'account_segment', 'acct_segment', 'account_part', 'acct_part', 'account_portion', 
                'acct_portion', 'account_piece', 'acct_piece', 'account_component', 'acct_component', 
                'account_element', 'acct_element', 'account_factor', 'acct_factor', 
                'account_aspect', 'acct_aspect', 'account_feature', 'acct_feature', 
                'account_characteristic', 'acct_characteristic', 'account_attribute', 'acct_attribute', 
                'account_property', 'acct_property', 'account_quality', 'acct_quality', 
                'account_trait', 'acct_trait', 'account_nature', 'acct_nature', 'account_essence', 
                'acct_essence', 'from_account', 'to_account', 'source_account', 'destination_account', 
                'debit_account', 'credit_account', 'primary_account', 'secondary_account', 
                'main_account', 'sub_account', 'parent_account', 'child_account', 'master_account', 
                'detail_account', 'summary_account', 'control_account', 'subsidiary_account', 
                'related_account', 'linked_account', 'associated_account', 'connected_account', 
                'paired_account', 'matched_account', 'corresponding_account', 'equivalent_account', 
                'similar_account', 'comparable_account', 'parallel_account', 'mirrored_account', 
                'twin_account', 'duplicate_account', 'copy_account', 'replica_account', 
                'clone_account', 'backup_account', 'reserve_account', 'alternate_account', 
                'alternative_account', 'substitute_account', 'replacement_account', 'spare_account', 
                'extra_account', 'additional_account', 'supplementary_account', 'auxiliary_account', 
                'supporting_account', 'helping_account', 'assisting_account', 'aiding_account', 
                'contributing_account', 'participating_account', 'involved_account', 'engaged_account', 
                'active_account', 'working_account', 'operating_account', 'functioning_account', 
                'running_account', 'current_account', 'present_account', 'existing_account', 
                'available_account', 'accessible_account', 'open_account', 'live_account', 
                'valid_account', 'legitimate_account', 'authorized_account', 'approved_account', 
                'confirmed_account', 'verified_account', 'authenticated_account', 'certified_account', 
                'qualified_account', 'licensed_account', 'registered_account', 'recognized_account', 
                'acknowledged_account', 'accepted_account', 'admitted_account', 'included_account', 
                'incorporated_account', 'integrated_account', 'embedded_account', 'built_in_account', 
                'installed_account', 'established_account', 'created_account', 'formed_account', 
                'developed_account', 'constructed_account', 'built_account', 'made_account', 
                'produced_account', 'generated_account', 'manufactured_account', 'fabricated_account'
            ]
        }
        
        # Read and analyze the CSV file
        self._read_csv_file()
        self._map_columns()
        self.ALL_TRANSACTIONS = self.create_transactions()
    
    def _read_csv_file(self) -> None:
        """Read the CSV file and store raw data."""
        try:
            with open(self.file_path, 'r', newline='', encoding='utf-8') as file:
                # Use csv.Sniffer to detect dialect
                sample = file.read(1024)
                file.seek(0)
                
                try:
                    dialect = csv.Sniffer().sniff(sample)
                except csv.Error:
                    dialect = csv.excel  # fallback to default
                
                reader = csv.DictReader(file, dialect=dialect)
                self.columns = reader.fieldnames or []
                
                for row in reader:
                    # Clean up the row data (strip whitespace from keys and values)
                    cleaned_row = {}
                    for key, value in row.items():
                        if key is not None:
                            clean_key = key.strip()
                            clean_value = value.strip() if value else None
                            cleaned_row[clean_key] = clean_value
                    self.raw_data.append(cleaned_row)
                    
        except UnicodeDecodeError:
            # Try with different encoding if UTF-8 fails
            with open(self.file_path, 'r', newline='', encoding='latin-1') as file:
                reader = csv.DictReader(file)
                self.columns = reader.fieldnames or []
                
                for row in reader:
                    cleaned_row = {}
                    for key, value in row.items():
                        if key is not None:
                            clean_key = key.strip()
                            clean_value = value.strip() if value else None
                            cleaned_row[clean_key] = clean_value
                    self.raw_data.append(cleaned_row)
    
    def _map_columns(self) -> None:
    
        self.column_mapping = {}

        # Convert column names to lowercase for matching
        lower_columns = [col.lower() for col in self.columns]

        # Loop through each CSV column and try to match it to a field
        for i, csv_column in enumerate(self.columns):
            csv_column_lower = csv_column.lower()
            matched = False
            
            # Try to match this CSV column to one of our expected fields
            for field, patterns in self.column_patterns.items():
                if matched:
                    break
                    
                for pattern in patterns:
                    pattern_lower = pattern.lower()
                    
                    # Exact match first
                    if csv_column_lower == pattern_lower:
                        self.column_mapping[field] = csv_column
                        matched = True
                        break
                    
                    # Partial match (contains pattern)
                    """
                    elif pattern_lower in csv_column_lower or csv_column_lower in pattern_lower:
                        self.column_mapping[field] = csv_column
                        print(csv_column_lower, " = ", pattern_lower, " from ", csv_column)
                        matched = True
                        break
                    """

                        
    
    def get_columns(self) -> List[str]:
        """Return the list of columns found in the CSV file."""
        return self.columns.copy()
    
    def get_column_mapping(self) -> Dict[str, str]:
        """Return the mapping between expected fields and CSV columns."""
        return self.column_mapping.copy()
    
    def get_raw_data(self) -> List[Dict[str, Any]]:
        """Return the raw CSV data as a list of dictionaries."""
        return self.raw_data.copy()
    
    def get_all_transactions(self) -> List[Transaction]:
        return self.ALL_TRANSACTIONS
    
    def _parse_transaction_type(self, value: str) -> 'TransactionType':
        """
        Parse transaction type from various string formats.
        
        Args:
            value (str): The transaction type value from CSV
            
        Returns:
            TransactionType: The parsed transaction type
            
        Raises:
            ValueError: If transaction type cannot be determined
        """
        if not value:
            raise ValueError("Transaction type cannot be empty")
        
        value_lower = value.lower().strip()
        
        # Income indicators
        income_indicators = ['income', 'credit', 'deposit', 'in', 'positive', '+', '1']
        # Spending indicators  
        spending_indicators = ['spending', 'expense', 'debit', 'withdrawal', 'out', 'negative', '-', '0']
        
        if value_lower in income_indicators or any(indicator in value_lower for indicator in income_indicators):
            from enum import Enum
            # Import TransactionType from the provided code
            return TransactionType.INCOME
        elif value_lower in spending_indicators or any(indicator in value_lower for indicator in spending_indicators):
            return TransactionType.SPENDING
        else:
            raise ValueError(f"Cannot determine transaction type from value: {value}")
    
    def _parse_price(self, value: str) -> float:
        """
        Parse price from string, handling various formats.
        
        Args:
            value (str): The price value from CSV
            
        Returns:
            float: The parsed price as a positive number
            
        Raises:
            ValueError: If price cannot be parsed or is negative
        """
        if not value:
            raise ValueError("Price cannot be empty")
        
        # Remove common currency symbols and whitespace
        cleaned_value = value.replace('$', '').replace('€', '').replace('£', '').replace(',', '').strip()
        
        # Handle negative signs and parentheses (accounting format)
        is_negative = False
        if cleaned_value.startswith('(') and cleaned_value.endswith(')'):
            cleaned_value = cleaned_value[1:-1]
            is_negative = True
        elif cleaned_value.startswith('-'):
            cleaned_value = cleaned_value[1:]
            is_negative = True
        
        try:
            price = float(cleaned_value)
            # Convert to positive (Transaction class expects positive values)
            return abs(price)
        except ValueError:
            raise ValueError(f"Cannot parse price from value: {value}")
    
    def _parse_date(self, value: str) -> date:
        
        """
        Parse date from string, handling various formats.
        
        Args:
            value (str): The date value from CSV
            
        Returns:
            date: The parsed date
            
        Raises:
            ValueError: If date cannot be parsed
        """
        if not value:
            raise ValueError("Date cannot be empty")
        
        # Common date formats to try
        date_formats = [
        '%Y-%m-%d',      # 2024-09-15
        '%m/%d/%Y',      # 09/15/2024
        '%d/%m/%Y',      # 15/09/2024
        '%m-%d-%Y',      # 09-15-2024
        '%d-%m-%Y',      # 15-09-2024
        '%d-%b-%Y',      # 15-Aug-2024 (capitalized)
        '%d-%B-%Y',      # 15-August-2024 (capitalized full month)
        '%d-%b-%Y',      # base for lowercase/uppercase handling
        '%d-%b-%Y',      # 15-Aug-2024
        '%Y/%m/%d',      # 2024/09/15
        '%m/%d/%y',      # 09/15/24
        '%d/%m/%y',      # 15/09/24
        '%Y-%m-%d %H:%M:%S',  # With timestamp
        '%m/%d/%Y %H:%M:%S',  # With timestamp
    ]
        
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(value.strip(), date_format).date()
                return parsed_date
            except ValueError:
                continue
        
        raise ValueError(f"Cannot parse date from value: {value}")
    
    def prepare_transaction_data(self) -> List[Dict[str, Any]]:
        """
        Prepare transaction data ready for Transaction constructor calls.
        
        Returns:
            List[Dict[str, Any]]: List of dictionaries with parsed transaction data
            
        Raises:
            ValueError: If required fields are missing or cannot be parsed
        """
        prepared_data = []
        
        # Check if we have the minimum required mappings
        required_fields = ['date', 'price']
        missing_fields = [field for field in required_fields if field not in self.column_mapping]
        
        if missing_fields:
            raise ValueError(f"Cannot find columns for required fields: {missing_fields}")
        
        for row_index, row in enumerate(self.raw_data):
            try:
                # Extract required fields
                my_price_raw = row.get(self.column_mapping['price'])
                my_date_raw = row.get(self.column_mapping['date'])
                
                # Parse required fields
                my_price = self._parse_price(my_price_raw)
                my_transaction_date = self._parse_date(my_date_raw)
                
                # Extract optional fields
                my_description = None
                if 'description' in self.column_mapping:
                    my_description_raw = row.get(self.column_mapping['description'])
                    my_description = my_description_raw.strip() if my_description_raw else None

                my_transaction_type = None
                if 'transaction_type' in self.column_mapping:
                    my_transaction_type_raw = row.get(self.column_mapping['transaction_type'])
                    my_transaction_type = self._parse_transaction_type(my_transaction_type_raw) if my_transaction_type_raw else None
                #if 'transaction_type = self._parse_transaction_type(transaction_type_raw)'

                #category = 'Uncategorized'
                my_category = 'uncategorized'
                if 'category' in self.column_mapping:
                    my_category_raw = row.get(self.column_mapping['category'])
                    if (my_category_raw):
                        my_category = my_category_raw.strip()
                    else:
                        my_category = 'uncategorized'
                
                # Prepare the data dictionary for Transaction constructor
                transaction_data = {
                    'transaction_type': my_transaction_type,
                    'price': my_price,
                    'date': my_transaction_date,
                    'category': my_category,
                    'description': my_description,
                    'categorized_by_ai': None  # Default to None as per Transaction class
                }
                
                prepared_data.append(transaction_data)
                
            except (ValueError, KeyError) as e:
                raise ValueError(f"Error processing row {row_index + 1}: {str(e)}")
        
        return prepared_data
    
    def create_transactions(self) -> List['Transaction']:
        """
        Create Transaction objects from the CSV data.
        
        Returns:
            List[Transaction]: List of Transaction objects
            
        Note:
            This method assumes the Transaction class is imported and available.
            You need to import Transaction and TransactionType classes before calling this.
        """
        prepared_data = self.prepare_transaction_data()
        transactions = []
        
        
        for data in prepared_data:
            transaction = Transaction(
                transaction_type=data['transaction_type'],
                price=data['price'],
                date=data['date'],
                category=data['category'],
                description=data['description'],
                categorized_by_ai=data['categorized_by_ai']
            )
            transactions.append(transaction)
            #print(transaction)
        return transactions
   