from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User

from Order.models import *
from UserInfo.models import *
from ItemInfo.models import *

class SimpleTest(TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)

def setUpTestCase():
    
    user = User.objects.create_user('customer1', 'customer1@163.com', 'aaabbb')
    user.save()
    userInfo = UserInfo(user=user, balance=1000, address='ZJU-yq')
    userInfo.save()

    user = User.objects.create_user('customer2', 'customer2@163.com', 'bbbaaa')
    user.save()
    userInfo = UserInfo(user=user, balance=5000, address='ZJU-zjg')
    userInfo.save()

    user = User.objects.create_user('seller1', 'seller1@gmail.com', 'iamseller')
    user.save()
    userInfo = UserInfo(user=user, balance=10000, address='ZJU-xx')
    userInfo.save()

    item = ItemInfo(seller=user, product_name="item1", price=10, storage=1000)
    item.save()
    item = ItemInfo(seller=user, product_name="item2", price=5, storage=50)
    item.save()
    item = ItemInfo(seller=user, product_name="item100", price=1000, storage=100)
    item.save()

class UserInfoTest(TestCase):
    def setUp(self):
        setUpTestCase()
    def test_users(self):
        cus1 = User.objects.get(username='customer1')
        cus2 = User.objects.get(username='customer2')
        balance1 = UserInfo.objects.get(user=cus1).balance
        address1 = UserInfo.objects.get(user=cus1).address
        self.assertEqual(balance1, 1000)
        self.assertEqual(address1, 'ZJU-yq')
        balance2 = UserInfo.objects.get(user=cus2).balance
        address2 = UserInfo.objects.get(user=cus2).address
        self.assertEqual(balance2, 5000)
        self.assertEqual(address2, 'ZJU-zjg')

class ItemInfoTest(TestCase):
    def setUp(self):
        setUpTestCase()
    def test_users(self):
        item1 = ItemInfo.objects.get(product_name='item1')
        item2 = ItemInfo.objects.get(product_name='item100')
        self.assertEqual(item1.price, 10)
        self.assertEqual(item2.price, 1000)
        self.assertEqual(item1.storage, 1000)
        self.assertEqual(item2.storage, 100)

class MyOrderTest(TestCase):
    def setUp(self):
        setUpTestCase()
    def test_my_order(self):
        c = Client()
        res = c.login(username='customer1', password='aaabbb')
        self.assertTrue(res)
        response = c.get('/order/')
        self.assertTrue(response.content.find('customer1')!=-1)

