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


def empty_cart(request):
    if not request.user.is_authenticated:
        return HttpResponse('Необходима регистрация', status=403)
    user = Profile.objects.get(user=request.user)
    user.cart = {}
    user.save()
    return redirect('/')


def get_total_amount(request):
    user = get_profile(request)
    if not user:
        return None
    if user.cart:
        amount = sum([item['amount'] for item in user.cart.values()])
    else:
        amount = None
    return amount


def custom_render(request, template, context):
    context['profile'] = get_profile(request)
    context['amount'] = get_total_amount(request)
    return render(request, template, context)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def is_enough(total_sum, balance):
    if balance - total_sum <= 0:
        return False
    else:
        return True


class MainView(View):
    def get(self, request):
        item_list = list(Item.objects.all())
        random.shuffle(item_list)
        swiper_list = [item for item in item_list[:3]]
        random.shuffle(item_list)
        num = 8 if len(item_list) >= 8 else len(item_list)
        main_list = [item for item in item_list[:num]]
        return custom_render(request, 'main.html',
                             context={'swiper_list': swiper_list, 'main_list': main_list})


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
            return custom_render(request, 'category_list.html',
                                 context={'category_list': categories})
        except Category.DoesNotExist:
            return custom_render(request, 'category_list.html',
                                 context={'category_list': None})


class ProductsView(View):
    def get(self, request, index):
        try:
            category = Category.objects.get(category_index=index)
            products = Item.objects.filter(category=category).all()
            return custom_render(request, 'products.html', context={'exist': True,
                                                                    'products_list': products,
                                                                    'category': category.category_name, })
        except Category.DoesNotExist:
            return custom_render(request, 'products.html', context={'exist': False})


class ProductDetailView(View):
    def get(self, request, id):
        try:
            product = Item.objects.get(pk=id)
            return custom_render(request, 'product_details.html',
                                 context={'product': product})
        except Item.DoesNotExist:
            return redirect('/categories/')


class CartView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Необходима регистрация', status=403)
        user = Profile.objects.get(user=request.user)
        cart = user.cart
        total_price = sum([item['price'] for item in user.cart.values()])
        return custom_render(request, 'cart.html',
                             context={'cart': cart, 'total_price': total_price})


class AddToCartView(View):
    def get(self, request, id):
        try:
            if not request.user.is_authenticated:
                return HttpResponse('Необходима регистрация', status=403)
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
            return redirect(request.META.get('HTTP_REFERER') or '/')
        except Item.DoesNotExist:
            return HttpResponse('Id товара недействителен', status=401)


class DeleteFromCartView(View):
    def get(self, request, id):
        if not request.user.is_authenticated:
            return HttpResponse('Необходима регистрация', status=403)
        user = Profile.objects.get(user=request.user)
        try:
            user.cart.pop(str(id))
        except KeyError:
            return HttpResponse('Id товара недействителен', status=401)
        user.save()
        return redirect(request.META.get('HTTP_REFERER') or '/')


class MakeOrderView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return HttpResponse('Необходима регистрация', status=403)
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
        return redirect(request.META.get('HTTP_REFERER') or '/')


class OrdersView(View):
    def get(self, request):
        if not request.user.is_staff:
            return HttpResponse('Нужны права администратора', status=403)
        orders = Order.objects.all()
        return custom_render(request, 'orders.html', context={'order_list': orders})
