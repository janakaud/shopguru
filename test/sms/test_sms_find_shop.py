'''
@author: janaka

Test collection for shop find message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class FindShopSMSTest(unittest.TestCase):

    def test_find_shop_sms(self):
        """ test shop find query with category """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'find hardware')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.FIND_SHOP)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['category'], 'hardware')

    def test_no_category_find_shop_sms(self):
        """ make sure a shop find query without a category doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'find')
        self.assertRaises(QueryCategoryTooShortException, message_parser.parse,
                          message)

    def test_short_category_find_shop_sms(self):
        """ make sure a shop find query with shop category shorter than 
            MIN_CATEGORY_QUERY chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('find %s' 
                               % ('a'*(MIN_CATEGORY_QUERY-1))))
        self.assertRaises(QueryCategoryTooShortException, 
                          message_parser.parse, message)

    def test_long_category_find_shop_sms(self):
        """ make sure a shop find query with shop category longer than 
            MAX_CATEGORY_QUERY chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('find %s' 
                               % ('a'*(MAX_CATEGORY_QUERY+1))))
        self.assertRaises(QueryCategoryTooLongException, 
                          message_parser.parse, message)


if __name__ == '__main__':
    unittest.main()