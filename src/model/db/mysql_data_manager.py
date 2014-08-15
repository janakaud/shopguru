'''
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
        # singleton pattern
        if cls.instance is None:
            cls.instance = MySQLDataManager()
        return cls.instance
    
    def search_record(self, table, select_fields,
                      filter_fields, filter_values):
        # ensure all filter fields have values
        filter_field_len = len(filter_fields)
        filter_values_len = len(filter_values)
        
        if filter_field_len < 1 or filter_field_len != filter_values_len:
            raise MySQLError('Invalid field-value mapping in filter')
        
        if len(select_fields) < 1:
            raise MySQLError('Invalid select field list')

        # construct update field-value list
        query = 'SELECT '
        query += ', '.join(select_fields)
        query += ' FROM ' + table 
        
        # construct filter field-value list
        query += ' WHERE ('
        query += ', '.join(filter_fields)
        query += ') = (%s'
        query += ', %s'*(len(filter_fields) - 1)
        query += ')'
        
        logging.info(query + ' with ' + str(filter_values))
        
        result = None
        # do actual transaction
        try:
            result = mysql_db_handler.run_query(query, filter_values)
        except MySQLError as e:
            logging.error(e)
            
        return result

    def insert_record(self, table, fields, values):
        # ensure all fields have values
        field_len = len(fields)
        values_len = len(values)
        
        if field_len < 1 or field_len != values_len:
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

    def update_record(self, table,
                      filter_fields, filter_values,
                      fields, values):
        # ensure all filter fields have values
        filter_field_len = len(filter_fields)
        filter_values_len = len(filter_values)
        
        if filter_field_len < 1 or filter_field_len != filter_values_len:
            raise MySQLError('Invalid field-value mapping in filter')

        # ensure all fields have values
        field_len = len(fields)
        values_len = len(values)
        
        if field_len < 1 or field_len != values_len:
            raise MySQLError('Invalid field-value mapping')

        # construct update field-value list
        query = 'UPDATE ' + table + ' SET '
        query += ' = %s, '.join(fields)
        query += ' = %s' 
        
        # construct filter field-value list
        query += ' WHERE '
        query += ' = %s AND '.join(filter_fields)
        query += ' = %s'
        
        logging.info(query + ' with ' + str(values))
        
        # do actual transaction
        try:
            mysql_db_handler.run_update(query, values)
        except MySQLError as e:
            logging.error(e)
