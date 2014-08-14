'''
@author: janaka
'''
from config import db_config
import MySQLdb
import logging

conn = None

def get_connection():
    """ singleton implementation of database connection """
    global conn
    if conn is None:
        conn = MySQLdb.connect(db=db_config.DB_NAME,
                               user=db_config.DB_USER,
                               passwd=db_config.DB_PASSWORD)
    return conn


def run_update(query, param_list):
    """ runs database update queries """
    # do actual transaction
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, param_list)
    conn.commit()
    cursor.close()
    logging.info('Query execution successful')


def run_query(query, param_list):
    """ runs database search queries """
    # do actual transaction
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, param_list)
    conn.commit()
    logging.info('Query execution successful')
    return cursor