# encoding: utf-8
import unittest
from create_bills import Order


class OrderTests(unittest.TestCase):

    def test_order_class_saves_parameter(self):
        self.order = Order(order_id=4711,
                           order_date='28.02.2014',
                           order_status='eventuell',
                           total=499,
                           tax=12)
        self.assertEqual(self.order.order_id, 4711)
        self.assertEqual(self.order.order_date, '28.02.2014')
        self.assertEqual(self.order.order_status, 'eventuell')
        self.assertEqual(self.order.total, 499)
        self.assertEqual(self.order.tax, 12)
