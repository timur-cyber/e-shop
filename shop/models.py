import datetime
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from jsonfield import JSONField


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')
    email = models.CharField(max_length=30, blank=True, verbose_name='Эл. Почта')
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')
    city = models.CharField(max_length=20, blank=True, verbose_name='Город')
    cart = JSONField(default={}, null=True)
    balance = models.PositiveIntegerField()

    def __str__(self):
        return self.user.username


class Category(models.Model):
    category_name = models.CharField(max_length=30)
    category_index = models.CharField(max_length=15, unique=True)
    image = models.ImageField(default=None, null=True)

    def __str__(self):
        return self.category_name


class Item(models.Model):
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    image = models.ImageField(default=None)

    def __str__(self):
        return self.title


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    list = JSONField()
    date = models.DateTimeField(default=now)
