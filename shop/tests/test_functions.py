from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Profile, Category, Item


class FunctionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        username = 'john'
        password = 'helloworld11'
        user = User.objects.create_superuser(username=username, email='lennon@thebeatles.com', password=password)
        user.is_staff = True
        user.save()
        Profile.objects.create(
            user=user,
            first_name='John',
            last_name='Johnson',
            email='test@test.com',
            phone_number='+78994738292',
            city='Moscow',
            balance=10000
        )
        cls.user = user
        cls.username = username
        cls.password = password

        Category.objects.create(
            id=1,
            category_name='Телефоны',
            category_index='smartphones',
        )
        Item.objects.create(
            id=1,
            title='iPhone 13',
            description='Lorem ipsum100x',
            category=Category.objects.get(pk=1),
            price=799,
        )

    def test_add_to_cart(self):
        url = '/add-to-cart/1'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username=self.username,
                          password=self.password
                          )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        cart = Profile.objects.get(pk=1).cart
        self.assertNotEqual(cart, {})

    def test_delete_from_cart(self):
        url = '/delete-from-cart/1'
        self.client.login(username=self.username,
                          password=self.password
                          )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 401)
        self.client.get('/add-to-cart/1')
        self.assertNotEqual(Profile.objects.get(pk=1).cart, {})
        self.client.get(url)
        self.assertEqual(Profile.objects.get(pk=1).cart, {})

    def test_empty_cart(self):
        url = '/empty-cart/'
        self.client.login(username=self.username,
                          password=self.password
                          )
        for _ in range(10):
            self.client.get('/add-to-cart/1')
        self.assertNotEqual(Profile.objects.get(pk=1).cart, {})
        self.client.get(url)
        self.assertEqual(Profile.objects.get(pk=1).cart, {})

    def test_make_order(self):
        url = reverse('make_order')
        self.client.login(username=self.username,
                          password=self.password
                          )
        for _ in range(3):
            self.client.get('/add-to-cart/1')
        user = Profile.objects.get(pk=1)
        balance = user.balance
        cart = user.cart
        total = sum([item['price'] for item in cart.values()])
        self.client.get(url)
        self.assertEqual(Profile.objects.get(pk=1).cart, {})
        self.assertEqual(balance - total, Profile.objects.get(pk=1).balance)
