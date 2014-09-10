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
                      filter_fields, filter_values,
                      order_fields=None, order_values=None,
                      search_with_like=False):
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
        
        # construct filter field-value list (based on search type)
        if search_with_like:
            # construct list using LIKE
            query += ' WHERE '
            query += ' LIKE %s AND '.join(filter_fields)
            query += ' LIKE %s'
        else:
            # construct list using =
            query += ' WHERE ('
            query += ', '.join(filter_fields)
            query += ') = (%s'
            query += ', %s'*(len(filter_fields) - 1)
            query += ')'
        
        # add ORDER BY part if fields provided
        if order_fields != None:
            # ensure non-emptiness of field list
            if len(order_fields) < 1:
                raise MySQLError('Invalid order by field list')
            
            # ensure non-emptiness of order by values list (if any)
            if order_values != None and len(order_values) < 1:
                raise MySQLError('Invalid order by value list')
            
            query += ' ORDER BY ('
            query += ', '.join(order_fields)
            query += ')'
        
        # create full parameter list
        if order_fields != None and order_values != None:
            params = filter_values + order_values
        else:
            params = filter_values
        
        logging.info(query + ' with ' + str(params))
        
        output = []
        # do actual transaction
        try:
            result = mysql_db_handler.run_query(query, params)
            if result.rowcount > 0:
                # create list object with retrieved records 
                output = result.fetchall()
        except MySQLError as e:
            logging.error(e)
            
        return output

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
        query += ' WHERE ('
        query += ', '.join(filter_fields)
        query += ') = (%s'
        query += ', %s'*(len(filter_values) - 1)
        query += ')'
        
        # complete parameter list
        params = values + filter_values
        
        logging.info(query + ' with ' + str(params))
        
        # do actual transaction
        try:
            mysql_db_handler.run_update(query, params)
        except MySQLError as e:
            logging.error(e)

    def delete_record(self, table,
                      filter_fields, filter_values):
        # ensure all filter fields have values
        filter_field_len = len(filter_fields)
        filter_values_len = len(filter_values)
        
        if filter_field_len < 1 or filter_field_len != filter_values_len:
            raise MySQLError('Invalid field-value mapping in filter')

        # construct update field-value list
        query = 'DELETE FROM ' + table
        
        # construct filter field-value list
        query += ' WHERE ('
        query += ', '.join(filter_fields)
        query += ') = (%s'
        query += ', %s'*(len(filter_values) - 1)
        query += ')'
        
        logging.info(query + ' with ' + str(filter_values))
        
        # do actual transaction
        try:
            mysql_db_handler.run_update(query, filter_values)
        except MySQLError as e:
            logging.error(e)
