from typing import List
import unittest
from Transaction_File_Processor import Transaction_File_Processor
from Transaction import Transaction

if __name__ == '__main__':
    # first test
    csv_file_path_1 = 'Test_Data\\CSV_Test_1.csv' 
    csv_file_path_2 = 'Test_Data\\CSV_Test_2.csv'
    csv_file_path_3 = 'Test_Data\\CSV_Test_3.csv'


    print("-" * 75)
    print("\t---First Test---")
    print("Filepath: ", csv_file_path_1)
    print("-" * 75)

    tmp = Transaction_File_Processor(csv_file_path_1)
    print(tmp.get_column_mapping())
    print("-" * 20)

    trans: List[Transaction]
    trans = tmp.get_all_transactions()
    for tran in trans:
        print(repr(tran))

    print("-" * 75)
    print("\t---Second Test---")
    print("Filepath: ", csv_file_path_2)
    print("-" * 75)

    tmp = Transaction_File_Processor(csv_file_path_2)
    print(tmp.get_column_mapping())
    print("-" * 20)

    trans: List[Transaction]
    trans = tmp.get_all_transactions()
    for tran in trans:
        print(repr(tran))

    print("-" * 75)
    print("\t---Third Test---")
    print("Filepath: ", csv_file_path_3)
    print("-" * 75)

    tmp = Transaction_File_Processor(csv_file_path_3)
    print(tmp.get_column_mapping())
    print("-" * 20)

    trans: List[Transaction]
    trans = tmp.get_all_transactions()
    for tran in trans:
        print(repr(tran))


"""
    #hr test
    csv_file_path = 'Test_Data\\100 BT Records.csv' 
    tmp = Transaction_File_Processor(csv_file_path)
    print(tmp.get_columns())
    print(tmp.get_column_mapping())

    trans: List[Transaction]
    trans = tmp.get_all_transactions()
"""
