'''
@author: janaka

Test collection for shop status update message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class UpdateShopStatusSMSTest(unittest.TestCase):

    def test_shop_status_update_sms(self):
        """ test shop status update query """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'update open from 7 am to 8 am')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.UPDATE_STATUS)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['status'], 'open from 7 am to 8 am')

    def test_no_name_shop_status_update_sms(self):
        """ make sure shop status update query without name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'update')
        self.assertRaises(StatusTooShortException, message_parser.parse,
                          message)

    def test_short_name_shop_status_update_sms(self):
        """ make sure a query with status shorter than MIN_STATUS chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'update %s' % ('a'*(MIN_STATUS-1)))
        self.assertRaises(StatusTooShortException, message_parser.parse, 
                          message)

    def test_long_name_shop_status_update_sms(self):
        """ make sure a query with status longer than MAX_STATUS chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'update %s' % ('a'*(MAX_STATUS+1)))
        self.assertRaises(StatusTooLongException, message_parser.parse, 
                          message)


if __name__ == '__main__':
    unittest.main()