'''
Created on Aug 13, 2014

@author: janaka
'''

from base_data_manager import BaseDataManager
import logging
from MySQLdb import Error as MySQLError
import mysql_db_handler


class MySQLDataManager(BaseDataManager):
    '''
    This class is a MySQL-compliant implementation of a data manager.
    '''
    instance = None

    @classmethod
    def get_instance(cls):
        if cls.instance is None:
            cls.instance = MySQLDataManager()
        return cls.instance
    
    def insert_record(self, table, fields, values):
        if len(fields) < 1 or len(values) < 1:
            raise MySQLError('Invalid field-value mapping')

        # construct query and parameter list
        query = 'INSERT INTO ' + table + ' ('
        query += ', '.join(fields) 
        query += ') VALUES (%s'
        query += ', %s'*(len(fields) - 1)
        query += ')' 
        
        logging.info(query + ' with ' + str(values))
        
        # do actual transaction
        try:
            mysql_db_handler.run_update(query, values)
        except MySQLError as e:
            logging.error(e)

    def update_record(self, table, fields, values):
        pass