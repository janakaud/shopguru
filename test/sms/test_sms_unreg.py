'''
@author: janaka

Test collection for unregistration message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class UnregistrationSMSTest(unittest.TestCase):

    def test_bad_format_unreg_sms(self):
        """ make sure a unregistration SMS of bad format doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'unreg')
        self.assertRaises(UnregistrationException, message_parser.parse, 
                          message)

    def test_unreg_cust_sms(self):
        """ test customer unregistration query with name only """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'unreg cust')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.CUST_UNREGISTER)
        self.assertEqual(parsed.params['phone'], '94770000000')

    def test_unreg_shop_sms(self):
        """ test customer unregistration query with name only """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'unreg shop')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.SHOP_UNREGISTER)
        self.assertEqual(parsed.params['phone'], '94770000000')


if __name__ == '__main__':
    unittest.main()