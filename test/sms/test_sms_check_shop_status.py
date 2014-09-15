'''
@author: janaka

Test collection for shop status check message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class CheckShopStatusSMSTest(unittest.TestCase):

    def test_shop_status_check_sms(self):
        """ test shop status check query with name """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'status Bank of Ceylon, Katubedda')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.SHOP_STATUS)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['shop'], 'Bank of Ceylon, Katubedda')

    def test_no_name_shop_status_check_sms(self):
        """ make sure shop status check query without name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'status')
        self.assertRaises(QueryNameTooShortException, message_parser.parse,
                          message)

    def test_short_name_shop_status_check_sms(self):
        """ make sure a query with shop name shorter than MIN_NAME_QUERY chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'status %s' % ('a'*(MIN_NAME_QUERY-1)))
        self.assertRaises(QueryNameTooShortException, message_parser.parse, 
                          message)

    def test_long_name_shop_status_check_sms(self):
        """ make sure a query with shop name longer than MAX_NAME_QUERY chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'status %s' % ('a'*(MAX_NAME_QUERY+1)))
        self.assertRaises(QueryNameTooLongException, message_parser.parse, 
                          message)


if __name__ == '__main__':
    unittest.main()