import random

from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.template.defaulttags import register
from .models import Category, Item, Profile, Order
from .forms import RegisterForm


def get_profile(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
    else:
        profile = None
    return profile


def check_if_registered(request):
    if not request.user.is_authenticated:
        return HttpResponse('Необходима регистрация', status=403)


def empty_cart(request):
    check_if_registered(request)
    user = Profile.objects.get(user=request.user)
    user.cart = {}
    user.save()
    return redirect('/')


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


class MainView(View):
    def get(self, request):
        item_list = list(Item.objects.all())
        random.shuffle(item_list)
        swiper_list = [item for item in item_list[:3]]
        random.shuffle(item_list)
        num = 8 if len(item_list) >= 8 else len(item_list)
        main_list = [item for item in item_list[:num]]
        return render(request, 'main.html',
                      context={'swiper_list': swiper_list, 'main_list': main_list, 'profile': get_profile(request)})


class LoginSysView(LoginView):
    template_name = 'login.html'


def logout_view(request):
    logout(request)
    return HttpResponse('Вы успешно вышли из учетной записи')


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'registration.html', context={'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            city = form.cleaned_data.get('city')
            Profile.objects.create(
                user=user,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                city=city,
                balance=10000
            )
            username = form.cleaned_data.get('username')
            raw_pass = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_pass)
            login(request, user)
            return redirect('/')
        return render(request, 'registration.html', {'form': form})


class CategoriesView(View):
    def get(self, request):
        try:
            categories = Category.objects.all()
            return render(request, 'category_list.html',
                          context={'category_list': categories, 'profile': get_profile(request)})
        except Category.DoesNotExist:
            return render(request, 'category_list.html',
                          context={'category_list': None, 'profile': get_profile(request)})


class ProductsView(View):
    def get(self, request, index):
        try:
            category = Category.objects.get(category_index=index)
            products = Item.objects.filter(category=category).all()
            return render(request, 'products.html', context={'exist': True,
                                                             'products_list': products,
                                                             'category': category.category_name,
                                                             'profile': get_profile(request)})
        except Category.DoesNotExist:
            return render(request, 'products.html', context={'exist': False})


class ProductDetailView(View):
    def get(self, request, id):
        try:
            product = Item.objects.get(pk=id)
            return render(request, 'product_details.html',
                          context={'product': product, 'profile': get_profile(request)})
        except Item.DoesNotExist:
            return redirect('/categories/')


class CartView(View):
    def get(self, request):
        check_if_registered(request)
        user = Profile.objects.get(user=request.user)
        cart = user.cart
        total_price = sum([item['price'] for item in user.cart.values()])
        return render(request, 'cart.html',
                      context={'cart': cart, 'total_price': total_price, 'profile': get_profile(request)})


class AddToCartView(View):
    def get(self, request, id):
        try:
            check_if_registered(request)
            user = Profile.objects.get(user=request.user)
            item = Item.objects.get(pk=id)
            cart = user.cart
            index = str(item.id)
            if index in cart:
                cart[index]['amount'] += 1
                cart[index]['price'] += item.price
            else:
                cart[item.id] = {'title': item.title, 'amount': 1, 'price': item.price, 'img': item.image.name}
            user.save()
            return redirect(request.META.get('HTTP_REFERER'))
        except Item.DoesNotExist:
            return HttpResponse('Id товара недействителен', status=401)


class DeleteFromCartView(View):
    def get(self, request, id):
        check_if_registered(request)
        user = Profile.objects.get(user=request.user)
        try:
            user.cart.pop(str(id))
        except KeyError:
            return HttpResponse('Id товара недействителен', status=401)
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))


class MakeOrderView(View):
    def get(self, request):
        check_if_registered(request)
        user = Profile.objects.get(user=request.user)
        total = sum([item['price'] for item in user.cart.values()])
        if not user.cart:
            return HttpResponse('Корзина пуста', status=401)
        if total > user.balance:
            return HttpResponse('Недостаточно средств', status=401)
        Order.objects.create(
            user=user.user,
            list=user.cart
        )
        user.cart = {}
        user.balance -= total
        user.save()
        return redirect(request.META.get('HTTP_REFERER'))
