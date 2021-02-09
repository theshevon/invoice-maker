'''
:name: AdHocDB.py
:author: Shevon Mendis <shevonmendis@gmail.com>
:purpose: To create an ad hoc database out of information in a Google Sheet. 
'''

import gspread
import logging

from common.op_constants import CREDENTIALS_FILE_PATH

class AdHocDB:
    '''
        Represents an ad hoc database created out of records from a Google Sheet.
    '''

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def build(self, gs_id, table_info):
        '''
            Reads data from a google sheet and creates an adhoc database out of it.

            Arguments:
                gs_id        (String): The ID of the Google Sheet from which the DB info will be sourced.
                table_info     (List): A list of 2 tuples, where each tuple contains, in order:
                                                    [0]- The name of a worksheet (which will be the name of the table)
                                                    [1]- The primary key fields for a record in that worksheet
        '''

        self.logger.info(f"Attempting to read info from Google Sheet with ID: { gs_id }")

        tables = {}
        try:
            gc = gspread.service_account(CREDENTIALS_FILE_PATH)
            spreadsheet = gc.open_by_key(gs_id)
            for table_name, primary_keys in table_info:
                records = spreadsheet.worksheet(table_name).get_all_records()
                tables[table_name] = self.__create_adhoc_table(records, primary_keys)
            self.logger.info("Succesfully read records.")
        except:
            self.logger.error("Could not read records!", exc_info=True)

        self.tables = tables

    def __create_adhoc_table(self, records, primary_keys):

        table = {}
        for record in records:    
            key = tuple()
            for primary_key in primary_keys:
                key += (record[primary_key], )
            table[key] = record

        return table

    def getTable(self, table_name):
        ''' 
            Fetches a table from the database.

            Arguments:
                table_name (String): The name of the table that should be retrieved

            Return:
                Dictionary: A dictionary representing a table from the database. The structure is as follows:
                                [key]- Tuple representing primary key value for a record
                                [value]- A record from the table
        '''

        return self.tables[table_name]
        
    def queryTable(self, table_name, key, field):
        '''
            Fetches a record from a table in the database.

            Arguments:
                table_name (String): The name of the table that should be queried
                key         (Tuple): The value of the primary key for the required record

            Return:
                Dictionary: The required record
        '''

        return self.tables[table_name][key][field] if field else self.tables[table_name][key]

    def validateTable(self):
        pass