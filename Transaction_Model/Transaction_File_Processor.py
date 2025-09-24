from enum import Enum
from typing import Optional

class File_Type(Enum):
    TRANSACTION_HISTORY = 0
    BANK_STATEMENT = 1


class TransactionFileProcessor:

    def __init__(self, 
                 file_type: File_Type, 
                 #Optional Parameters for Transaction_History type files
                 csv_bool: Optional[bool] =None,
                 headers_bool: Optional[bool] =None,
                 num_of_colums: Optional[int] =None,
                 
                 
                 ):
        return 0
    