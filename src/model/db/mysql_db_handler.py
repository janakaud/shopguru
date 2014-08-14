'''
Created on Aug 13, 2014

@author: janaka
'''
from config import db_config
import MySQLdb
import logging

conn = None


def get_connection():
    global conn
    if conn is None:
        conn = MySQLdb.connect(db=db_config.DB_NAME,
                               user=db_config.DB_USER,
                               passwd=db_config.DB_PASSWORD)
    return conn


def run_update(query, param_list):
    # do actual transaction
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, param_list)
    conn.commit()
    cursor.close()
    logging.info('Query execution successful')