from django.test import TestCase
from django.urls import reverse


class FormsTest(TestCase):

    def test_registration(self):
        payload = dict(username='john',
                       password='helloworld11',
                       first_name='John',
                       last_name='Johnson',
                       email='test@test.com',
                       phone_number='+78994738292',
                       city='Moscow',
                       balance=10000)
        response = self.client.post(reverse('registration'), payload)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration.html')
