from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from shop.models import Profile, Category, Item


class WebPagesViewTest(TestCase):
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
            balance=1000
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

    def test_login_view(self):
        url = reverse('login')
        template = 'login.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_registration_view(self):
        url = reverse('registration')
        template = 'registration.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_main_view(self):
        url = reverse('main')
        template = 'main.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_categories_list_view(self):
        url = reverse('categories_list')
        template = 'category_list.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_products_list_view(self):
        url = '/smartphones/'
        template = 'products.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_detailed_view(self):
        url = '/product-details/1'
        template = 'product_details.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)

    def test_cart_view(self):
        url = reverse('cart')
        template = 'cart.html'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)
        self.client.login(username=self.username,
                          password=self.password
                          )
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template)
