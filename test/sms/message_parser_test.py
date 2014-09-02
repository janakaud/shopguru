'''
@author: janaka

Test collection for message parser module
'''

import unittest
from src.sms import message_parser
from message_parser import RegistrationException, MissingNameException
from src.model.entity.message import IncomingSMS
from src.config import util


class MessageParserTest(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_bad_format_reg_sms(self):
        """ make sure a registration SMS of bad format does not return a query """
        message = IncomingSMS('94770000000', util.current_time(), 'reg')
        self.assertRaises(RegistrationException, message_parser.parse, message)

    def test_no_details_reg_cust_sms(self):
        """ make sure an SMS without customer data does not return a query """
        message = IncomingSMS('94770000000', util.current_time(), 'reg cust')
        self.assertRaises(RegistrationException, message_parser.parse, message)

    def test_no_name_reg_cust_sms(self):
        """ make sure an SMS without customer name does not return a query """
        message = IncomingSMS('94770000000', util.current_time(), 'reg cust n:')
        self.assertRaises(MissingNameException, message_parser.parse, message)

    def test_no_details_reg_shop_sms(self):
        """ make sure an SMS without shop data does not return a query """
        message = IncomingSMS('94770000000', util.current_time(), 'reg shop')
        self.assertRaises(RegistrationException, message_parser.parse, message)

    def test_no_name_reg_shop_sms(self):
        """ make sure an SMS without shop name does not return a query """
        message = IncomingSMS('94770000000', util.current_time(), 'reg shop n:')
        self.assertRaises(MissingNameException, message_parser.parse, message)


if __name__ == '__main__':
    unittest.main()