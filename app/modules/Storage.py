'''
:name: AdHocDB.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To create an ad hoc database out of information in a Google Sheet. 
'''

import sys
import gspread
import logging

from common.defaults import CREDENTIALS_FILE_PATH
from modules.util import log

class AdHocDB:

    def __init__(self):
        
        self.logger = logging.getLogger(__name__)
        self.tables = {}

    def build(self, gs_id, table_info):
        '''
            Reads data from a google sheet and creates an adhoc database out of it.

            Arguments:
                gs_id        (string): The ID of the Google Sheet from which the DB info will be sourced.
                table_info     (List): A list of 2 tuples, where each tuple contains, in order:
                                            [0]- The name of a worksheet (which will be the name of the table)
                                            [1]- The primary key fields for a record in that worksheet as a tuple
        '''

        log(f"Attempting to read records from Google Sheet with ID: { gs_id }")

        try:
            gc = gspread.service_account(CREDENTIALS_FILE_PATH)
            spreadsheet = gc.open_by_key(gs_id)
            for table_name, primary_keys in table_info:
                records = spreadsheet.worksheet(table_name).get_all_records()
                self.__add_adhoc_table(table_name, records, primary_keys)
            log("Successfully read records from Google Sheet.")
        except:
            self.logger.error("Could not read records from Google Sheet!", exc_info=True)
            sys.exit()

    def __add_adhoc_table(self, table_name, records, primary_keys):
        '''
            Creates a table in the ad hoc DB.

            Arguments:
                table_name  (string): The name of the table
                records       (List): A list of dictionaries, each representing a record from a sheet
                primary_keys (Tuple): The primary keys for the table being built
        '''

        table = {}
        for record in records:    
            key = tuple()
            for primary_key in primary_keys:
                key += (record[primary_key], )
            table[key] = record

        self.tables[table_name] = table

    def getTable(self, table_name):
        ''' 
            Fetches a table from the database.

            Arguments:
                table_name (string): The name of the table that should be retrieved

            Return:
                Dictionary: A dictionary representing a table from the database. 
                            The structure is as follows:
                                                        [key]  - Tuple representing primary key value for a record
                                                        [value]- The complete record
        '''

        return self.tables[table_name]
        
    def getTableRecord(self, table_name, key):
        '''
            Fetches a record from a table in the database.

            Arguments:
                table_name (string): The name of the table that should be queried
                key         (Tuple): The value of the primary key for the required record

            Return:
                Dictionary: A dictionary representing a record from a table in the database
        '''

        return self.tables[table_name][key]

    def getTableRecordValue(self, table_name, key, field):
        '''
            Fetches a record from a table in the database.

            Arguments:
                table_name (string): The name of the table that should be queried
                key         (Tuple): The value of the primary key for the required record
                field      (string): The field for which the value is required

            Return:
                Dictionary: A dictionary representing a record from a table in the database
        '''

        return self.getTableRecord(table_name, key)[field]