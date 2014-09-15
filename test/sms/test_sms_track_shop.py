'''
@author: janaka

Test collection for shop subscription message parsing
'''

import unittest
from src.sms import message_parser
from src.task import query
from message_parser import *
from exception.exception import *
from src.model.entity.message import IncomingSMS
from src.config import util


class TrackShopSMSTest(unittest.TestCase):

    def test_track_shop_sms_with_name_only_1(self):
        """ test shop track query with name only """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'track Royal Diner')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.TRACK_SHOP)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['shop'], 'Royal Diner')
        self.assertEqual(parsed.params['address'], None)

    def test_track_shop_sms_with_name_only_2(self):
        """ test shop track query with name only """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'track n:Royal Diner')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.TRACK_SHOP)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['shop'], 'Royal Diner')
        self.assertEqual(parsed.params['address'], None)

    def test_track_shop_sms_with_name_and_address(self):
        """ test shop track query with name and address """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'track n:Royal Diner a:Moratuwa')
        parsed = message_parser.parse(message)
        self.assertEqual(parsed.type, query.TRACK_SHOP)
        self.assertEqual(parsed.params['phone'], '94770000000')
        self.assertEqual(parsed.params['shop'], 'Royal Diner')
        self.assertEqual(parsed.params['address'], 'Moratuwa')

    def test_no_name_track_shop_sms(self):
        """ make sure a shop track query with no shop name doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 'track')
        self.assertRaises(QueryNameTooShortException, message_parser.parse, 
                          message)

    def test_short_name_track_shop_sms(self):
        """ make sure a query with shop name shorter than MIN_NAME_QUERY 
            chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'track n:%s' % ('a'*(MIN_NAME_QUERY-1)))
        self.assertRaises(QueryNameTooShortException, message_parser.parse, 
                          message)

    def test_long_name_track_shop_sms(self):
        """ make sure a query with shop name longer than MAX_NAME_QUERY
            chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              'track n:%s' % ('a'*(MAX_NAME_QUERY+1)))
        self.assertRaises(QueryNameTooLongException, message_parser.parse, 
                          message)

    def test_short_address_track_shop_sms(self):
        """ make sure a query with shop address shorter than 
            MIN_ADDRESS_QUERY chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('track n:name1 a:%s' 
                               % ('a'*(MIN_ADDRESS_QUERY-1))))
        self.assertRaises(QueryAddressTooShortException, message_parser.parse, 
                          message)

    def test_long_address_track_shop_sms(self):
        """ make sure a query with shop address longer than 
            MAX_ADDRESS_QUERY chars doesn't proceed """
        message = IncomingSMS('94770000000', util.current_time(), 
                              ('track n:name1 a:%s' 
                               % ('a'*(MAX_ADDRESS_QUERY+1))))
        self.assertRaises(QueryAddressTooLongException, message_parser.parse, 
                          message)


if __name__ == '__main__':
    unittest.main()