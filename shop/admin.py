from django.contrib import admin
from .models import Profile, Category, Item, Order


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'email', 'phone_number', 'city']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'category_index']


class ItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'category', 'price', 'image']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'date']


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)
