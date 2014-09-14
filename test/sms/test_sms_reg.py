'''
@author: janaka

Test collection for registration message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class RegistrationSMSTest(unittest.TestCase):

    def test_reg_cust_sms_with_name_only(self):
        """ test customer registration query with name only """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg cust n:janaka')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.CUST_REGISTER)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['name'], 'janaka')
        self.assertEqual(parsed.params['address'], None)

    def test_reg_cust_sms_with_name_and_address(self):
        """ test customer registration query with name and address """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg cust n:janaka a:molpe, moratuwa 10400')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.CUST_REGISTER)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['name'], 'janaka')
        self.assertEqual(parsed.params['address'], 'molpe, moratuwa 10400')

    def test_bad_format_reg_sms(self):
        """ make sure a registration SMS of bad format doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'reg')
        self.assertRaises(RegistrationException, message_parser.parse, message)

    def test_no_details_reg_cust_sms(self):
        """ make sure a query without customer data doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'reg cust')
        self.assertRaises(MissingCustomerNameException, message_parser.parse, 
                          message)

    def test_no_name_reg_cust_sms(self):
        """ make sure a query without customer name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg cust n:')
        self.assertRaises(ActualNameTooShortException, message_parser.parse, 
                          message)

    def test_short_name_reg_cust_sms(self):
        """ make sure a query with customer name shorter than MIN_NAME_ACTUAL 
            chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg cust n:%s' % ('a'*(MIN_NAME_ACTUAL-1)))
        self.assertRaises(ActualNameTooShortException, message_parser.parse, 
                          message)

    def test_long_name_reg_cust_sms(self):
        """ make sure a query with customer name longer than MAX_NAME_ACTUAL
            chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg cust n:%s' % ('a'*(MAX_NAME_ACTUAL+1)))
        self.assertRaises(ActualNameTooLongException, message_parser.parse, 
                          message)

    def test_short_address_reg_cust_sms(self):
        """ make sure a query with customer address shorter than 
            MIN_ADDRESS_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg cust n:name1 a:%s' 
                               % ('a'*(MIN_ADDRESS_ACTUAL-1))))
        self.assertRaises(ActualAddressTooShortException, message_parser.parse, 
                          message)

    def test_long_address_reg_cust_sms(self):
        """ make sure a query with customer address longer than 
            MAX_ADDRESS_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg cust n:name1 a:%s' 
                               % ('a'*(MAX_ADDRESS_ACTUAL+1))))
        self.assertRaises(ActualAddressTooLongException, message_parser.parse, 
                          message)

    def test_no_details_reg_shop_sms(self):
        """ make sure a query without shop data doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'reg shop')
        self.assertRaises(MissingShopNameException, message_parser.parse, 
                          message)

    def test_no_name_reg_shop_sms(self):
        """ make sure a query without shop name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg shop n:')
        self.assertRaises(ActualNameTooShortException, message_parser.parse, 
                          message)

    def test_short_name_reg_shop_sms(self):
        """ make sure a query with shop name shorter than MIN_NAME_ACTUAL chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg shop n:%s' % ('a'*(MIN_NAME_ACTUAL-1)))
        self.assertRaises(ActualNameTooShortException, message_parser.parse, 
                          message)

    def test_long_name_reg_shop_sms(self):
        """ make sure a query with shop name longer than MAX_NAME_ACTUAL chars
            doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg shop n:%s' % ('a'*(MAX_NAME_ACTUAL+1)))
        self.assertRaises(ActualNameTooLongException, message_parser.parse, 
                          message)

    def test_short_address_reg_shop_sms(self):
        """ make sure a query with shop address shorter than 
            MIN_ADDRESS_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg shop n:shop1 a:%s' 
                               % ('a'*(MIN_ADDRESS_ACTUAL-1))))
        self.assertRaises(ActualAddressTooShortException, message_parser.parse,
                          message)

    def test_long_address_reg_shop_sms(self):
        """ make sure a query with shop address longer than 
            MAX_ADDRESS_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg shop n:shop1 a:%s' 
                               % ('a'*(MAX_ADDRESS_ACTUAL+1))))
        self.assertRaises(ActualAddressTooLongException, message_parser.parse,
                          message)

    def test_no_category_reg_shop_sms(self):
        """ make sure a query without shop name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'reg shop n:shop1 c:')
        self.assertRaises(ActualCategoryTooShortException, 
                          message_parser.parse, message)

    def test_short_category_reg_shop_sms(self):
        """ make sure a query with shop category shorter than 
            MIN_CATEGORY_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg shop n:shop1 c:%s' 
                               % ('a'*(MIN_CATEGORY_ACTUAL-1))))
        self.assertRaises(ActualCategoryTooShortException, 
                          message_parser.parse, message)

    def test_long_category_reg_shop_sms(self):
        """ make sure a query with shop category longer than 
            MAX_CATEGORY_ACTUAL chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('reg shop n:shop1 c:%s' 
                               % ('a'*(MAX_CATEGORY_ACTUAL+1))))
        self.assertRaises(ActualCategoryTooLongException, 
                          message_parser.parse, message)


if __name__ == '__main__':
    unittest.main()